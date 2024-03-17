from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List
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

    def to_dto1(self) -> 'ExampleDTO1':
        return ExampleDTO1(
            id=self.id,
            username=self.username,
            created_at=self.get_created_at_str()
        )


@dataclass(frozen=True)
class ExampleDTO1:
    id: int = 0
    username: str = ''
    created_at: str = ''


@dataclass(frozen=True)
class ExampleJSONPresenter:
    code: str = ''
    message: str = ''
    data: dict = field(default_factory=dict)
    error: List[str] = field(default_factory=list)


class FindExampleByIDRepository(ABC):

    @abstractmethod
    def exec(self, example_id: int) -> tuple[Example | None, Exception | None]:
        raise NotImplementedError


class GetExampleUseCase(ABC):

    @abstractmethod
    def exec(self, example_id: int) -> tuple[ExampleDTO1 | None, Exception | None]:
        raise NotImplementedError


class ExampleDelivery(ABC):

    @abstractmethod
    def register_handler(self, method: str, endpoint: str):
        raise NotImplementedError
