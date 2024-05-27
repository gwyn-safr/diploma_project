from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

import chardet

def encrypt_data(message, key) -> bytes:
  """
  Function transforms string input (message) into bytes
  to allow ecies library to function properly
  Input: string, eth_keys.datatypes.PrivateKey
  Return: <class 'bytes'> encrypted message
  """
  # eth_k.public_key.to_hex()  # hex string
  return encrypt(key.public_key.to_hex(), message)

def decrypt_data(message, key) -> bytes:
  return decrypt(key.to_hex(), encrypt(key.public_key.to_hex(), message))

def generate_encr_key():
  return generate_eth_key()

if __name__ == "__main__":
  eth_k = generate_eth_key()
  sk_hex = eth_k.to_hex()  # hex string
  pk_hex = eth_k.public_key.to_hex()  # hex string

  # https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function
  data = bytes('this is a test', 'UTF-8') # each value in string is supposed to be a hex number
  print(chardet.detect(data))

  decrypt(sk_hex, encrypt(pk_hex, data))

  secp_k = generate_key()
  sk_bytes = secp_k.secret  # bytes
  pk_bytes = secp_k.public_key.format(True)  # bytes
  decrypt(sk_bytes, encrypt(pk_bytes, data))

  print(type(decrypt_data(data, eth_k)))
  print(decrypt(sk_bytes, encrypt(pk_bytes, data)))