from app.models.user_model import get_user_by_email, create_user
from app.utils.password_utils import hash_password, check_password

def register_user(email, password):
    if get_user_by_email(email):
        return False, "User already exists"
    hashed = hash_password(password)
    create_user(email, hashed)
    return True, "User registered successfully"

def authenticate_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return None
    if check_password(password, user["password"]):
        return user
    return None
