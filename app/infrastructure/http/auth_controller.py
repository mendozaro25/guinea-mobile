from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.use_cases.user_use_cases import UserUseCases
from app.infrastructure.database.config import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.http.schemas import TokenResponse
from app.core.utils import create_access_token
from app.config import API_PREFIX

router = APIRouter(prefix=f"{API_PREFIX}/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_use_cases(db: Session = Depends(get_db)) -> UserUseCases:
    return UserUseCases(user_repo=UserRepositoryImpl(db))

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), use_cases: UserUseCases = Depends(get_user_use_cases)):
    authenticated_user = use_cases.authenticate_user(username=form_data.username, password=form_data.password)
    
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return TokenResponse(access_token=access_token, token_type="bearer")
