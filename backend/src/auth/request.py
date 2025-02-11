from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class OauthLoginRequest(BaseModel):
    provider: str
    oauth_token: str
