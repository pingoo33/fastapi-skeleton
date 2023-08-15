from pydantic import BaseModel


class Subject(BaseModel):
    id: int
    user_id: str


class SignInRequest(BaseModel):
    user_id: str
    password: str


class SignUpRequest(BaseModel):
    user_id: str
    password: str
