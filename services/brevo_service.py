import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from config import settings
import logging

logger = logging.getLogger(__name__)

class BrevoService:
    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
    
    def send_otp_email(self, to_email: str, otp_code: str, name: str = "User"):
        """Send OTP code via Brevo"""
        sender = {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        }
        
        to = [{"email": to_email, "name": name}]
        
        subject = f"Your OTP Code - {settings.APP_NAME}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .otp-box {{ background: white; border: 2px dashed #667eea; padding: 20px; text-align: center; margin: 20px 0; border-radius: 10px; }}
                .otp-code {{ font-size: 36px; font-weight: bold; color: #667eea; letter-spacing: 8px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 OTP Verification</h1>
                    <p>{settings.APP_NAME}</p>
                </div>
                <div class="content">
                    <h2>Hello {name},</h2>
                    <p>You requested access to the SAYeTECH Investor Dataroom. Use the code below to verify your identity:</p>
                    
                    <div class="otp-box">
                        <p style="margin: 0; color: #666;">Your OTP Code</p>
                        <div class="otp-code">{otp_code}</div>
                        <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">Valid for {settings.OTP_EXPIRY_MINUTES} minutes</p>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                            <li>Never share this code with anyone</li>
                            <li>SAYeTECH will never ask for your OTP</li>
                            <li>This code expires in {settings.OTP_EXPIRY_MINUTES} minutes</li>
                            <li>If you didn't request this, please ignore this email</li>
                        </ul>
                    </div>
                    
                    <p>Having trouble? Contact us at <a href="mailto:{settings.ADMIN_EMAIL}">{settings.ADMIN_EMAIL}</a></p>
                </div>
                <div class="footer">
                    <p>© 2025 SAYeTECH. All rights reserved.</p>
                    <p>This is an automated email, please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content
        )
        
        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            logger.info(f"OTP email sent successfully to {to_email}: {api_response}")
            return True
        except ApiException as e:
            logger.error(f"Failed to send OTP email: {e}")
            return False
    
    def send_login_success_email(self, to_email: str, name: str, login_time: str, ip_address: str = "Unknown"):
        """Send login notification"""
        sender = {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        }
        
        to = [{"email": to_email, "name": name}]
        subject = f"New Login to {settings.APP_NAME}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #28a745; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #28a745; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1> Successful Login</h1>
                </div>
                <div class="content">
                    <h2>Hello {name},</h2>
                    <p>Your account was successfully accessed:</p>
                    
                    <div class="info-box">
                        <p><strong>Time:</strong> {login_time}</p>
                        <p><strong>IP Address:</strong> {ip_address}</p>
                        <p><strong>Location:</strong> Dataroom Access</p>
                    </div>
                    
                    <p>If this wasn't you, please contact us immediately at {settings.ADMIN_EMAIL}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content
        )
        
        try:
            self.api_instance.send_transac_email(send_smtp_email)
            return True
        except ApiException as e:
            logger.error(f"Failed to send login notification: {e}")
            return False