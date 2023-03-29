import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

from src.routes.auth import oauth_bp
from src.routes.kyc import kyc_bp
from src.routes.user import user_bp
from src.utils.oauth_utils import oauth

load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL"))

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": os.getenv("MONGO_DB"),
    "host": os.getenv("MONGO_DB_HOST"),
}
db = MongoEngine(app)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
oauth.init_app(app)

app.register_blueprint(oauth_bp)
app.register_blueprint(kyc_bp)
app.register_blueprint(user_bp)


@app.route("/")
def test():
    return {"message": "API works!"}, 200
