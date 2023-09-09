import bcrypt
import requests

from helpers.strings import encode_base64


def is_strong_password(password: str) -> bool:
    password_size = len(password)  # CHECK PASSWORD SIZE
    if 8 <= password_size <= 20:
        has_letters = any(char.isalpha() for char in password)
        has_numbers = any(char.isdigit() for char in password)
        has_special_characters = any(not char.isalnum() for char in password)

        return has_letters and has_numbers and has_special_characters
    else:
        return False


# REQUEST A RANDOM VECTOR WHICH IS THEN USED A PROFILE IMAGE
def generate_profile_image() -> bytes or None:
    """
        Generates a random profile image during the registration process

    :return: bytes or None
    """
    url = "https://source.boringavatars.com/beam/128?square"
    r = requests.get(url)
    if r.status_code == 200:
        image_data = r.content
        image_data = encode_base64(image_data)
    else:
        image_data = None

    return image_data


def hash_password(password: str) -> bytes:
    """
        Hashes the password in order to be stored securely in the database

    :param password: Password in string format
    :return: [bytes] hashed password
    """
    hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
    return hashed_password
