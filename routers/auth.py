# routers/auth.py — /users/register + /users/login
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRegister, UserResponse, LoginRequest, TokenResponse
from auth import hash_password, verify_password, create_access_token
from exceptions import UserAlreadyExistsException, UnauthorizedAccessException

router = APIRouter(prefix="/users", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(request: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""

    # Check username unique
    if db.query(User).filter(User.username == request.username).first():
        raise UserAlreadyExistsException("username")

    # Check email unique
    if db.query(User).filter(User.email == request.email).first():
        raise UserAlreadyExistsException("email")

    # Create user
    user = User(
        username        = request.username,
        email           = request.email,
        hashed_password = hash_password(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        username   = user.username,
        email      = user.email,
        created_at = user.created_at,
        message    = "Registration successful! You can now login."
    )

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token"""

    # Find user
    user = db.query(User).filter(User.username == request.username).first()

    # Verify password
    if not user or not verify_password(request.password, user.hashed_password):
        raise UnauthorizedAccessException()

    # Create token
    token = create_access_token({"sub": user.username})

    return TokenResponse(access_token=token)