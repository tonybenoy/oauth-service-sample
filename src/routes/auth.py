from typing import Dict, Tuple, Union

from flask import Blueprint, request

from src.utils.helper import check_existing_user, encrypt_password
from src.utils.oauth_utils import oauth

oauth_bp = Blueprint("oauth_bp", __name__, url_prefix="/oauth")


@oauth_bp.route("/authorize", methods=["POST"])  # type: ignore
@oauth.authorize_handler
def authorize() -> Union[bool, Tuple[Dict[str, str], int]]:
    """
    This method is used to authorize the client.
    :param username: username of the user
    :param password: password of the user
    :param client_id: client id of the client
    :return: True if the client is authorized else return error message"""
    data = request.get_json()
    user_name = data.get("username")
    password = data.get("password")
    if not user_name or not password:
        return {"message": "Invalid authentication!"}, 400
    client_id = data.get("client_id")
    if not client_id:
        return {"message": "Invalid client!"}, 400
    encrypted_password = encrypt_password(password)
    user = check_existing_user(user_name, encrypted_password)
    if not user or user.password != encrypted_password or not user.admin:
        return {"message": "Invalid authentication!"}, 400
    return True


@oauth_bp.route("/token", methods=["POST"])
@oauth.token_handler
def access_token() -> Dict[str, str]:
    """This method is used to generate access token
    :return: access token"""
    return {"message": "Token generated"}


@oauth_bp.route("/authorized", methods=["GET"])
def authorized() -> Dict[str, str | None]:
    """This method is used to check if the client is authorized
    :param code: code of the client
    :return: authorisation code"""
    code = request.args.get("code")
    return {"code": code}


@oauth_bp.route("/revoke", methods=["POST"])
@oauth.revoke_handler
def revoke_token() -> Dict[str, str]:
    """This method is used to revoke the access token
    :return: access token revoked message"""
    return {"message:": "Token revoked"}
