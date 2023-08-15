from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from fastapi_skeleton.container import Container
from fastapi_skeleton.model.request.example import ExampleRequest
from fastapi_skeleton.model.response.example import ExampleResponse
from fastapi_skeleton.service.example import ExampleService

router = APIRouter()


@cbv(router)
class ExampleRouter:
    @inject
    def __init__(self,
                 example_service: ExampleService = Depends(Provide[Container.example_service])):
        self.example_service = example_service

    @router.get('/{example_id}', response_model=ExampleResponse)
    async def get_name(self,
                       example_id: int):
        return await self.example_service.find_by_id(example_id)

    @router.post('/', response_model=ExampleResponse)
    async def upload(self,
                     req: ExampleRequest):
        return await self.example_service.save(req)
