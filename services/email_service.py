# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # from config import settings
# # import logging

# # logger = logging.getLogger(__name__)

# # class EmailService:
# #     @staticmethod
# #     def send_email(to_email: str, subject: str, body: str):
# #         """Send email using SMTP with SSL"""
        
# #         msg = MIMEMultipart()
# #         msg['From'] = settings.FROM_EMAIL
# #         msg['To'] = to_email
# #         msg['Subject'] = subject
# #         msg.attach(MIMEText(body, 'html'))
        
# #         try:
# #             print(f"📧 Attempting to send email to {to_email}...")
# #             print(f"Using SMTP: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
            
# #             # Use SMTP_SSL for port 465
# #             if settings.SMTP_USE_SSL:
# #                 with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
# #                     server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
# #                     print("✅ Login successful")
# #                     server.send_message(msg)
# #                     print(f"✅ Email sent successfully to {to_email}")
# #             else:
# #                 # Use SMTP with STARTTLS for port 587
# #                 with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
# #                     if settings.SMTP_USE_TLS:
# #                         server.starttls()
# #                         print("✅ TLS started")
# #                     server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
# #                     print("✅ Login successful")
# #                     server.send_message(msg)
# #                     print(f"✅ Email sent successfully to {to_email}")
            
# #             return True
            
# #         except smtplib.SMTPAuthenticationError as e:
# #             error_msg = f"❌ Authentication failed: {e}"
# #             logger.error(error_msg)
# #             print(error_msg)
# #             return False
            
# #         except smtplib.SMTPException as e:
# #             error_msg = f"❌ SMTP error: {e}"
# #             logger.error(error_msg)
# #             print(error_msg)
# #             return False
            
# #         except Exception as e:
# #             error_msg = f"❌ Unexpected error: {type(e).__name__} - {e}"
# #             logger.error(error_msg)
# #             print(error_msg)
# #             return False
    
# #     @staticmethod
# #     def send_access_request_confirmation(email: str, name: str):
# #         subject = "Access Request Received - SAYeTECH Dataroom"
# #         body = f"""
# #         <html>
# #         <body>
# #             <h2>Thank you for your interest, {name}</h2>
# #             <p>We have received your access request to the SAYeTECH investor dataroom.</p>
# #             <p>Our team will review your request and respond within 24-48 hours.</p>
# #             <br>
# #             <p>Best regards,<br>SAYeTECH Team</p>
# #         </body>
# #         </html>
# #         """
# #         return EmailService.send_email(email, subject, body)
    
# #     @staticmethod
# #     def send_admin_notification(request_data: dict):
# #         subject = "New Dataroom Access Request"
# #         body = f"""
# #         <html>
# #         <body>
# #             <h2>New Access Request</h2>
# #             <p><strong>Name:</strong> {request_data['full_name']}</p>
# #             <p><strong>Email:</strong> {request_data['email']}</p>
# #             <p><strong>Company:</strong> {request_data['company']}</p>
# #             <p><strong>Phone:</strong> {request_data.get('phone', 'N/A')}</p>
# #             <p><strong>Message:</strong> {request_data.get('message', 'N/A')}</p>
# #         </body>
# #         </html>
# #         """
# #         return EmailService.send_email(settings.ADMIN_EMAIL, subject, body)
    
# #     @staticmethod
# #     def send_access_approved(email: str, name: str, token: str):
# #         subject = "Access Approved - SAYeTECH Dataroom"
# #         link = f"https://investor-dataroom-rq1l.vercel.app/login"
# #         body = f"""
# #         <html>
# #         <body>
# #             <h2>Welcome, {name}!</h2>
# #             <p>Your access to the SAYeTECH investor dataroom has been approved.</p>
# #             <p><a href="{link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Access Dataroom</a></p>
# #             <p>This link is valid until the expiration date set by our team.</p>
# #             <br>
# #             <p>Best regards,<br>SAYeTECH Team</p>   
# #         </body>
# #         </html>
# #         """
# #         return EmailService.send_email(email, subject, body)
    
