import base64
import random
import string

import bcrypt
import requests


def generate_id():
    numbers = string.digits
    file_id = "".join(random.choice(numbers) for _ in range(15))
    return file_id


def encode_base64(data: bytes) -> bytes:
    """
        Encodes bytes to Base64

    :param data: Image data in bytes
    :return: bytes
    """
    encoded: bytes = base64.b64encode(data)
    return encoded
