from pymongo import MongoClient
from bson import ObjectId

class SearchService:
    def __init__(self):
        # Updated connection string
        self.client = MongoClient('mongodb+srv://dataroom:dataroom@grow-cohort6.safmckr.mongodb.net/')
        self.db = self.client["investor_dataroom"]
        self.collection = self.db.documents

    def search_documents(self, query: str, user_id: str, document_type: str = None, category: str = None):
        """Search documents with regex matching"""
        search_query = {}
        
        # Check if query is a valid ObjectId for exact match
        try:
            search_query["_id"] = ObjectId(query)
        except:
            # If not a valid ObjectId, search in multiple fields using regex
            search_query["$or"] = [
                {"name": {"$regex": query, "$options": "i"}},  # case-insensitive regex
                {"type": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        
        # Add additional filters if provided
        if document_type:
            search_query["type"] = {"$regex": document_type, "$options": "i"}
        if category:
            search_query["category"] = {"$regex": category, "$options": "i"}
        
        # Execute search
        cursor = self.collection.find(search_query)
        results = []
        
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            # Create SearchResult objects based on your model
            results.append(doc)  # Adjust based on your SearchResult model
        
        return results