# #     @staticmethod
# #     def send_access_denied(email: str, name: str, reason: str = ""):
# #         subject = "Access Request Update - SAYeTECH Dataroom"
# #         body = f"""
# #         <html>
# #         <body>
# #             <h2>Hello {name},</h2>
# #             <p>Thank you for your interest in SAYeTECH.</p>
# #             <p>Unfortunately, we are unable to grant access to the dataroom at this time.</p>
# #             {f"<p><strong>Reason:</strong> {reason}</p>" if reason else ""}
# #             <br>
# #             <p>Best regards,<br>SAYeTECH Team</p>
# #         </body>
# #         </html>
# #         """
# #         return EmailService.send_email(email, subject, body)



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from config import settings

# class EmailService:
#     @staticmethod
#     def send_email(to_email: str, subject: str, body: str):
#         """Send email using Brevo SMTP"""
#         msg = MIMEMultipart()
#         msg['From'] = "dataroom@sayetech.io"
#         msg['To'] = to_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'html'))
        
#         try:
#             with smtplib.SMTP('smtp-relay.brevo.com', 587) as server:
#                 server.starttls()
#                 server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
#                 server.send_message(msg)
            
#             print(f" Email sent to {to_email}")
#             return True
#         except Exception as e:
#             print(f" Email error: {e}")
#             raise Exception(f"Failed to send email: {str(e)}")
    
#     @staticmethod
#     def send_access_request_confirmation(email: str, name: str):
#         """Send confirmation email after access request submission"""
#         subject = "Access Request Received - SAYeTECH Dataroom"
#         body = f"""
#         <!DOCTYPE html>
#         <html>
#         <body style="font-family: Arial, sans-serif; padding: 20px;">
#             <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
#                 <h2 style="color: #4CAF50;">✅ Access Request Received</h2>
#                 <p>Hello {name},</p>
#                 <p>Thank you for your interest in the <strong>SAYeTECH Investor Dataroom</strong>.</p>
#                 <p>We have received your access request and our team will review it shortly.</p>
                
#                 <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
#                     <h3 style="margin-top: 0;">📧 Next Step: Verify Your Email</h3>
#                     <p>To complete your request, please verify your email address by requesting an OTP (One-Time Password) from our platform.</p>
#                 </div>
                
#                 <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
#                     <p style="margin: 0;"><strong>⏰ What happens next?</strong></p>
#                     <ol style="margin: 10px 0; padding-left: 20px;">
#                         <li>Verify your email with OTP</li>
#                         <li>Our team reviews your request (24-48 hours)</li>
#                         <li>You'll receive an email with access details if approved</li>
#                     </ol>
#                 </div>
                
#                 <p>If you have any questions, contact us at <a href="mailto:dataroom@sayetech.io">dataroom@sayetech.io</a></p>
                
#                 <p style="color: #666; font-size: 12px; text-align: center; margin-top: 30px;">
#                     © 2025 SAYeTECH. All rights reserved.
#                 </p>
#             </div>
#         </body>
#         </html>
#         """
        
#         return EmailService.send_email(email, subject, body)
    
#     @staticmethod
#     def send_admin_notification(request_data: dict):
#         """Send notification to admin about new access request"""
#         subject = "🔔 New Dataroom Access Request"
#         body = f"""
#         <!DOCTYPE html>
#         <html>
#         <body style="font-family: Arial, sans-serif; padding: 20px;">
#             <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
#                 <h2 style="color: #333;">New Access Request</h2>
#                 <table style="width: 100%; border-collapse: collapse;">
#                     <tr>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Name:</strong></td>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;">{request_data.get('full_name', 'N/A')}</td>
#                     </tr>
#                     <tr>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Email:</strong></td>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;">{request_data.get('email', 'N/A')}</td>
#                     </tr>
#                     <tr>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Company:</strong></td>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;">{request_data.get('company', 'N/A')}</td>
#                     </tr>
#                     <tr>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Phone:</strong></td>
#                         <td style="padding: 10px; border-bottom: 1px solid #ddd;">{request_data.get('phone', 'N/A')}</td>
#                     </tr>
#                     <tr>
#                         <td style="padding: 10px;"><strong>Message:</strong></td>
#                         <td style="padding: 10px;">{request_data.get('message', 'N/A')}</td>
#                     </tr>
#                 </table>
                
