from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

import chardet
import re

from psycopg2 import sql
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

class UnauthorizedAccessError(Exception):
  """
  Only users themselfs, and admin can change user password.
  """

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
  pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'
  print(passwd.decode("utf-8"))
  if re.match(pattern, passwd.decode("utf-8")):
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
  cur.execute("Select * from Сотрудники;")
  existing_user_list = cur.fetchall()
  cur.close()
  conn.close()
  return [[user[-2],user[-1]] for user in existing_user_list]

def is_that_user(user):
  """
  Checks if corrent user is trying to access his own data in database
  """
  pass

def is_admin(user):
  """
  Checks if admin is trying to access database
  """
  return True

def change_user_data(find, search_field_name, replacement, replacement_field_name) -> bool:
  """
  Allows you to make changes in database table "Сотрудники".
  Returns boolian if query was executed
  """
  # if not is_that_user() or  not is_admin():
  #   raise UnauthorizedAccessError("Action is now allowed")
  try:
    config = load_config()
    conn = connect(config)
    cur = conn.cursor()
    # cur.execute("update Сотрудники set Логин = (%s) where (%s) = (%s);", (replacement, "Логин", find))
    cur.execute(sql.SQL("Update Сотрудники Set {replacement_field_name} = %s Where {search_field_name} = %s").format(
        replacement_field_name=sql.Identifier(replacement_field_name), search_field_name=sql.Identifier(search_field_name)), (replacement, find))
    
    conn.commit()
    cur.execute(sql.SQL("Select * From{}").format(sql.Identifier('Сотрудники')))
    print(cur.fetchall())
    cur.close()
    conn.close()
    return True
  except:
    return False

def authenticate_user(email, passwd) -> bool :
  if is_email_valid(email) and is_passwd_valid(passwd):
    is_user_exists(email, passwd)

def is_user_exists(email, passwd):
  if encrypt_data(passwd, eth_key) in get_existing_user_list():
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

decrypt(sk_hex, encrypt(pk_hex, data))

secp_k = generate_key()
sk_bytes = secp_k.secret  # bytes
pk_bytes = secp_k.public_key.format(True)  # bytes
decrypt(sk_bytes, encrypt(pk_bytes, data))

# change_user_data("1", 'Пароль', 'NewPetr1', 'Логин')
change_user_data("NewPetr1", 'Логин', encrypt_passwd(b"mypassword1A#!", generate_eth_key()), 'Пароль')

# Successful SQL injection which doesn't work anymore
# change_user_data("NewerPetr'; update Сотрудники set Пароль = 'EvenBiggerLoser' where Логин = 'NewPetr", "NewPetr1", "Логин")