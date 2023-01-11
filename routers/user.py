from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi_jwt_auth import AuthJWT

from models.user import User
from schemas.user import *

from e_commerce.database import get_db
from utils.auth import hash_password, require_user

router = APIRouter()


@router.delete("/{id}")
def delete_user(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    request_user: str = Depends(require_user),
):
    obj = db.query(User).filter(User.id == id)
    if not obj.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="object not found",
        )
    if obj.first().id != uuid.UUID(request_user.id) or not request_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    obj.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=UserSchema)
def update_user(
    id: uuid.UUID,
    payload: UserUpdateSchema,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    request_user: str = Depends(require_user),
):
    obj = db.query(User).filter(User.id == id)

    if not obj.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="object not found",
        )
    if obj.first().id != uuid.UUID(request_user.id) or not request_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )

    payload = payload.dict(exclude_none=True)

    if "password" in payload:
        hashed_password = hash_password(payload["password"])
        payload["hashed_password"] = hashed_password
        del payload["password"]

    obj.update(payload)
    db.commit()
    db.refresh(obj.first())

    return obj.first()


@router.get("/{id}", response_model=UserSchema)
def get_user(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    request_user: str = Depends(require_user),
):
    res = db.query(User).filter(User.id == id).first()

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="object not found",
        )

    return res


@router.get("/", response_model=list[UserSchema])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    request_user: str = Depends(require_user),
):
    res = db.query(User).offset(skip).limit(limit).all()
    return res
