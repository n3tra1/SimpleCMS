"""User tortoise and pydantic models"""
import bcrypt as bcrypt
from pydantic import Field
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from api import access_security
from models import MainModelMixin


class User(MainModelMixin):
    login = fields.CharField(64, unique=True)
    secret = fields.CharField(60)

    class Meta:
        table = "user"

    def __init__(self, login: str, password: str):
        super().__init__()
        self.login = login
        self.secret = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.secret.encode())

    def make_access_token(self):
        subject = {"login": self.login, "user_id": self.id.hex}
        return {"access_token": access_security.create_access_token(subject)}


CredentialsSchemaMixin = pydantic_model_creator(
    User,
    include=("login",),
)


class CredentialsSchema(CredentialsSchemaMixin):
    password: str = Field(..., example="super+password")
