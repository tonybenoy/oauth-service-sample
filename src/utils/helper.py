from hashlib import md5

from src.models.document import Client, User


def encrypt_password(password):
    """Encrypt password using sha256 algorithm
    :param password: password
    :return: encrypted password"""
    return md5(password.encode()).hexdigest()


def check_existing_user(username, password=None):
    """Check if user already exists
    :param username: username
    :param password: password
    :return: user"""
    if password:
        return User.objects(  # type: ignore
            username=username, password=password
        ).first()
    return User.objects(username=username).first()  # type: ignore


def check_existing_client(client_id):
    """Check if client already exists
    :param client_id: client id
    :return: client"""
    return Client.objects(client_id=client_id).first()  # type: ignore
