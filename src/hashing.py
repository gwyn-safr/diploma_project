from ecdsa import SigningKey, NIST256p
from hashlib import sha256
from ecdsa.util import sigencode_der

def generate_key():
  """
  Returns ecdsa.key object created in a curve NIST256p
  """
  return SigningKey.generate(curve=NIST256p)

def export_key(key):
  """
  Store ecdsa.key object as a file
  """
  with open("priv_key.pem", "wb") as f:
    f.write(key.to_pem(format="pkcs8"))

def import_key():
  """
  Import previously generated key
  """
  with open("priv_key.pem") as f:
    key = SigningKey.from_pem(f.read())
  return key

def hash(message, private_key):
  """
  Hashing message with sha256 and key generated on elliptic curve
  """
  return private_key.sign_deterministic(
    message,
    hashfunc=sha256,
    sigencode=sigencode_der)

if __name__ == "__main__":
  private_key = generate_key()
  message = b"test text"
  print(f"Usage example:\nText: {message}\nKey:{private_key}\nHash: {hash(message, private_key)}")