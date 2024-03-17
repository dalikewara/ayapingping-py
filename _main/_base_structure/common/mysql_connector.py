import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection


def connect_mysql_connector(host: str, port: str, user: str, password: str, db_name: str) -> tuple[PooledMySQLConnection | None, Exception | None]:
    try:
        connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=db_name)

        if connection.is_connected():
            return connection, None

        raise ValueError("can't connect to mysql database")

    except ValueError as e:
        return None, e

    except mysql.connector.Error as e:
        return None, e
