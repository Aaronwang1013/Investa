from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.request import LoginRequest, RegisterRequest
from src.auth.service import AuthService
from src.user.service import UserService
from src.database import get_db
from src.config import settings


router = APIRouter()

auth_service = AuthService(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)


@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existed_user = await UserService.get_user_by_email(db, request.email)
    if existed_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = await UserService.create_user(request, db)
    print("user", user)
    return {"message": "User created successfully"}


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    print("email", request.email)
    print("password", request.password)
    print("db", db)
    try:
        return await auth_service.login(request, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error, {e}",
        )
