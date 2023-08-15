from pydantic import BaseModel


class JwtResponse(BaseModel):
    access_token: str
    refresh_key: str


class JwtReissueResponse(BaseModel):
    access_token: str
