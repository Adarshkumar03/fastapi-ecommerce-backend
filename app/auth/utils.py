from bcrypt import hashpw, gensalt
from sqlalchemy import Column

 
def password_validity(password: str) -> bool:
    """
    Validate the password based on specific criteria.
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    import re

    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def generate_password_hash(password: str) -> str:
    """
    Generate a hashed password using a secure hashing algorithm.
    """ 
    if not password_validity(password):
        raise ValueError("Password does not meet complexity requirements.")
    
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed.decode('utf-8')

def check_password(hashed_password: Column[str], password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    return hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')

