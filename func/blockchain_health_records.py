import hashlib
import time
import json
from flask import Flask, request, jsonify

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + json.dumps(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), {"message": "Genesis Block"}, calculate_hash(0, "0", int(time.time()), {"message": "Genesis Block"}))

def get_previous_block(blockchain):
    return blockchain[-1]

def add_new_block(blockchain, data):
    previous_block = get_previous_block(blockchain)
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.previous_hash, timestamp, data)
    block = Block(index, previous_block.previous_hash, timestamp, data, hash)
    blockchain.append(block)

def is_chain_valid(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
            return False

        if previous_block.hash != calculate_hash(previous_block.index, previous_block.previous_hash, previous_block.timestamp, previous_block.data):
            return False

    return True

def get_blockchain_json(blockchain):
    blockchain_json = []
    for block in blockchain:
        block_json = {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash
        }
        blockchain_json.append(block_json)
    return json.dumps(blockchain_json)

app = Flask(__name__)

blockchain = [create_genesis_block()]

@app.route('/new_block', methods=['POST'])
def new_block():
    data = request.get_json()
    add_new_block(blockchain, data)
    return jsonify({"message": "Block added to the blockchain"})

@app.route('/is_valid', methods=['GET'])
def is_valid():
    if is_chain_valid(blockchain):
        return jsonify({"message": "The blockchain is valid"})
    return jsonify({"message": "The blockchain is not valid"})

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    return get_blockchain_json(blockchain)

if __name__ == '__main__':
    app.run(debug=True)
