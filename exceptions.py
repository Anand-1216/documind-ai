# exceptions.py — custom exception classes
from fastapi import HTTPException, status

class DocumentNotFoundException(HTTPException):
    def __init__(self, document_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found or access denied"
        )

class DocumentNotReadyException(HTTPException):
    def __init__(self, current_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document is not ready for querying. Current status: {current_status}"
        )

class UnauthorizedAccessException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

class FileTooLargeException(HTTPException):
    def __init__(self, size_mb: float, max_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large: {size_mb:.1f}MB. Maximum allowed: {max_mb}MB"
        )

class InvalidFileTypeException(HTTPException):
    def __init__(self, file_type: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Invalid file type: {file_type}. Only PDF files are accepted"
        )

class UserAlreadyExistsException(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with this {field} already exists"
        )