from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import AuthService
from src.database import get_db
from src.config import settings
import httpx


router = APIRouter()

auth_service = AuthService(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    grant_type: str = Form(default="password"),
    provider: str = Form(None),
    oauth_token: str = Form(None),
    db: AsyncSession = Depends(get_db),
):
    if grant_type == "password":
        user = await auth_service.authenticate_user(
            db, form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth_service.create_access_token({"sub": user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        }
    elif grant_type == "oauth":
        if not provider or not oauth_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="provider and oauth_token are required",
            )
        token_response = await auth_service.oauth_login(provider, db, oauth_token)
        return {
            "access_token": token_response.access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unspported grant_type",
        )


@router.get("/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code is required",
        )
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8001/auth/callback",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to retrieve token",
            )
        token = response.json()
    access_token = token.get("access_token")

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{user_info_url}?access_token={access_token}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info.")
        user_info = user_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = await auth_service.oauth_login("google", db, access_token)

    jwt_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}
