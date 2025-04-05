from typing import List, Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.core.entities.user import User
from app.infrastructure.database.models import UserDBModel
from app.core.utils import verify_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserDBModel(username=user.username, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User(id=db_user.id, username=db_user.username, password=db_user.password)

    def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(UserDBModel).filter(UserDBModel.id == user_id).first()
        if db_user:
            return User(id=db_user.id, username=db_user.username, password=db_user.password)
        return None

    def list(self, skip: int = 0, limit: int = 10) -> List[User]:
        db_users = self.db.query(UserDBModel).offset(skip).limit(limit).all()
        return [User(id=user.id, username=user.username) for user in db_users]

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            db_user = self.db.query(UserDBModel).filter(UserDBModel.username == username).one()
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.password)
        except NoResultFound:
            return None

    def verify_password(self, username: str, password: str) -> bool:
        try:
            db_user = self.db.query(UserDBModel).filter(UserDBModel.username == username).first()
            
            if db_user and verify_password_hash(password, db_user.password):
                return True
        except Exception as e:
            print(f"Error verificando contraseña: {e}")
            
        return False
