import random
import string
import uuid
from itertools import permutations, combinations
import datetime
import json

FIRST_NAMES = ['John', 'Jane', 'Alice', 'Bob', 'David', 'Emma', 'Liam', 'Olivia']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
EMAIL_DOMAINS = ['example.com', 'test.com', 'mail.com', 'demo.org']

def random_string(length=8):
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random string: {str(e)}")

def random_number(length=6):
    try:
        return ''.join(random.choices(string.digits, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random number: {str(e)}")

def random_alphabets(length=8):
    try:
        return ''.join(random.choices(string.ascii_letters, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random alphabets: {str(e)}")

def random_password(length=12):
    try:
        if length < 8 or length > 24:
            raise ValueError("Password length must be between 8 and 24 characters.")

        # Required characters
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)

        # Remaining characters
        remaining_length = length - 4
        all_chars = string.ascii_letters + string.digits + string.punctuation
        remaining = random.choices(all_chars, k=remaining_length)

        # Combine and shuffle
        password_list = [uppercase, lowercase, digit, special] + remaining
        random.shuffle(password_list)
        return ''.join(password_list)

    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random password: {str(e)}")

def random_integer(min_value=0, max_value=100):
    try:
        return random.randint(min_value, max_value)
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random integer: {str(e)}")

def load_card_details(filepath='testdata/E2E_data.json'):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data['card']

def random_first_name():
    return random.choice(FIRST_NAMES)

def random_last_name():
    return random.choice(LAST_NAMES)

def random_email():
    try:
        fname = random_first_name().lower()
        lname = random_last_name().lower()
        domain = random.choice(EMAIL_DOMAINS)
        num = random.randint(100, 999)
        return f"{fname}.{lname}{num}@{domain}"
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate email: {str(e)}")
    
def generate_uuid():
    try:
        return str(uuid.uuid4())
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate UUID: {str(e)}")

def generate_combinations(input_list, r):
    try:
        return list(combinations(input_list, r))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate combinations: {str(e)}")

def generate_permutations(input_list, r):
    try:
        return list(permutations(input_list, r))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate permutations: {str(e)}")

def get_current_datetime():
    try:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise Exception(f"[ERROR] Failed to get current datetime: {str(e)}")

def format_datetime(dt, format='%Y-%m-%d'):
    try:
        return dt.strftime(format)
    except Exception as e:
        raise Exception(f"[ERROR] Failed to format datetime: {str(e)}")

def generate_us_mobile_number(formatted: bool = False) -> str:
    # US country code
    country_code = "+1"

    # Valid area codes excluding toll-free numbers (800, 888, etc.)
    valid_area_codes = [
        201, 202, 203, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216,
        217, 218, 219, 224, 225, 228, 229, 231, 234, 239, 240, 248, 251, 252,
        253, 254, 256, 260, 262, 267, 269, 270, 272, 274, 276, 281, 283, 301,
        302, 303, 304, 305, 307, 308, 309, 310, 312, 313, 314, 315, 316, 317,
        318, 319, 320, 321, 323, 325, 330, 331, 334, 336, 337, 339, 346, 347
    ]

    area_code = str(random.choice(valid_area_codes))
    exchange_code = str(random.randint(200, 999)).zfill(3)
    subscriber_number = str(random.randint(0, 9999)).zfill(4)

    if formatted:
        return f"{country_code} ({area_code}) {exchange_code}-{subscriber_number}"
    else:
        return f"{country_code}{area_code}{exchange_code}{subscriber_number}"