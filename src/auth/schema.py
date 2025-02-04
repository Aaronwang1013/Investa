from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str
    password: str

class UserInDB(UserBase):
    id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True