import httpx
from datetime import datetime
from database import alert_configs_collection, alert_logs_collection, investors_collection
from services.email_service import EmailService
from config import settings

class AlertService:
    @staticmethod
    async def trigger_alert(alert_type: str, investor_id: str, context: dict):
        # Get active alert configs for this type
        alert_configs = list(alert_configs_collection.find({
            "alert_type": alert_type,
            "is_active": True
        }))
        
        for config in alert_configs:
            # Check if conditions are met
            if AlertService._check_conditions(config["trigger_conditions"], context):
                # Get investor info
                investor = investors_collection.find_one({"_id": investor_id})
                if not investor:
                    continue
                
                message = AlertService._create_message(alert_type, investor, context)
                
                # Send notifications
                for channel in config["notification_channels"]:
                    if channel == "email":
                        EmailService.send_email(settings.ADMIN_EMAIL, f"Alert: {alert_type}", message)
                    elif channel == "slack":
                        await AlertService._send_slack_notification(message)
                
                # Log alert
                alert_logs_collection.insert_one({
                    "alert_config_id": str(config["_id"]),
                    "investor_id": investor_id,
                    "message": message,
                    "triggered_at": datetime.utcnow(),
                    "is_sent": True
                })
    
    @staticmethod
    def _check_conditions(conditions: dict, context: dict) -> bool:
        # Simple condition checking logic
        for key, value in conditions.items():
            if key not in context or context[key] < value:
                return False
        return True
    
    @staticmethod
    def _create_message(alert_type: str, investor: dict, context: dict) -> str:
        messages = {
            "high_value_login": f"High-value investor {investor['full_name']} from {investor['company']} has logged in.",
            "critical_document_view": f"Investor {investor['full_name']} viewed critical document: {context.get('document_title', 'Unknown')}",
            "extended_session": f"Investor {investor['full_name']} has spent {context.get('duration_minutes', 0)} minutes in the dataroom."
        }
        return messages.get(alert_type, f"Alert triggered for investor {investor['full_name']}")
    
    @staticmethod
    async def _send_slack_notification(message: str):
        if not settings.SLACK_WEBHOOK_URL:
            return
        
        async with httpx.AsyncClient() as client:
            await client.post(
                settings.SLACK_WEBHOOK_URL,
                json={"text": message}
            )
