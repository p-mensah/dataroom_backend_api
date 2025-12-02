from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database import qa_threads_collection, users_collection
from services.email_service import EmailService

class QAService:
    
    @staticmethod
    def submit_question(user_id: str, question_text: str, category: str, is_urgent: bool = False):
        """Submit a new question"""
        question_data = {
            "question_text": question_text,
            "category": category,
            "asked_by": user_id,
            "asked_at": datetime.utcnow(),
            "answer_text": None,
            "answered_by": None,
            "answered_at": None,
            "is_public": False,
            "is_urgent": is_urgent,
            "status": "pending"
        }
        
        result = qa_threads_collection.insert_one(question_data)
        
        # Notify admin of new question
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            QAService._notify_admin_new_question(
                user.get("email"),
                user.get("full_name"),
                question_text,
                category,
                is_urgent
            )
        
        return str(result.inserted_id)
    
    @staticmethod
    def answer_question(
        question_id: str,
        admin_id: str,
        answer_text: str,
        is_public: bool = False
    ):
        """Answer a question"""
        result = qa_threads_collection.update_one(
            {"_id": ObjectId(question_id)},
            {
                "$set": {
                    "answer_text": answer_text,
                    "answered_by": admin_id,
                    "answered_at": datetime.utcnow(),
                    "is_public": is_public,
                    "status": "answered"
                }
            }
        )
        
        # Notify user of answer
        thread = qa_threads_collection.find_one({"_id": ObjectId(question_id)})
        if thread:
            user = users_collection.find_one({"_id": ObjectId(thread["asked_by"])})
            if user:
                QAService._notify_user_answer(
                    user.get("email"),
                    user.get("full_name"),
                    thread["question_text"],
                    answer_text,
                    is_public
                )
        
        return result.modified_count > 0
    
    @staticmethod
    def get_qa_threads(user_id: str, include_public: bool = True) -> List[dict]:
        """Get Q&A threads for a user"""
        filter_query = {"$or": [{"asked_by": user_id}]}
        
        if include_public:
            filter_query["$or"].append({"is_public": True, "status": "answered"})
        
        threads = list(qa_threads_collection.find(filter_query).sort("asked_at", -1))
        
        for thread in threads:
            thread["id"] = str(thread.pop("_id"))
        
        return threads
    
    @staticmethod
    def search_qa(query: str) -> List[dict]:
        """Search Q&A threads"""
        threads = list(qa_threads_collection.find({
            "$text": {"$search": query},
            "is_public": True,
            "status": "answered"
        }))
        
        for thread in threads:
            thread["id"] = str(thread.pop("_id"))
        
        return threads
    
    @staticmethod
    def _notify_admin_new_question(email: str, name: str, question: str, category: str, is_urgent: bool):
        """Notify admin of new question"""
        # Implementation using EmailService
        pass
    
    @staticmethod
    def _notify_user_answer(email: str, name: str, question: str, answer: str, is_public: bool):
        """Notify user when their question is answered"""
        # Implementation using EmailService
        pass
