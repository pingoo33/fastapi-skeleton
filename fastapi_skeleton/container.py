from dependency_injector import containers, providers

from fastapi_skeleton import router
from fastapi_skeleton.common import util
from fastapi_skeleton.repository.example import ExampleRepository
from fastapi_skeleton.service.example import ExampleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[util, router])

    """ Repository """
    example_repository = providers.Singleton(ExampleRepository)

    """ Service """
    example_service = providers.Singleton(ExampleService,
                                          example_repository=example_repository)
