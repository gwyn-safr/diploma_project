from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

import chardet
import re

import psycopg2
from connect import connect
from config import load_config


"""
ecies uses secp256k1 with a 256-bit size key

"""

class InvalidCredentialsError(Exception):
  """
  Either part of authentication data is invalid, not found
  """

class InvalidPasswordError(Exception):
  """
  Unacceptable symbols used in password
  """

def sterilize_data(message) -> str:
  """
  Function to find any suspicious parts of a message and raise attention.
  Used to prevent bad things like SQL-injections
  For data passed to database
  Input: string, list of forbidded symbols
  Return: clean sterile data: <str>
  """
  pass

def encrypt_data(message, eth_key) -> bytes:
  """
  Function transforms string input (message) into bytes
  to allow ecies library to function properly
  Input: string, eth_keys.datatypes.PrivateKey
  Return: <class 'bytes'> encrypted message
  """
  # eth_k.public_key.to_hex()  # hex string
  return encrypt(eth_k.public_key.to_hex(), message)

def encrypt_passwd(passwd, eth_key) -> bytes:
  # or check if password is invalid !
  if is_passwd_valid(passwd):
    return encrypt_data(passwd, eth_key)
  else: raise InvalidPasswordError()

def decrypt_data(message, eth_key) -> bytes:
  return decrypt(eth_k.to_hex(), encrypt(eth_k.public_key.to_hex(), data))

def is_passwd_valid(passwd) -> bool:
  """
  Checks if password is alligned with requirements
  Input: password
  Return: True if password is valid
  """
  reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
  pattern = re.compile(reg)
  pattern_match = re.search(pattern, passwd)

  if pattern_match:
      return True
  else:
      return False

def is_email_valid(email) -> bool:
  """
  Checks if emails is alligned with requirements
  Input: email
  Return: True if email is valid
  """
  pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  if re.match(pattern, email):
    return True
  else:
    return False

def get_existing_user_list() -> list[list[str, str]]:
  "Returns a list of user names and hashes of passwords"
  config = load_config()
  conn = connect(config)
  cur = conn.cursor()
  cur.execute("Select * from Сотрудники")
  existing_user_list = cur.fetchall()
  print(existing_user_list)
  cur.close()
  conn.close()
  return [[user[-2],user[-1]] for user in existing_user_list]

def change_user_data(user, find, replacement, field_name):
  config = load_config()
  conn = connect(config)
  cur = conn.cursor()
  cur.execute((f"update Сотрудники set {field_name} = '{replacement}' where {field_name} = '{find}';"))
  conn.commit()
  cur.execute("Select * from Сотрудники")
  print(cur.fetchall())
  cur.close()
  conn.close()
  pass

def authenticate_user(email, passwd) -> bool :
  if is_email_valid(email) and is_passwd_valid(passwd):
    is_user_exists(email, passwd)

def is_user_exists(email, passwd):
  get_existing_user_list()
  if encrypt_data(is_passwd_valid(passwd), eth_key) in existing_passwd_list:
    return True
  else:
    raise InvalidCredentialsError("Invalid user credentials/n")


def add_user(new_user, existing_user_list):
  # Before adding user, check if there is repeating login
  pass



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

existing_user_list = get_existing_user_list()
print(existing_user_list)
first_user = existing_user_list[0]
change_user_data(existing_user_list, first_user[0], "multiPetr", "Логин")