from abc import ABC, abstractmethod
from typing import Dict

import requests
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request

from fastapi_skeleton.common.error.exception import InternalServerException, ErrorCode
from fastapi_skeleton.config.env import config
from fastapi_skeleton.common.enum import OAuthProvider
from fastapi_skeleton.model.oauth import OAuthUserInfo

GOOGLE_CLIENT_ID = config.get("security.oauth.google.client-id")
KAKAO_CLIENT_ID = config.get("security.oauth.kakao.client-id")
KAKAO_CLIENT_SECRET = config.get("security.oauth.kakao.client-secret")
KAKAO_REDIRECT_URI = config.get("security.oauth.kakao.redirect-uri")


class OAuthUserProvider(ABC):
    @abstractmethod
    async def get_user_info(self, token: str):
        pass


class GoogleOAuthUserProvider(OAuthUserProvider):
    async def get_user_info(self, token: str):
        try:
            id_token = verify_oauth2_token(token, Request(), GOOGLE_CLIENT_ID)

            if id_token is None:
                raise InternalServerException(
                    ErrorCode.INTERNAL_SERVER_ERROR,
                    "Failed to google login because of not existing id token"
                )

            return OAuthUserInfo(oauth_id=id_token['sub'], email=id_token['email'])
        except Exception as e:
            raise InternalServerException(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "Failed to get google user information"
            ) from e


class KakaoOAuthUserProvider(OAuthUserProvider):
    async def get_user_info(self, token: str):
        try:
            access_token = await self.get_access_token(token)

            response = requests.get(
                url="https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": "Bearer " + access_token,
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                timeout=5
            )

            response.raise_for_status()

            user = response.json()
            return OAuthUserInfo(oauth_id=user['id'], email=user['kakao_account']['email'])
        except Exception as e:
            raise InternalServerException(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "Failed to get kakao user information"
            ) from e

    async def get_access_token(self, code: str):
        try:
            response = requests.post(
                url="https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": KAKAO_CLIENT_ID,
                    "client_secret": KAKAO_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": KAKAO_REDIRECT_URI
                }
            )

            response.raise_for_status()

            return response.json()['access_token']
        except Exception as e:
            raise InternalServerException(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "Failed to get kakao access token"
            ) from e


class OAuthUserProviderSupplier:
    def __init__(self):
        self.supplier: Dict[OAuthProvider, OAuthUserProvider] = {
            OAuthProvider.GOOGLE: GoogleOAuthUserProvider(),
            OAuthProvider.KAKAO: KakaoOAuthUserProvider()
        }

    def get_provider(self, provider: OAuthProvider):
        try:
            return self.supplier.get(provider)
        except Exception as e:
            raise InternalServerException(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "Failed to get provider because of incorrect provider name"
            ) from e

    async def get_user_info(self, provider: OAuthProvider, token: str):
        provider = self.get_provider(provider)

        return await provider.get_user_info(token)
