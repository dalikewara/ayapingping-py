from domain.example import Example, ExampleRepository


class RepositoryMySQL(ExampleRepository):

    def __init__(self, db: None):
        self.db = db

    def find_by_id(self, example_id: int) -> tuple[Example | None, Exception | None]:
        try:
            example = Example(
                id=example_id,
                username='dalikewara',
                password='admin123'
            )

            example.set_created_at_now()

            return example, None
        except Exception as e:
            return None, e
