from flask import Flask, jsonify
from domain.example import ExampleDelivery
from domain.example import GetExampleUseCase
from features.example.utility.json_presenter import json_presenter_ok, json_presenter_not_ok
from features.example.delivery.middlewares.authorization.v1_flask import authorization_v1_flask


class ExampleGetV1Flask(ExampleDelivery):
    def __init__(self, client: Flask, get_example: GetExampleUseCase):
        self.client = client
        self.get_example = get_example

    def register_handler(self, method: str, endpoint: str):
        @self.client.route(rule=endpoint, methods=[method])
        @authorization_v1_flask
        def route_handler():
            return self.handler()

    def handler(self):
        try:
            dto, err = self.get_example.exec(1)
            if err is not None:
                return jsonify(json_presenter_not_ok(err))

            return jsonify(json_presenter_ok(dto))
        except Exception as e:
            return jsonify(json_presenter_not_ok(e))
