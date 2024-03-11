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

    def validate_username(self) -> Exception | None:
        return validate_username(self.username)


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
