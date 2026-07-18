# dependencies.py — replace entire file
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_token
from models import User
from exceptions import UnauthorizedAccessException

# HTTPBearer shows clean "Bearer token" input in Swagger
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db:          Session                      = Depends(get_db)
) -> User:
    """
    Dependency — extracts and validates JWT token.
    Returns current user or raises 401.
    """
    token    = credentials.credentials
    username = verify_token(token)

    if not username:
        raise UnauthorizedAccessException()

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UnauthorizedAccessException()

    return user