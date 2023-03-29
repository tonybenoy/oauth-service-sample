import uuid
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required

from src.models.document import Client, User
from src.utils.helper import (
    check_existing_client,
    check_existing_user,
    encrypt_password,
)

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


@user_bp.route("/login", methods=["POST"])
def login() -> Tuple[Dict[str, str], int]:
    """This method is used to login the user
    :param username: username of the user
    :param password: password of the user
    :return: access token
    """
    login_details = request.get_json()
    user_from_db = check_existing_user(login_details["username"])
    if user_from_db:
        encrpted_password = encrypt_password(login_details["password"])
        if encrpted_password == user_from_db["password"]:
            access_token = create_access_token(identity=user_from_db["username"])
            return {"access_token": access_token}, 200

    return {"message": "Invalid credentials!"}, 401


@user_bp.route("/register/client", methods=["POST"])  # type: ignore
@jwt_required  # type: ignore
def register_client() -> Tuple[Dict[str, str], int]:
    """This method is used to register the client
    :param client_id: client id of the client
    :param name: name of the client
    :param username: username of the user
    :param password: password of the user
    :return: client id and client secret
    """
    data = request.get_json()
    user_name = data.get("username")
    password = data.get("password")
    if not user_name or not password:
        return {"message": "Invalid authentication!"}, 400
    client_id = data.get("client_id")
    name = data.get("name")
    client_secret = uuid.uuid4().hex
    encrypted_password = encrypt_password(password)
    user = check_existing_user(user_name, encrypted_password)
    if not user or user.password != encrypted_password or not user.admin:
        return {"message": "Invalid authentication!"}, 400
    if not client_id or not name:
        return {"message": "Invalid client!"}, 400
    existing_client = check_existing_client(client_id)
    if existing_client:
        return {"message": "Client already exists!"}, 400
    client = Client(client_id=client_id, name=name, client_secret=client_secret)
    client.save()
    return {"client_id": client_id, "client_secret": client_secret}, 201


@user_bp.route("/register", methods=["POST"])
def register() -> Tuple[Dict[str, str], int]:
    """This method is used to register the user
    :param username: username of the user
    :param password: password of the user
    :param admin: admin status of the user
    :return: user registered message"""
    params = request.get_json()
    username = params.get("username")
    password = params.get("password")
    admin = params.get("admin") or False  # Ideally, this should be approved by admin
    if not username or not password:
        return {"message": "Invalid username or password!"}, 400
    encrypted_password = encrypt_password(password)
    existing_user = check_existing_user(username)
    if existing_user:
        return {"message": "User already exists!"}, 400
    user = User(username=username, password=encrypted_password, admin=admin)
    user.save()
    return {"message": "User registered!"}, 201
