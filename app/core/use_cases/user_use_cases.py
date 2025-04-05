from typing import List, Optional
from app.core.entities.user import User
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.core.utils import hash_password, verify_password_hash

class UserUseCases:
    def __init__(self, user_repo: UserRepositoryImpl):
        self.user_repo = user_repo

    def create_user(self, username: str, password: str) -> User:
        password = hash_password(password)
        user = User(username=username, password=password)
        return self.user_repo.create(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return self.user_repo.list(skip=skip, limit=limit)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.get_by_username(username)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        return self.user_repo.get_by_username(username) if self.user_repo.verify_password(username, password) else None
