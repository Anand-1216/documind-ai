# models.py — SQLAlchemy database models
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    username        = Column(String, unique=True, nullable=False, index=True)
    email           = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)

    # Relationships
    documents    = relationship("Document",    back_populates="owner")
    chat_history = relationship("ChatHistory", back_populates="owner")

    def __repr__(self):
        return f"<User {self.username}>"


class Document(Base):
    __tablename__ = "documents"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    filename       = Column(String, nullable=False)         # UUID filename
    original_name  = Column(String, nullable=False)         # original upload name
    file_path      = Column(String, nullable=False)         # disk path
    status         = Column(String, default="processing")   # processing/ready/failed
    page_count     = Column(Integer, nullable=True)
    chunk_count    = Column(Integer, nullable=True)
    error_message  = Column(String, nullable=True)
    uploaded_at    = Column(DateTime, default=datetime.utcnow)
    owner_username = Column(String, ForeignKey("users.username"), nullable=False)

    # Relationships
    owner        = relationship("User",        back_populates="documents")
    chat_history = relationship("ChatHistory", back_populates="document",
                                cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document {self.original_name} [{self.status}]>"


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    document_id      = Column(Integer, ForeignKey("documents.id"), nullable=False)
    question         = Column(Text, nullable=False)
    answer           = Column(Text, nullable=False)
    sources          = Column(Text, nullable=True)   # JSON string
    retrieval_score  = Column(Float, nullable=True)
    asked_at         = Column(DateTime, default=datetime.utcnow)
    owner_username   = Column(String, ForeignKey("users.username"), nullable=False)

    # Relationships
    document = relationship("Document", back_populates="chat_history")
    owner    = relationship("User",     back_populates="chat_history")

    def __repr__(self):
        return f"<ChatHistory doc={self.document_id} q={self.question[:30]}>"