from typing import Optional, ClassVar
from passlib.context import CryptContext
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None

    pwd_context: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def set_password(self, password: str) -> None:
        self.password = self._hash_password(password)
    
    def verify_password(self, password: str) -> bool:
        if not self.password:
            return False
        return self.pwd_context.verify(password, self.password)
