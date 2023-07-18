import re


def is_valid_full_name(full_name):
    pattern = r'^[A-Za-z\s-]{2,}(?: [A-Za-z\s-]{2,})+$'
    return bool(re.match(pattern, full_name))


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))



