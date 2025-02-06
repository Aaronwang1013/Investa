from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.user.service import UserService
from src.auth.request import RegisterRequest
from src.database import get_db


router = APIRouter()


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
