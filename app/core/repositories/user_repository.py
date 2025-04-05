from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.database.models import UserDBModel
from app.core.entities.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserDBModel(username=user.username, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(UserDBModel).filter(UserDBModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    def list(self, skip: int = 0, limit: int = 10) -> List[User]:
        db_users = self.db.query(UserDBModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_user) for db_user in db_users]

    def _to_entity(self, db_user: UserDBModel) -> User:
        return User(id=db_user.id, username=db_user.username, password=db_user.password)
