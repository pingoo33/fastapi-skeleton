import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi_skeleton.common.error.exception import BadRequestException, UnauthorizedException, NotFoundException, \
    UnprocessableEntityException, ErrorCode, InternalServerException


def add_http_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(UnprocessableEntityException)
    async def unprocessable_entity_exception_handler(request: Request, exc: UnprocessableEntityException):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        details = exc.errors()
        message = [{"loc": error["loc"], "message": error["msg"], "type": error["type"]} for error in details]

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"code": ErrorCode.UNPROCESSABLE_ENTITY.value, "message": message}
        )

    @app.exception_handler(InternalServerException)
    async def internal_server_exception(request: Request, exc: InternalServerException):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(Exception)
    async def exception(request: Request, exc: Exception):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={
                                "code": ErrorCode.INTERNAL_SERVER_ERROR.value,
                                "message": traceback.format_exception_only(exc)
                            })
