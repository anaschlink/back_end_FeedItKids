from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import usuario_schema as schemas
from src.repositories import usuario_repositories as repository
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.database.database import get_db



router = APIRouter()  



db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = repository.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = repository.create_acess_token(user.email, user.id_usuario, timedelta(minutes=20))
    return {"acess_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.TokenData)
async def read_users_me(current_user: schemas.TokenData = Depends(repository.get_current_user)):
    return current_user