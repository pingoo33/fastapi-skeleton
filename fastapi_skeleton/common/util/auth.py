from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi_skeleton.common.error.exception import UnauthorizedException, ErrorCode
from fastapi_skeleton.common.util.database import db
from fastapi_skeleton.common.util.jwt import resolve_access_token
from fastapi_skeleton.common.util.redis import find_user_id_by_refresh_key, delete_refresh_key, save_refresh_key
from fastapi_skeleton.container import Container
from fastapi_skeleton.model.request.auth import Subject
from fastapi_skeleton.repository.user import UserRepository


@inject
async def __find_user_by_id(
        user_id: int,
        user_repository: UserRepository = Depends(Provide[Container.user_repository])
):
    async with db.async_session_maker() as session:
        user = await user_repository.find_by_id(session, user_id)
        if user is None:
            raise UnauthorizedException(
                ErrorCode.USER_DOES_NOT_EXIST,
                "Not existing user account."
            )
        return user


async def get_subject(token: HTTPAuthorizationCredentials):
    token = token.dict().get("credentials")
    payload = resolve_access_token(token)

    user = await __find_user_by_id(user_id=payload.get("sub"))

    return Subject(
        id=user.id,
        user_id=user.user_id
    )


async def get_refresh(refresh_key: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    refresh_key = refresh_key.dict().get("credentials")

    user_id = find_user_id_by_refresh_key(refresh_key)

    if user_id is None:
        raise UnauthorizedException(
            ErrorCode.EXPIRED_JWT,
            "refresh key is expired."
        )

    user = await __find_user_by_id(user_id=user_id)

    delete_refresh_key(refresh_key=refresh_key)
    save_refresh_key(refresh_key=refresh_key, user_id=user_id)

    return Subject(
        id=user.id,
        user_id=user.user_id
    )


async def get_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    return await get_subject(token)


RequestUser = Annotated[Subject, Depends(get_user)]
ReissuedUser = Annotated[Subject, Depends(get_refresh)]
