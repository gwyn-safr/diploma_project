import pytest

from src.encrypting import generate_key



def test_passing():
    assert (1, 2, 3) == (1, 2, 4)

def key_generation_test():
    key = generate_key()
    assert  generate_key() == generate_key()

def public_key_creatino_test():
    assert (1, 2, 3) == (1, 2, 3)

def privite_key_creation_test():
    assert (1, 2, 3) == (1, 2, 3)

def ecies_encryption_test():
    assert (1, 2, 3) == (1, 2, 3)

def ecies_decryption_test():
    assert (1, 2, 3) == (1, 2, 3)

def psycorg_connection_test():
    pass