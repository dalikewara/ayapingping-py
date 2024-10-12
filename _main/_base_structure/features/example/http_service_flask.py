from flask import Flask, jsonify
from domain.example import ExampleHttpService, ExampleUseCase
from common.response import new_response_json_success, new_response_json_error


class HttpServiceFlask(ExampleHttpService):

    def __init__(self, client: Flask, example_usecase: ExampleUseCase):
        self.client = client
        self.example_usecase = example_usecase

    def example_detail(self, method: str, endpoint: str):
        @self.client.route(rule=endpoint, methods=[method])
        def example_detail_route_handler():
            try:
                result, err = self.example_usecase.get_detail(1)
                if err is not None:
                    return jsonify(new_response_json_error(err))

                return jsonify(new_response_json_success(result))
            except Exception as e:
                return jsonify(new_response_json_error(e))
