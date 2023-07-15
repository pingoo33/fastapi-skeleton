import pytest

from fastapi_skeleton.model.request.example import ExampleRequest
from fastapi_skeleton.model.response.example import ExampleResponse
from fastapi_skeleton.schema.example import Example
from fastapi_skeleton.service.example import ExampleService


@pytest.mark.describe("Test case for save example")
class TestSaveExample(object):
    @pytest.fixture
    async def example_request(self):
        yield ExampleRequest(
            name="test"
        )

    @pytest.mark.asyncio
    @pytest.mark.it("Success cases for saving example")
    async def test_save(
            self,
            mock_repo: dict,
            example_service: ExampleService,
            example_fixture: Example,
            example_request: ExampleRequest
    ):
        # given
        mock_repo["example"].save.side_effect = [example_fixture]

        # when
        result = await example_service.save(req=example_request)

        # then
        assert result == ExampleResponse.from_entity(example_fixture)
