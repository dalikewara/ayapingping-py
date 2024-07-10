from domain.example import ExampleDTO1, ExampleUseCase, ExampleRepository
from domain.example import new_dto1


class UseCaseV1(ExampleUseCase):

    def __init__(self, example_repository: ExampleRepository):
        self.example_repository = example_repository

    def get_detail(self, example_id: int) -> tuple[ExampleDTO1 | None, Exception | None]:
        try:
            example, err = self.example_repository.find_by_id(example_id)
            if err is not None:
                return None, err

            return new_dto1(example), None
        except Exception as e:
            return None, e
