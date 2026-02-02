from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import RefreshToken, User
from app.schemas import UserCreate, Token
from app.core.security import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.auth.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User).filter(User.email == user_data.email).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # derive a username from the email local-part to satisfy NOT NULL constraint
    username = user_data.email.split("@", 1)[0]

    user = User(
        username=username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(
        user_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/refresh", response_model=Token)
def refresh_token(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )

    if not db_token or db_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reused or revoked",
        )

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # 🔥 ROTATION HAPPENS HERE
    db_token.revoked = True

    new_refresh_token = create_refresh_token(user.id)
    new_db_token = RefreshToken(
        token=new_refresh_token,
        user_id=user.id
    )

    db.add(new_db_token)
    db.commit()

    return {
        "access_token": create_access_token(user.id, user.role),
        "refresh_token": new_refresh_token,
    }

@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )

    if db_token:
        db_token.revoked = True
        db.commit()

    return {"message": "Logged out successfully"}

    # Note: With JWT, logout is typically handled client-side by discarding tokens.