#                 <p style="margin-top: 20px;">
#                     <a href="http://localhost:8000/docs#/Admin%20Management/list_access_requests_api_admin_access_requests_get" 
#                        style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
#                         Review in Admin Panel
#                     </a>
#                 </p>
#             </div>
#         </body>
#         </html>
#         """
        
#         return EmailService.send_email(settings.ADMIN_EMAIL, subject, body)
    
#     @staticmethod
#     def send_access_approved(email: str, name: str, token: str):
#         """Send email when access is approved"""
#         subject = " Access Approved - SAYeTECH Dataroom"
#         link = f"https://investor-dataroom-rq1l.vercel.app/login"
#         body = f"""
#         <!DOCTYPE html>
#         <html>
#         <body style="font-family: Arial, sans-serif; padding: 20px;">
#             <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
#                 <h2 style="color: #4CAF50;">Welcome to SAYeTECH Dataroom!</h2>
#                 <p>Hello {name},</p>
#                 <p>Great news! Your access request has been approved.</p>
                
#                 <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
#                     <p><strong>Click below to access the dataroom:</strong></p>
#                     <a href="{link}" 
#                        style="background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; font-size: 16px;">
#                         Access Dataroom
#                     </a>
#                 </div>
                
#                 <p style="color: #666; font-size: 14px;">
#                     If the button doesn't work, copy and paste this link:<br>
#                     <a href="{link}">{link}</a>
#                 </p>
#             </div>
#         </body>
#         </html>
#         """
        
#         return EmailService.send_email(email, subject, body)
    
#     @staticmethod
#     def send_access_denied(email: str, name: str, reason: str = ""):
#         """Send email when access is denied"""
#         subject = "Access Request Update - SAYeTECH Dataroom"
#         body = f"""
#         <!DOCTYPE html>
#         <html>
#         <body style="font-family: Arial, sans-serif; padding: 20px;">
#             <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
#                 <h2 style="color: #333;">Access Request Update</h2>
#                 <p>Hello {name},</p>
#                 <p>Thank you for your interest in SAYeTECH.</p>
#                 <p>Unfortunately, we are unable to grant access to the dataroom at this time.</p>
#                 {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
#                 <p>If you have any questions, please contact us at <a href="mailto:dataroom@sayetech.io">dataroom@sayetech.io</a></p>
#             </div>
#         </body>
#         </html>
#         """
        
#         return EmailService.send_email(email, subject, body)

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
            # Try non-SSL connection first (port 587)
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()  # Enable encryption
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except:
            # If non-SSL fails, try SSL connection (port 465)
            try:
                import ssl
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(settings.SMTP_HOST, 465, context=context) as server:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                return True
            except Exception as e:
                print(f"Failed to send email: {e}")
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
        link = f"https://investor-dataroom-rq1l.vercel.app/login"
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
    
    @staticmethod
    def send_access_request_status(email: str, name: str, status: str, admin_notes: str = None):
        """Send status update email for access request"""
        subject = f"Your Data Room Access Request Status: {status.upper()}"
        
        body = f"""
        <h2>Dear {name},</h2>
        <p>Your data room access request status has been updated to: <strong>{status.upper()}</strong></p>
        """
        
        if admin_notes:
            body += f"<p><strong>Admin Notes:</strong> {admin_notes}</p>"
        
        if status.lower() == "approved":
            body += "<p>Congratulations! Your access request has been approved. You can now access the data room.</p>"
        elif status.lower() == "denied":
            body += "<p>Unfortunately, your access request has been denied. Please contact us if you have questions.</p>"
        else:
            body += "<p>Your request is still under review.</p>"
        
        body += "<p>Thank you for your interest in SAYeTECH.</p>"
        
        return EmailService.send_email(email, subject, body)
    
    @staticmethod
    def send_otp_email(email: str, otp: str):
        """Send OTP email to user"""
        subject = "Your OTP Code for SAYeTECH Data Room"
        
        body = f"""
        <h2>Dear User,</h2>
        <p>Your OTP code for accessing SAYeTECH Data Room is: <strong>{otp}</strong></p>
        <p>This code is valid for 10 minutes.</p>
        <p>Thank you for using SAYeTECH Data Room.</p>
        """
        
        return EmailService.send_email(email, subject, body)