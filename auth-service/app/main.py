from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from pymongo import MongoClient
import redis

from app.routes.auth_routes import auth_bp
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Extensions
jwt = JWTManager(app)
mail = Mail(app)
redis_client = redis.StrictRedis(host=app.config["REDIS_HOST"], port=6379, decode_responses=True)
mongo_client = MongoClient(app.config["MONGO_URI"])
db = mongo_client["auth_db"]

# Register routes
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
