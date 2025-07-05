from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.rate_limiter import limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
auth_scheme = HTTPBearer()



class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/auth/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, req: LoginRequest):
    logger.info("Login attempt for user: %s", req.username)
    if req.username == "admin" and req.password == "password":
        logger.info("Successful login for user: %s", req.username)
        return {"access_token": "fake-jwt-token-123", "token_type": "bearer"}
    logger.warning("Failed login attempt for user: %s", req.username)
    raise HTTPException(status_code=401, detail="Invalid credentials")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    token = credentials.credentials
    if token != "fake-jwt-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "admin"}
