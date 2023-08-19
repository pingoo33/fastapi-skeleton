from pydantic import BaseModel


class OAuthUserInfo(BaseModel):
    oauth_id: str
    email: str | None
