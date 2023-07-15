import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_skeleton.schema.example import Example
from tests.repository.example.conftest import example_repository


@pytest.mark.describe("Test case for example repository")
class TestExampleRepository(object):
    @pytest.mark.asyncio
    async def test_save(
            self,
            session: AsyncSession,
            example_fixture: Example
    ):
        # then
        assert example_fixture.id is not None
        assert example_fixture.name == "test"

    @pytest.mark.asyncio
    async def test_find__by_id(
            self,
            session: AsyncSession,
            example_fixture: Example
    ):
        # when
        result = await example_repository.find_by_id(session, example_fixture.id)

        # then
        assert result == example_fixture
