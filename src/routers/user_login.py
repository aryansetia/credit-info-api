from src.authentication.auth import authenticate_user, create_access_token
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from datetime import datetime, timedelta
from src.schemas.token import Token
from src.schemas.user_login import UserLogin
from src.authentication.auth import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


@router.post("/token", response_model=Token)
def login(user: UserLogin):
    if authenticate_user(user.username, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )
