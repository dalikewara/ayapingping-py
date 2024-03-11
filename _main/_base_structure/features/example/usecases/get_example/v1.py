from domain.example import ExampleDTO1, GetExampleUseCase, FindExampleByIDRepository
from features.example.utility.example_dto import new_example_dto1


class GetExampleV1(GetExampleUseCase):

    def __init__(self, find_example_by_id: FindExampleByIDRepository):
        self.find_example_by_id = find_example_by_id

    def exec(self, example_id: int) -> tuple[ExampleDTO1 | None, Exception | None]:
        try:
            example, err = self.find_example_by_id.exec(example_id)
            if err is not None:
                return None, err

            return new_example_dto1(example), None
        except Exception as e:
            return None, e


