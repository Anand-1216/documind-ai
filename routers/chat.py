# routers/chat.py — Q&A endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from database import get_db
from models import User, Document, ChatHistory
from schemas import QuestionRequest, ChatResponse, ChatHistoryResponse, SourceChunk
from dependencies import get_current_user
from exceptions import DocumentNotFoundException, DocumentNotReadyException
from rag_pipeline import answer_question

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/{document_id}", response_model=ChatResponse)
def ask_question(
    document_id:  int,
    request:      QuestionRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    """Ask a question about a document"""

    # Verify document exists and belongs to user
    doc = db.query(Document).filter(
        Document.id            == document_id,
        Document.owner_username == current_user.username
    ).first()

    if not doc:
        raise DocumentNotFoundException(document_id)

    # Check document is ready
    if doc.status != "ready":
        raise DocumentNotReadyException(doc.status)

    # Run RAG pipeline
    result = answer_question(
        document_id   = document_id,
        question      = request.question,
        username      = current_user.username,
        document_name = doc.original_name
    )

    # Save to chat history
    history = ChatHistory(
        document_id      = document_id,
        question         = request.question,
        answer           = result["answer"],
        sources          = json.dumps(result["sources"]),
        retrieval_score  = result["retrieval_score"],
        owner_username   = current_user.username
    )
    db.add(history)
    db.commit()

    # Build response
    sources = [
        SourceChunk(
            content     = s["content"],
            chunk_index = s["chunk_index"]
        )
        for s in result["sources"]
    ]

    return ChatResponse(
        answer          = result["answer"],
        sources         = sources,
        retrieval_score = result["retrieval_score"],
        document_name   = doc.original_name
    )

@router.get("/{document_id}/history", response_model=List[ChatHistoryResponse])
def get_chat_history(
    document_id:  int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    """Get all Q&A history for a document"""

    # Verify document belongs to user
    doc = db.query(Document).filter(
        Document.id            == document_id,
        Document.owner_username == current_user.username
    ).first()

    if not doc:
        raise DocumentNotFoundException(document_id)

    history = db.query(ChatHistory).filter(
        ChatHistory.document_id    == document_id,
        ChatHistory.owner_username == current_user.username
    ).order_by(ChatHistory.asked_at.desc()).all()

    return history

@router.delete("/{chat_id}")
def delete_chat(
    chat_id:      int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    """Delete a single chat entry"""
    chat = db.query(ChatHistory).filter(
        ChatHistory.id           == chat_id,
        ChatHistory.owner_username == current_user.username
    ).first()

    if not chat:
        raise DocumentNotFoundException(chat_id)

    db.delete(chat)
    db.commit()

    return {"message": "Chat entry deleted successfully"}