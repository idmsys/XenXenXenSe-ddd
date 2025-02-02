import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .settings import Settings


class Security:
    fastapi_basic = HTTPBasic()

    @classmethod
    def load_authentication_config(cls):
        return Settings.get_authentication_config()

    @classmethod
    def load_authentication_type(cls):
        config = cls.load_authentication_config()

        if config is None:
            return None

        return str(config["type"]).lower()

    @classmethod
    def load_accounts(cls):
        config = cls.load_authentication_config()

        accounts = []
        if config is not None:
            accounts = config["accounts"]

        return accounts

    @classmethod
    def get_authentication_dependencies(cls):
        dependencies = []

        if cls.load_authentication_type() == "basic":
            dependencies.append(Depends(cls.authenticate_basic))

        return dependencies

    @classmethod
    def authenticate_basic(
        cls, credentials: HTTPBasicCredentials = Depends(fastapi_basic)
    ):
        if cls.load_authentication_type() == "basic":
            match_found = False

            username_bytes = credentials.username.encode("utf8")
            password_bytes = credentials.password.encode("utf8")

            for account in cls.load_accounts():
                account_username_bytes = account["username"].encode("utf8")
                account_password_bytes = account["password"].encode("utf8")

                username_match = secrets.compare_digest(
                    username_bytes, account_username_bytes
                )
                password_match = secrets.compare_digest(
                    password_bytes, account_password_bytes
                )
                if username_match and password_match:
                    match_found = True

            if not match_found:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"type": "unauthorized"},
                    headers={"WWW-Authenticate": "Basic"},
                )
