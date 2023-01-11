from datetime import timedelta
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas.user import UserSchema
from schemas.auth import UserLoginSchema, UserCreateSchema
from models.user import User

from utils.auth import *
from restaurant_crm.database import get_db
from restaurant_crm.config import settings


router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post("/register")
def register(
    payload: UserCreateSchema,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    user = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    hashed_password = hash_password(payload.password)
    del payload.password

    data = payload.dict()
    data["hashed_password"] = hashed_password

    db_user = User(**data)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = Authorize.create_access_token(
        subject=str(db_user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(db_user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
    )

    response = {
        "user": UserSchema.from_orm(db_user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return response


@router.post("/login")
def login(
    payload: UserLoginSchema,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):

    user = db.query(User).filter(User.phone_number == payload.phone_number).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Phone number or Password",
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)
    )

    return {
        "user": UserSchema.from_orm(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.get("/refresh")
def refresh_token(
    response: Response,
    request: Request,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh access token",
            )
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user belonging to this token no logger exist",
            )
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
        )
    except Exception as e:
        error = e.__class__.__name__
        if error == "MissingTokenError":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide refresh token",
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {
        "status": "success",
        "access_token": access_token,
    }


@router.get("/logout", status_code=status.HTTP_200_OK)
def logout(
    Authorize: AuthJWT = Depends(),
    request_user: str = Depends(require_user),
):
    Authorize.unset_jwt_cookies()

    return {"status": "success"}
