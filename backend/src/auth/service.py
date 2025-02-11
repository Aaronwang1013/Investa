from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from src.auth.schema import TokenResponse
from src.dependencies import password_context
from src.user.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
import httpx


class AuthService:
    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int = 30
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    # @staticmethod
    # def hash_password(password: str) -> str:
    #     return password_context.hash(password)
    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
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

    async def authenticate_user(self, session: AsyncSession, email: str, password: str):
        user = await UserService.get_user_by_email(session, email)
        if not user or not self._verify_password(password, user.password):
            return False
        else:
            return user

    async def oauth_login(self, provider: str, session: AsyncSession, oauth_token: str):
        if provider == "google":
            user_info = await self.verify_google_token(oauth_token)
        elif provider == "facebook":
            pass

        email = user_info.get("email")
        name = user_info.get("name", "")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to retrieve user information from provider",
            )

        user = await UserService.get_user_by_email(session, email)
        if not user:
            user = await UserService.create_oauth_user(
                email=email, username=name, session=session
            )
        access_token = self.create_access_token({"sub": user.email})
        return TokenResponse(access_token=access_token, token_type="bearer")

    async def verify_google_token(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
                )
            return response.json()
