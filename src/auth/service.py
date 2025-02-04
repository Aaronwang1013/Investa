from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from src.auth.request import LoginRequest
from src.auth.schema import TokenResponse
from src.dependencies import password_context
from src.user.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings


class AuthService:
    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int = 30
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    @staticmethod
    def hash_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, data: dict, expire_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expire_delta or timedelta(minutes=self.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:
        """
        decode jwt token
        param: token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authe nticate": "Bearer"},
            )

    async def login(
        self, session: AsyncSession, login_data: LoginRequest
    ) -> TokenResponse:
        user = await UserService.get_user_by_email(session, login_data.email)
        if not user or not self.verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        token = self.create_access_token({"sub": user.email})
        return TokenResponse(access_token=token, token_type="bearer")

    async def authenticate_user(self, session: AsyncSession, email: str, password: str):
        user = await UserService.get_user_by_email(session, email)
        if not user or not self.verify_password(password, user.password):
            return False
        else:
            return user
