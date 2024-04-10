import os
import secrets
import base64
from cryptography.fernet import Fernet

def generate_random_password(length=16):
    """Generate a random password of the given length.

    Args:
        length (int): The length of the password.

    Returns:
        (str) The generated random password.
    """
    return secrets.token_hex(length // 2)

def generate_encryption_key():
    """Generate a new encryption key for encrypting and decrypting data.

    Returns:
        (bytes) The encryption key.
    """
    return Fernet.generate_key()

def encrypt_data(data, encryption_key):
    """Encrypt the given data using the provided encryption key.

    Args:
        data (bytes): The data to be encrypted.
        encryption_key (bytes): The encryption key.

    Returns:
        (bytes) The encrypted data.
    """
    f = Fernet(encryption_key)
    return f.encrypt(data)

def decrypt_data(encrypted_data, encryption_key):
    """Decrypt the given encrypted data using the provided encryption key.

    Args:
        encrypted_data (bytes): The encrypted data to be decrypted.
        encryption_key (bytes): The encryption key.

    Returns:
        (bytes) The decrypted data.
   """
    f = Fernet(encryption_key)
    return f.decrypt(encrypted_data)

def secure_file_storage(filename, data, encryption_key=None):
    """Store the file securely if an encryption key is provided, or in plain text otherwise.

    Args:
        filename (str): The name of the file to be stored.
        data (bytes): The data to be stored in the file.
        encryption_key (bytes, optional): The encryption key for encrypting and decrypting the data.
    """
    if encryption_key:
        encrypted_data = encrypt_data(data, encryption_key)
        with open(filename, 'wb') as f:
            f.write(encrypted_data)
    else:
        with open(filename, 'wb') as f:
            f.write(data)

def load_file(filename, encryption_key=None):
    """Load the file securely if an encryption key is provided, or in plain text otherwise.

    Args:
        filename (str): The name of the file to be loaded.
        encryption_key (bytes, optional): The encryption key for encrypting and decrypting the data.

    Returns:
        (bytes) The data in the file.
    """
    with open(filename, 'rb') as f:
        data = f.read()

    if encryption_key:
        return decrypt_data(data, encryption_key)
    else:
        return data

def secure_data_transmission(data, key):
    """Transmit data securely by encrypting it with the given key.

    Args:
        data (bytes): The data to be transmitted.
        key (bytes): The key for encrypting and decrypting the data.

    Returns:
        (str) The encrypted data in base64 format.
    """
    encrypted_data = encrypt_data(data, key)
    return base64.b64encode(encrypted_data).decode()

def receive_secure_data(encrypted_data_base64, key):
    """Receive data securely by decrypting it with the given key.

    Args:
        encrypted_data_base64 (str): The encrypted data in base64 format.
        key (bytes): The key for encrypting and decrypting the data.

    Returns:
        (bytes) The decrypted data.
    """
    encrypted_data = base64.b64decode(encrypted_data_base64.encode())
    return decrypt_data(encrypted_data, key)

def secure_system_access(username, password, encryption_key):
    """Authenticate users securely by encrypting and comparing their credentials.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        encryption_key (bytes): The encryption key for encrypting and decrypting the data.

    Returns:
        (bool) True if the credentials match, False otherwise.
    """
    hashed_password = password.encode()
    if not hashed_password:
        return False

    key = encryption_key
    f = Fernet(key)
    encrypted_password = f.encrypt(hashed_password)

    with open('user_credentials.txt', 'rb') as file:
        stored_password = file.read()

    if stored_password:
        stored_password = base64.b64decode(stored_password)
        stored_password = f.decrypt(stored_password)

        if stored_password.decode() == username and hashed_password == encrypted_password:
            return True
    return False
