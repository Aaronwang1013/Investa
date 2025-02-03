from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.request import LoginRequest, RegisterRequest
from src.auth.service import AuthService
from src.user.service import UserService
from src.database import get_db
from src.config import settings
import logging


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
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully", "email": user.email},
        headers={"Location": f"/users/{user.id}"},
    )


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        token_response = await auth_service.login(db, request)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Login successful",
                "data": {
                    "access_token": token_response.access_token,
                    "token_type": token_response.token_type,
                    "expires_in": auth_service.access_token_expire_minutes,
                },
            },
        )
    except HTTPException as http_exp:
        logging.warning(f"Login failed for {request.email}, {http_exp.detail}")
        raise http_exp
    except Exception as e:
        logging.error(f"Internal server error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
