from app.core.repositories.user_repository import UserRepository

class GetUserQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int):
        return self.repository.get_user_by_id(user_id)
