from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_skeleton.common.enum import OAuthProvider
from fastapi_skeleton.common.error.exception import UnauthorizedException, ErrorCode
from fastapi_skeleton.common.util.jwt import create_access_token, create_refresh_key
from fastapi_skeleton.common.util.transaction import transactional
from fastapi_skeleton.model.request.auth import SignInRequest, SignUpRequest, Subject, SocialSignInRequest, \
    SocialSignUpRequest
from fastapi_skeleton.model.response.auth import JwtResponse, JwtReissueResponse
from fastapi_skeleton.repository.user import UserRepository
from fastapi_skeleton.schema.user import User
from fastapi_skeleton.service.oauth import OAuthUserProviderSupplier


class UserService:
    def __init__(self,
                 user_repository: UserRepository,
                 oauth_user_provider_supplier: OAuthUserProviderSupplier):
        self.user_repository = user_repository
        self.oauth_user_provider_supplier = oauth_user_provider_supplier

    @transactional(read_only=True)
    async def sign_in(self, session: AsyncSession, req: SignInRequest):
        user = await self.user_repository.find_by_user_id(session, req.user_id)
        if user is None:
            raise UnauthorizedException(
                ErrorCode.USER_DOES_NOT_EXIST,
                "Not existing user account."
            )

        if not user.check_password(req.password):
            raise UnauthorizedException(
                ErrorCode.INVALID_PASSWORD,
                "Invalid password."
            )

        return JwtResponse(
            access_token=create_access_token(user.id),
            refresh_key=create_refresh_key(user.id)
        )

    @transactional(read_only=True)
    async def social_sign_in(self, session: AsyncSession, provider: OAuthProvider, req: SocialSignInRequest):
        oauth_user = await self.oauth_user_provider_supplier.get_user_info(provider, req.id_token)

        user = await self.user_repository.find_by_oauth_id(session, oauth_user.oauth_id)
        if user is None:
            raise UnauthorizedException(
                ErrorCode.USER_DOES_NOT_EXIST,
                "Not existing user account."
            )

        return JwtResponse(
            access_token=create_access_token(user.id),
            refresh_key=create_refresh_key(user.id)
        )

    @transactional()
    async def sign_up(self, session: AsyncSession, req: SignUpRequest):
        user = await self.user_repository.save(session, User(user_id=req.user_id, password=req.password))

        return JwtResponse(
            access_token=create_access_token(user.id),
            refresh_key=create_refresh_key(user.id)
        )

    @transactional()
    async def social_sign_up(self, session: AsyncSession, provider: OAuthProvider, req: SocialSignUpRequest):
        oauth_user = await self.oauth_user_provider_supplier.get_user_info(provider, req.id_token)

        user = await self.user_repository.save(session, User(user_id=req.user_id, password=req.password, oauth_id=oauth_user.oauth_id))

        return JwtResponse(
            access_token=create_access_token(user.id),
            refresh_key=create_refresh_key(user.id)
        )

    async def reissue(self, subject: Subject):
        return JwtReissueResponse(
            access_token=create_access_token(subject.id)
        )
