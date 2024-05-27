import pytest

import sys
sys.path.append("./src")
from hashing import generate_key, hash
from extra import has_duplicates

import string
import itertools

def test_hash_stability():
    private_key = generate_key()
    assert hash(b"test", private_key) == hash(b"test", private_key)

def test():
  private_key = generate_key()

  # Generate all possible messages with current alphabeth
  messages = [''.join(tup)for tup in list(itertools.combinations_with_replacement(string.ascii_lowercase, 5))]
  # Alarm the user if 
  if has_duplicates(messages): print("Repeating messages")
  else: print("messages good")
  for elem in input():
     if elem in ['y','д']:
          hashes = [hash(bytes(message, 'utf-8'), private_key) for message in messages]
          if has_duplicates(hashes): print("Repeating hashes")
          else: print("hashes good")
     else: print("Skipping further computations")