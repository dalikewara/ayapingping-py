import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Env:
    app_env: str = os.getenv('APP_ENV', 'development')
    rest_port: str = os.getenv('REST_PORT', '8080')
    mysql_host: str = os.getenv('MYSQL_HOST', 'localhost')
    mysql_port: str = os.getenv('MYSQL_PORT', '3306')
    mysql_user: str = os.getenv('MYSQL_USER', '')
    mysql_password: str = os.getenv('MYSQL_PASSWORD', '')
    mysql_db_name: str = os.getenv('MYSQL_DB_NAME', '')

    def get_rest_port_int(self) -> int:
        return int(self.rest_port)


def parse_env() -> tuple[Env | None, Exception | None]:
    try:
        load_dotenv()

        return Env(), None
    except Exception as e:
        return None, e
