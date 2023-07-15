from pydantic import BaseModel

from fastapi_skeleton.schema.example import Example


class ExampleResponse(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_entity(entity: Example):
        return ExampleResponse(
            id=entity.id,
            name=entity.name
        )
