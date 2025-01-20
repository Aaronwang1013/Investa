from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()

@router.post("/token")
def login(from_data: OAuth2PasswordRequestForm=Depends()):
    pass