import string
from datetime import datetime
from datetime import timedelta
from random import choices
from random import randint


def get_random_boolean() -> bool:
    return bool(randint(0, 1))


def get_random_lower_string(string_length: int) -> str:
    return "".join(choices(string.ascii_lowercase, k=string_length))


def get_random_upper_string(string_length: int) -> str:
    return "".join(choices(string.ascii_uppercase, k=string_length))


def get_random_lower_alphanumeric_string(string_length: int) -> str:
    return "".join(
        choices(string.ascii_lowercase + string.digits, k=string_length)
    )


def get_random_upper_alphanumeric_string(string_length: int) -> str:
    return "".join(
        choices(string.ascii_uppercase + string.digits, k=string_length)
    )


def get_random_mixed_alphanumeric_string(string_length: int) -> str:
    return "".join(
        choices(string.ascii_letters + string.digits, k=string_length)
    )


def get_random_numeric_string(string_length: int) -> str:
    return "".join(choices(string.digits, k=string_length))


def get_random_string(string_length: int) -> str:
    return "".join(choices(string.printable, k=string_length))


def get_random_date_string():
    return (
        (
            datetime.utcnow()
            - timedelta(
                days=randint(0, 30),
                hours=randint(0, 24),
                minutes=randint(0, 60),
                seconds=randint(0, 60),
            )
        )
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )


def get_random_string_string_dictionary():
    string_string_dictionary = {}
    for i in range(randint(3, 10)):
        key = get_random_lower_string(randint(5, 8))
        value = get_random_lower_string(randint(5, 8))
        string_string_dictionary[key] = value
    return string_string_dictionary
