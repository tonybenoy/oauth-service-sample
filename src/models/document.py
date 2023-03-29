import os

import mongoengine as me


class User(me.Document):
    username = me.StringField()
    password = me.StringField()
    admin = me.BooleanField(default=False)


class Client(me.Document):
    client_id = me.StringField(unique=True)
    client_secret = me.StringField()
    name = me.StringField(unique=True)
    redirect_uri = me.StringField()
    default_scopes = me.ListField(me.StringField(), default=["kyc_status"])

    @property
    def client_type(self):
        return "public"

    @property
    def default_redirect_uri(self):
        return self.redirect_uri or f"{os.getenv('APP_URL')}/oauth/authorized"

    @property
    def redirect_uris(self):
        return [self.redirect_uri] or [f"{os.getenv('APP_URL')}/oauth/authorized"]


class Token(me.Document):
    access_token = me.StringField(unique=True)
    refresh_token = me.StringField(unique=True)
    expires = me.DateTimeField()
    scope = me.StringField()
    user = me.StringField()
    client_id = me.StringField()


class Grant(me.Document):
    code = me.StringField()
    expires = me.DateTimeField()
    scope = me.ListField(me.StringField())
    client_id = me.StringField()
    user = me.StringField()
    redirect_uri = me.StringField()


class Kyc(me.Document):
    user = me.StringField()
    kyc_id = me.StringField()
    kyc_status = me.BooleanField(default=False)
    kyc_type = me.StringField()
    kyc_data = me.DictField()
