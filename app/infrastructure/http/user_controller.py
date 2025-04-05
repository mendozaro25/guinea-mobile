from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.use_cases.user_use_cases import UserUseCases
from app.infrastructure.database.config import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.http.schemas import ListResponse, UserCreate, Response, UserResponse
from app.core.utils import verify_token
from fastapi.security import OAuth2PasswordBearer
from app.config import API_PREFIX

router = APIRouter(prefix=f"{API_PREFIX}/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_use_cases(db: Session = Depends(get_db)) -> UserUseCases:
    user_repo = UserRepositoryImpl(db)
    return UserUseCases(user_repo=user_repo)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = verify_token(token)
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"{str(e)}")

@router.post("/register", response_model=Response)
async def register_user(
    user: UserCreate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: str = Depends(get_current_user)  # Verificación de token aquí
):
    try:
        existing_user = use_cases.get_user_by_username(username=user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        new_user = use_cases.create_user(username=user.username, password=user.password)
        user_response = UserResponse(id=new_user.id, username=new_user.username)
        return Response(id=new_user.id, data=user_response, message="User registered successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.get("/{user_id}", response_model=Response)
def read_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: str = Depends(get_current_user)  # Verificación de token aquí
):
    user = use_cases.get_user(user_id=user_id)
    if user is None:
        return Response(id=0, data=None, message="User not found")
    user_response = UserResponse(id=user.id, username=user.username, password=user.password)
    return Response(id=1, data=user_response, message="User found")

@router.get("/list", response_model=ListResponse)
def list_users(
    skip: int = 0,
    limit: int = 10,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: str = Depends(get_current_user)  # Verificación de token aquí
):
    users = use_cases.list_users(skip=skip, limit=limit)
    user_responses = [UserResponse(id=user.id, username=user.username) for user in users]
    return ListResponse(id=1, data=user_responses, message="Users retrieved successfully")
