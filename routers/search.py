from fastapi import APIRouter, Depends, Query
from typing import List
from routers.admin_auth import get_current_admin 
from services.search_service import SearchService
from models.search import SearchResult, SearchHistoryItem

router = APIRouter(prefix="/api/search", tags=["Search"])

# @router.get("/documents", response_model=List[SearchResult])
# def search_documents(
#     document: str = Query(..., min_length=1, description="Search documents by name, ID, category, or file type"),
#     current_user: dict = Depends(get_current_admin)
# ):
#     """
#     Dataroom document search endpoint
    
#     Searches documents by:
#     - Document ID
#     - Document name/title
#     - Category
#     - File type
#     """
#     results = SearchService.search_documents(
#         query=document,
#         user_id=current_user["id"]
#     )
#     return results


# @router.get("/history", response_model=List[SearchHistoryItem])
# def get_search_history(
#     limit: int = Query(10, ge=1, le=50, description="Number of recent searches to return"),
#     current_user: dict = Depends(get_current_admin)
# ):
#     """Get user's recent search history for the current session"""
#     history = SearchService.get_search_history(current_user["id"], limit)
#     return history


# @router.delete("/history")
# def clear_search_history(
#     current_user: dict = Depends(get_current_admin)
# ):
#     """Clear user's search history"""
#     SearchService.clear_search_history(current_user["id"])
#     return {"message": "Search history cleared successfully"}
