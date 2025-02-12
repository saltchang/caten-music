from dataclasses import dataclass
from typing import Protocol

from core.model.user import User
from core.type import IDType


@dataclass
class UserRepository(Protocol):
    def create(self, user: User) -> User: ...

    def get_by_id(self, user_id: IDType) -> User | None: ...

    def update(self, user: User) -> User: ...

    def delete(self, user: User) -> None: ...
