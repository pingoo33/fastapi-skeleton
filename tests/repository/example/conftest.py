import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_skeleton.repository.example import ExampleRepository
from fastapi_skeleton.schema.example import Example

example_repository = ExampleRepository()


@pytest.fixture(autouse=True)
async def example_fixture(session: AsyncSession):
    example = Example(
        name="test"
    )

    example = await example_repository.save(session, example)
    yield example
    await session.rollback()
