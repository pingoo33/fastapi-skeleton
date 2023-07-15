import pytest

from fastapi_skeleton.common.error.exception import NotFoundException, ErrorCode
from fastapi_skeleton.schema.example import Example
from fastapi_skeleton.service.example import ExampleService


@pytest.mark.describe("Test case for find example by id")
class TestExampleFindById(object):
    @pytest.mark.asyncio
    @pytest.mark.it("Success case")
    async def test_find_example_by_id(
            self,
            mock_repo: dict,
            example_service: ExampleService,
            example_fixture: Example
    ):
        # given
        mock_repo["example"].find_by_id.side_effect = [example_fixture]

        # when
        result = await example_service.find_by_id(example_fixture.id)

        # then
        assert result.id == 1
        assert result.name == "test"

    @pytest.mark.asyncio
    @pytest.mark.it("Fail case: example is not found")
    async def test_find_example_by_id_not_existing_example(
            self,
            mock_repo: dict,
            example_service: ExampleService,
            example_fixture: Example
    ):
        # given
        mock_repo["example"].find_by_id.side_effect = [None]

        with pytest.raises(NotFoundException) as exception:
            # when
            await example_service.find_by_id(example_fixture.id)

        # then
        assert exception.value.code == ErrorCode.DATA_DOES_NOT_EXIST
