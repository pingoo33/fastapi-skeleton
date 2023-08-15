from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from fastapi_skeleton.common.util.auth import ReissuedUser
from fastapi_skeleton.container import Container
from fastapi_skeleton.model.request.auth import SignInRequest, SignUpRequest
from fastapi_skeleton.model.response.auth import JwtResponse, JwtReissueResponse
from fastapi_skeleton.service.user import UserService

router = APIRouter()


@cbv(router)
class AuthRouter:
    @inject
    def __init__(self,
                 user_service: UserService = Depends(Provide[Container.user_service])):
        self.user_service = user_service

    @router.post('/sign-in', response_model=JwtResponse)
    async def sign_in(self, req: SignInRequest):
        return await self.user_service.sign_in(req)

    @router.post('/sign-up', response_model=JwtResponse)
    async def sign_up(self, req: SignUpRequest):
        return await self.user_service.sign_up(req)

    @router.post('/reissue', response_model=JwtReissueResponse)
    async def reissue_token(self, user: ReissuedUser):
        return await self.user_service.reissue(user)
