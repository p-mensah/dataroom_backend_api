from typing import List
from fastapi import APIRouter,Depends, HTTPException, Query
from models.qa import QuestionCreate, AnswerCreate, QAThreadResponse
from routers.admin_auth import get_current_admin, get_current_admin, require_admin
from services.qa import QAService

router = APIRouter(prefix="/api/qa", tags=["Q&A"])

@router.post("/questions", response_model=dict)
def submit_question(
    question: QuestionCreate,
    current_user: dict = Depends(get_current_admin)
):
    """Submit a new question"""
    question_id = QAService.submit_question(
        user_id=current_user["id"],
        question_text=question.question_text,
        category=question.category,
        is_urgent=question.is_urgent
    )
    return {"message": "Question submitted successfully", "id": question_id}

@router.get("/threads", response_model=List[QAThreadResponse])
def get_qa_threads(
    current_user: dict = Depends(get_current_admin)
):
    """Get Q&A threads for current user"""
    threads = QAService.get_qa_threads(current_user["id"])
    return threads

@router.get("/search")
def search_qa(
    q: str = Query(..., min_length=3),
    current_user: dict = Depends(get_current_admin)
):
    """Search public Q&A threads"""
    results = QAService.search_qa(q)
    return results

@router.post("/questions/{question_id}/answer")
def answer_question(
    question_id: str,
    answer: AnswerCreate,
    current_admin: dict = Depends(require_admin)
):
    """Answer a question (Admin only)"""
    success = QAService.answer_question(
        question_id=question_id,
        admin_id=current_admin["id"],
        answer_text=answer.answer_text,
        is_public=answer.is_public
    )
    
    if success:
        return {"message": "Answer posted successfully"}
    raise HTTPException(status_code=400, detail="Failed to post answer")
