import qkd


def establish_quantum_secure_communication(public_key, receiver):
    """
    Establish a quantum-secure communication channel between the sender and the receiver.

    Args:
    public_key (str): The public key of the sender.
    receiver (qkd.Receiver): The receiver object.

    Returns:
    None
    """
    # Initialize the sender and the receiver
    sender = qkd.Sender(public_key)

    # Generate a random secret key using the BB84 protocol
    secret_key = sender.generate_secret_key(receiver)

    # Print the secret key
    print(f"Secret key: {secret_key}")


# Example usage:
if __name__ == "__main__":
    # Initialize the receiver
    receiver = qkd.Receiver()

    # Establish a quantum-secure communication channel
    establish_quantum_secure_communication("public_key_of_sender", receiver)
