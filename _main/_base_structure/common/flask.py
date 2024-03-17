from flask import Flask


def flask_server() -> tuple[Flask | None, Exception | None]:
    try:
        return Flask(__name__), None
    except Exception as e:
        return None, e
