from datetime import datetime, timedelta
from database import meetings_collection
from services.email_service import EmailService
import secrets

class MeetingService:
    @staticmethod
    def schedule_meeting(investor_id: str, scheduled_at: datetime, 
                        duration_minutes: int, notes: str = ""):
        # Generate meeting link (in production, integrate with Zoom/Google Meet)
        meeting_link = f"https://meet.sayetech.com/{secrets.token_urlsafe(16)}"
        
        meeting_data = {
            "investor_id": investor_id,
            "scheduled_at": scheduled_at,
            "duration_minutes": duration_minutes,
            "meeting_link": meeting_link,
            "status": "scheduled",
            "created_at": datetime.utcnow(),
            "notes": notes
        }
        
        result = meetings_collection.insert_one(meeting_data)
        
        # Send confirmation emails
        MeetingService._send_meeting_confirmation(investor_id, meeting_data)
        
        return str(result.inserted_id)
    
    @staticmethod
    def _send_meeting_confirmation(investor_id: str, meeting_data: dict):
        # Implementation for sending meeting confirmation
        # This would integrate with your email service
        pass
    
    @staticmethod
    def get_available_slots(date: datetime):
        # Business hours: 9 AM - 5 PM
        slots = []
        start_hour = 9
        end_hour = 17
        
        for hour in range(start_hour, end_hour):
            slot_time = date.replace(hour=hour, minute=0, second=0)
            
            # Check if slot is available
            existing = meetings_collection.find_one({
                "scheduled_at": slot_time,
                "status": {"$ne": "cancelled"}
            })
            
            if not existing:
                slots.append(slot_time.isoformat())
        
        return slots