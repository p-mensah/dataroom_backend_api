from datetime import datetime, timedelta
from database import document_access_collection, documents_collection, investors_collection
from typing import List, Dict

class AnalyticsService:
    @staticmethod
    def get_active_users(time_window_minutes: int = 30):
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        
        active_investors = document_access_collection.distinct(
            "investor_id",
            {"timestamp": {"$gte": cutoff_time}}
        )
        
        return len(active_investors)
    
    @staticmethod
    def get_document_heatmap():
        pipeline = [
            {
                "$group": {
                    "_id": "$document_id",
                    "view_count": {"$sum": {"$cond": [{"$eq": ["$action", "view"]}, 1, 0]}},
                    "download_count": {"$sum": {"$cond": [{"$eq": ["$action", "download"]}, 1, 0]}}
                }
            },
            {"$sort": {"view_count": -1}},
            {"$limit": 20}
        ]
        
        results = list(document_access_collection.aggregate(pipeline))
        
        heatmap = []
        for item in results:
            doc = documents_collection.find_one({"_id": item["_id"]})
            if doc:
                heatmap.append({
                    "document_id": str(item["_id"]),
                    "document_title": doc.get("title", "Unknown"),
                    "view_count": item["view_count"],
                    "download_count": item["download_count"]
                })
        
        return heatmap
    
    @staticmethod
    def get_investor_activity(investor_id: str):
        pipeline = [
            {"$match": {"investor_id": investor_id}},
            {
                "$group": {
                    "_id": None,
                    "total_views": {"$sum": {"$cond": [{"$eq": ["$action", "view"]}, 1, 0]}},
                    "total_time": {"$sum": "$duration_seconds"},
                    "last_active": {"$max": "$timestamp"}
                }
            }
        ]
        
        result = list(document_access_collection.aggregate(pipeline))
        
        if result:
            return {
                "documents_viewed": result[0]["total_views"],
                "time_spent_minutes": result[0]["total_time"] // 60,
                "last_active": result[0]["last_active"]
            }
        
        return {"documents_viewed": 0, "time_spent_minutes": 0, "last_active": None}
    
    @staticmethod
    def export_analytics_report(start_date: datetime, end_date: datetime):
        # Get all activity in date range
        activities = list(document_access_collection.find({
            "timestamp": {"$gte": start_date, "$lte": end_date}
        }))
        
        # Process data for CSV export
        report_data = []
        for activity in activities:
            investor = investors_collection.find_one({"_id": activity["investor_id"]})
            document = documents_collection.find_one({"_id": activity["document_id"]})
            
            report_data.append({
                "investor_name": investor.get("full_name", "Unknown") if investor else "Unknown",
                "document_title": document.get("title", "Unknown") if document else "Unknown",
                "action": activity["action"],
                "timestamp": activity["timestamp"].isoformat(),
                "duration_seconds": activity["duration_seconds"]
            })
        
        return report_data
