import os
from datetime import datetime, timedelta

from flask_oauthlib.provider import OAuth2Provider

from src.models.document import Client, Grant, Token

oauth = OAuth2Provider()


@oauth.grantgetter
def load_grant(client_id, code):
    """Load grant for oauth
    :param client_id: client id
    :param code: code
    :return: grant"""
    return Grant.objects(client_id=client_id, code=code).first()  # type: ignore


@oauth.grantsetter
def save_grant(client_id, code, request):
    """Save grant for oauth
    :param client_id: client id
    :param code: code
    :param request: request
    :return: grant"""
    expires = datetime.utcnow() + timedelta(
        seconds=int(os.getenv("OAUTH2_TOKEN_EXPIRY", "3600"))
    )
    grant = Grant(
        client_id=client_id,
        code=code["code"],
        scope=request.scopes,
        user=request.user,
        expires=expires,
    )
    grant.save()
    return grant


@oauth.clientgetter
def load_client(client_id):
    """Load client for oauth
    :param client_id: client id
    :return: client"""
    return Client.objects(client_id=client_id).first()  # type: ignore


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    """Load token for oauth
    :param access_token: access token
    :param refresh_token: refresh token
    :return: token"""
    if access_token:
        return Token.objects(access_token=access_token).first()  # type: ignore
    elif refresh_token:
        return Token.objects(refresh_token=refresh_token).first()  # type: ignore


@oauth.tokensetter
def save_token(token, request):
    """Save token for oauth
    :param token: token
    :param request: request
    :return: token"""
    toks = Token.objects(client_id=request.client.client_id)  # type: ignore
    for t in toks:
        t.delete()
    expires_in = token.get("expires_in")
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    token = Token(
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        scope=" ".join(request.scopes),
        expires=expires,
        client_id=request.client.client_id,
        user=request.user,
    )
    token.save()
    return token
