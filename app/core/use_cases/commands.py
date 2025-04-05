from app.core.entities.user import User
from app.core.repositories.user_repository import UserRepository

class RegisterUserCommand:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user: User):
        return self.repository.add_user(user)
