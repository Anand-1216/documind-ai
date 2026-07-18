# schemas.py — Pydantic request/response schemas
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# ── Auth ────────────────────────────────────────────────
class UserRegister(BaseModel):
    username: str
    email:    str
    password: str

    @validator("username")
    def username_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be under 50 characters")
        return v

    @validator("password")
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    username:   str
    email:      str
    created_at: datetime
    message:    str = "Registration successful"

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"

# ── Documents ────────────────────────────────────────────
class DocumentResponse(BaseModel):
    id:            int
    original_name: str
    status:        str
    page_count:    Optional[int]
    chunk_count:   Optional[int]
    error_message: Optional[str]
    uploaded_at:   datetime

    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    document_id:   int
    original_name: str
    status:        str
    message:       str

# ── Chat ─────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

    @validator("question")
    def question_valid(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty")
        if len(v) > 1000:
            raise ValueError("Question too long — max 1000 characters")
        return v

class SourceChunk(BaseModel):
    content:    str
    chunk_index: Optional[int]

class ChatResponse(BaseModel):
    answer:          str
    sources:         List[SourceChunk]
    retrieval_score: Optional[float]
    document_name:   str

class ChatHistoryResponse(BaseModel):
    id:              int
    question:        str
    answer:          str
    retrieval_score: Optional[float]
    asked_at:        datetime

    class Config:
        from_attributes = True

# ── Health ───────────────────────────────────────────────
class HealthResponse(BaseModel):
    status:   str
    database: str
    chromadb: str