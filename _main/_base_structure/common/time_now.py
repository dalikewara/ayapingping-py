from datetime import datetime


def time_now_utc() -> datetime:
    return datetime.utcnow()
