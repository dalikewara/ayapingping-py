from common.flask import flask_server
from features.example import usecase_v1 as example_usecase_v1, repository_mysql as example_repository_mysql, \
    http_service_flask as example_http_service_flask

# Http server initialization

flask_svr, err = flask_server()
if err is not None:
    raise err

# Repositories

example_repository_mysql = example_repository_mysql.RepositoryMySQL(db=None)

# Use cases

example_usecase_v1 = example_usecase_v1.UseCaseV1(example_repository=example_repository_mysql)

# Services

example_http_service_flask = example_http_service_flask.HttpServiceFlask(client=flask_svr, example_usecase=example_usecase_v1)

# Service handlers

example_http_service_flask.example_detail(method="GET", endpoint="/example")

# Start & listen application

if __name__ == '__main__':
    flask_svr.run(port=8080, debug=True)
