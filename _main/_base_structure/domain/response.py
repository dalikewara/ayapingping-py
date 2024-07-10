from dataclasses import dataclass, field
from typing import List, Any


@dataclass(frozen=True)
class ResponseJSON:
    status: bool = False
    message: str = ''
    data: dict = field(default_factory=dict)
    error: List[str] = field(default_factory=list)


def new_response_json_success(data: Any = None) -> dict:
    if data is None:
        data = {}

    data = data.__dict__

    return ResponseJSON(
        status=True,
        message='success',
        data=data
    ).__dict__


def new_response_json_error(err: Exception = None) -> dict:
    if err is None:
        err = ValueError('error')

    return ResponseJSON(
        status=False,
        message='error',
        error=[err.args[0]]
    ).__dict__

