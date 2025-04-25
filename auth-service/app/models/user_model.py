from app.main import db

users = db["users"]

def get_user_by_email(email):
    return users.find_one({"email": email})

def create_user(email, password):
    users.insert_one({"email": email, "password": password})
