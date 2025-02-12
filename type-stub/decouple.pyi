from typing import TypeVar

T = TypeVar('T')

class Config:
    def __call__(
        self,
        option: str,
        default: T,
        cast: type[T],
    ) -> T: ...

def config(
    option: str,
    default: T | None = None,
    cast: type[T] = str,
) -> T: ...
