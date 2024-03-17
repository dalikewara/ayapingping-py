from datetime import datetime
from mysql.connector.pooling import PooledMySQLConnection
from domain.example import Example, FindExampleByIDRepository


class FindExampleByIDMySQLConnector(FindExampleByIDRepository):

    def __init__(self, db: PooledMySQLConnection):
        self.db = db

    def exec(self, example_id: int) -> tuple[Example | None, Exception | None]:
        try:
            return Example(
                id=example_id,
                username='dalikewara',
                password='password',
                created_at=datetime.now()
            ), None
        except Exception as e:
            return None, e
