from domain.example import Example, ExampleDTO1


def new_example_dto1(example: Example) -> ExampleDTO1:
    return ExampleDTO1(
        id=example.id,
        username=example.username,
        created_at=example.get_created_at_str()
    )
