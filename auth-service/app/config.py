import os

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

    # MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    # MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    # MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    # MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
