import base64
from typing import List
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from models.user import User

from restaurant_crm.database import get_db
from restaurant_crm.config import settings


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_access_cookie_key: str = "access_token"
    authjwt_refresh_cookie_key: str = "refresh_token"
    authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode("utf-8")
    authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode(
        "utf-8"
    )


@AuthJWT.load_config
def get_config():
    return Settings()


class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass


def require_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise UserNotFound("User no longer exist")

        if not user.is_active:
            raise NotVerified("You are not verified")

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == "MissingTokenError":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in"
            )
        if error == "UserNotFound":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exist"
            )
        if error == "NotVerified":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your account",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or has expired",
        )
    return user


def hash_password(password: str):
    return PWD_CONTEXT.hash(password)


def verify_password(password: str, hashed_password: str):
    return PWD_CONTEXT.verify(password, hashed_password)
