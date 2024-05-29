import ecies
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt

import chardet

def encrypt_data(message, public_key) -> bytes:
  """
  Function transforms string input (message) into bytes
  to allow ecies library to function properly
  Input: string, eth_keys.datatypes.PrivateKey
  Return: <class 'bytes'> encrypted message
  """
  return encrypt(public_key, message)

def decrypt_data(encrypted_message, private_key) -> bytes:
  return decrypt(private_key, encrypted_message)

def generate_key():
  return generate_eth_key()

def create_public_key(key):
  return key.public_key.to_hex()

def create_private_key(key):
  return key.to_hex()

if __name__ == "__main__":
  key = generate_key()
  cypher = encrypt_data(b'test', create_public_key(key))
  print("test: ", cypher)
  print(decrypt_data(cypher, create_private_key(key)))