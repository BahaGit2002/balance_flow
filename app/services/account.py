import random
import string


def generate_account_number():
    # Generate a random 10-character alphanumeric string
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
