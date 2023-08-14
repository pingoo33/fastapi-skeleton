from enum import Enum


class ErrorCode(Enum):
    # 400 Bad Request
    ROW_ALREADY_EXIST = 40000

    # 401 Unauthorized Error
    NOT_ACCESSIBLE = 40100
    USER_DOES_NOT_EXIST = 40101
    INVALID_JWT = 40102
    EXPIRED_JWT = 40103

    # 404 Not Found Error
    DATA_DOES_NOT_EXIST = 40400

    # 422
    UNPROCESSABLE_ENTITY = 42200

    # 500 Internal Server Error
    INTERNAL_SERVER_ERROR = 50000


class BaseRuntimeException(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message


class BadRequestException(BaseRuntimeException):
    ...


class UnauthorizedException(BaseRuntimeException):
    ...


class NotFoundException(BaseRuntimeException):
    ...


class UnprocessableEntityException(BaseRuntimeException):
    ...


class InternalServerException(BaseRuntimeException):
    ...
