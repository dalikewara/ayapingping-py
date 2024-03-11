from common.env import parse_env
from common.mysql_connector import connect_mysql_connector
from common.flask import flask_server
from features.example.repositories.findExampleByID.mysql_connector import FindExampleByIDMySQLConnector
from features.example.usecases.get_example.v1 import GetExampleV1
from features.example.delivery.handlers.example_get.v1_flask import ExampleGetV1Flask

# Parse env

env_cfg, err = parse_env()
if err is not None:
    # raise err
    print()

# Database connection

mysql_db, err = connect_mysql_connector(
    env_cfg.mysql_host,
    env_cfg.mysql_port,
    env_cfg.mysql_user,
    env_cfg.mysql_password,
    env_cfg.mysql_db_name
)
if err is not None:
    # raise err
    print()

# Server initialization

flask_svr, err = flask_server()
if err is not None:
    raise err

# Repositories

find_example_by_id_mysql_connector = FindExampleByIDMySQLConnector(mysql_db)

# Use cases

get_example_v1 = GetExampleV1(find_example_by_id_mysql_connector)

# Register handlers

ExampleGetV1Flask(flask_svr, get_example_v1).register_handler('GET', '/api/v1/example/get')

# Start & listen application

if __name__ == '__main__':
    flask_svr.run(port=env_cfg.get_rest_port_int(), debug=True)
