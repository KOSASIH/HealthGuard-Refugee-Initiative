import datetime
import hashlib
import json


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + json.dumps(data)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def create_genesis_block():
    return Block(
        0,
        "0",
        datetime.datetime.now(),
        {"refugees": []},
        calculate_hash(0, "0", datetime.datetime.now(), {"refugees": []}),
    )


def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    hash = calculate_hash(index, previous_block.previous_hash, timestamp, data)
    return Block(index, previous_block.previous_hash, timestamp, data, hash)


def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        if current_block.hash != calculate_hash(
            current_block.index,
            previous_block.previous_hash,
            current_block.timestamp,
            current_block.data,
        ):
            return False

        if previous_block.index + 1 != current_block.index:
            return False

    return True


def add_refugee_to_blockchain(refugee_data):
    refugee_block = create_new_block(blockchain[-1], refugee_data)
    blockchain.append(refugee_block)


def get_refugee_data_by_id(refugee_id):
    for block in blockchain:
        for refugee in block.data["refugees"]:
            if refugee["id"] == refugee_id:
                return refugee
    return None


# Initialize blockchain
blockchain = [create_genesis_block()]

# Add sample refugee data to blockchain
add_refugee_to_blockchain(
    {
        "id": 1,
        "name": "John Doe",
        "contact_info": {"phone": "555-555-5555", "email": "johndoe@example.com"},
        "location": {"latitude": 37.7749, "longitude": -122.4194},
    }
)
add_refugee_to_blockchain(
    {
        "id": 2,
        "name": "Jane Doe",
        "contact_info": {"phone": "555-555-5556", "email": "janedoe@example.com"},
        "location": {"latitude": 34.0522, "longitude": -118.2437},
    }
)

# Validate blockchain
if is_chain_valid(blockchain):
    print("Blockchain is valid")
else:
    print("Blockchain is not valid")

# Retrieve refugee data by ID
refugee_data = get_refugee_data_by_id(1)
print(refugee_data)
