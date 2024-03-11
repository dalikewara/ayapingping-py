from typing import Any
from domain.example import ExampleJSONPresenter


def json_presenter_ok(data: Any = None) -> dict:
    if data is None:
        data = {}

    data = data.__dict__

    return ExampleJSONPresenter(
        code='00',
        message='ok',
        data=data
    ).__dict__


def json_presenter_not_ok(error: Exception = None) -> dict:
    if error is None:
        error = ValueError('error')

    return ExampleJSONPresenter(
        code='-1',
        message='error',
        error=[error.args[0]]
    ).__dict__
