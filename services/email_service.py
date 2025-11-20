import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    @staticmethod
    def send_access_request_confirmation(email: str, name: str):
        subject = "Access Request Received - SAYeTECH Dataroom"
        body = f"""
        <h2>Thank you for your interest, {name}</h2>
        <p>We have received your access request to the SAYeTECH investor dataroom.</p>
        <p>Our team will review your request and respond within 24-48 hours.</p>
        """
        return EmailService.send_email(email, subject, body)
    
    @staticmethod
    def send_admin_notification(request_data: dict):
        subject = "New Dataroom Access Request"
        body = f"""
        <h2>New Access Request</h2>
        <p><strong>Name:</strong> {request_data['full_name']}</p>
        <p><strong>Email:</strong> {request_data['email']}</p>
        <p><strong>Company:</strong> {request_data['company']}</p>
        <p><strong>Phone:</strong> {request_data.get('phone', 'N/A')}</p>
        <p><strong>Message:</strong> {request_data.get('message', 'N/A')}</p>
        """
        return EmailService.send_email(settings.ADMIN_EMAIL, subject, body)
    
    @staticmethod
    def send_access_approved(email: str, name: str, token: str):
        subject = "Access Approved - SAYeTECH Dataroom"
        link = f"https://dataroom.sayetech.com/access?token={token}"
        body = f"""
        <h2>Welcome, {name}!</h2>
        <p>Your access to the SAYeTECH investor dataroom has been approved.</p>
        <p><a href="{link}">Click here to access the dataroom</a></p>
        <p>This link is valid until the expiration date set by our team.</p>
        """
        return EmailService.send_email(email, subject, body)
    
    @staticmethod
    def send_access_denied(email: str, name: str, reason: str = ""):
        subject = "Access Request Update - SAYeTECH Dataroom"
        body = f"""
        <h2>Hello {name},</h2>
        <p>Thank you for your interest in SAYeTECH.</p>
        <p>Unfortunately, we are unable to grant access to the dataroom at this time.</p>
        <p>{reason}</p>
        """
        return EmailService.send_email(email, subject, body)
