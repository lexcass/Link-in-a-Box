import hashlib
import random
import os


def generate_key():
    random_string = str(random.random())
    return hashlib.sha224(random_string.encode('utf-8')).hexdigest()
