from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from common.time_now import time_now_utc
from common.validate_username import validate_username


@dataclass
class Example:
    id: int = 0
    username: str = ''
    password: str = ''
    created_at: datetime | None = None

    def set_created_at_now(self):
        self.created_at = time_now_utc()

    def get_created_at_str(self) -> str:
        if self.created_at is None:
            return ''

        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def validate_username(self) -> Exception | None:
        return validate_username(self.username)


@dataclass(frozen=True)
class ExampleDTO1:
    id: int = 0
    username: str = ''
    created_at: str = ''


def new_dto1(example: Example) -> ExampleDTO1:
    return ExampleDTO1(
        id=example.id,
        username=example.username,
        created_at=example.get_created_at_str()
    )


class ExampleRepository(ABC):

    @abstractmethod
    def find_by_id(self, example_id: int) -> tuple[Example | None, Exception | None]:
        raise NotImplementedError


class ExampleUseCase(ABC):

    @abstractmethod
    def get_detail(self, example_id: int) -> tuple[ExampleDTO1 | None, Exception | None]:
        raise NotImplementedError


class ExampleHttpService(ABC):

    @abstractmethod
    def example_detail(self, method: str, endpoint: str):
        raise NotImplementedError
