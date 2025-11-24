<!-- <!-- # dataroom_backend_api

# Project Structure (Flat - No app folder):
"""
dataroom_backend_api/
├── main.py
├── config.py
├── database.py
├── models/
│   ├── __init__.py
│   ├── access_request.py
│   ├── access_token.py
│   └── audit_log.py
├── routers/
│   ├── __init__.py
│   ├── access_requests.py
│   └── admin.py
├── services/
│   ├── __init__.py
│   ├── email_service.py
│   └── auth_service.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── requirements.txt
├── .env
└── README.md -->


# SAYeTECH Investor Dataroom API

A secure, feature-rich investor dataroom with OTP authentication, NDA management, 
role-based access control, and comprehensive document management.

## Features

### 1. Access Request Management
- Investors can request access to the dataroom
- Email notifications for both investors and admins
- Status tracking (pending, approved, denied)

### 2. OTP Authentication
- Secure one-time password login
- Email-based OTP delivery
- Configurable expiry and attempt limits
- JWT token-based session management

### 3. NDA Management
- Digital NDA acceptance required before document access
- Timestamp and IP address logging
- Version control for NDA documents
- Digital signature capture

### 4. Role-Based Access Control (RBAC)
- Three default permission levels:
  - View Only
  - Download Allowed
  - Expiry-Controlled
- Granular permission management
- Automatic access expiry
- Session-level permission enforcement

### 5. Document Management
- Six main categories:
  - Company Overview
  - Market & Impact
  - Financials
  - IP & Technology
  - Traction
  - Legal
- Subcategory support
- Version control
- File size validation
- Multiple file type support

### 6. Audit & Logging
- Comprehensive access logging
- Document view/download tracking
- Admin action audit trails
- IP address and user agent tracking

## Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: MongoDB
- **Authentication**: JWT + OTP (pyotp)
- **Email**: SMTP (configurable)
- **File Storage**: Local filesystem (configurable)

## Installation

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- SMTP server access (Gmail, SendGrid, etc.)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd dataroom_backend_api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python init_database.py
```

6. **Run the application**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/auth/request-otp` - Request OTP code
- `POST /api/auth/verify-otp` - Verify OTP and get token
- `GET /api/auth/me` - Get current user info

### Access Requests
- `POST /api/access-requests/` - Submit access request
- `GET /api/access-requests/{request_id}` - Get request details

### NDA
- `GET /api/nda/content` - Get NDA content
- `POST /api/nda/accept` - Accept NDA
- `GET /api/nda/status` - Check NDA acceptance status

### Permissions
- `GET /api/permissions/levels` - List permission levels
- `GET /api/permissions/user/{user_id}/permissions` - Get user permissions

### Documents
- `GET /api/documents/categories` - List categories
- `POST /api/documents/upload` - Upload document (Admin)
- `GET /api/documents/category/{category_id}/documents` - List documents
- `GET /api/documents/{document_id}` - Get document details
- `GET /api/documents/{document_id}/download` - Download document
- `GET /api/documents/{document_id}/view` - View document

### Users
- `POST /api/users/` - Create user (Admin)
- `GET /api/users/` - List users (Admin)
- `GET /api/users/{user_id}` - Get user details
- `PUT /api/users/{user_id}` - Update user

### Admin
- `GET /api/admin/access-requests` - List all requests
- `PUT /api/admin/access-requests/{request_id}` - Update request status

## Security Features

1. **Authentication**
   - OTP-based login (6-digit code)
   - JWT token with configurable expiry
   - Automatic token refresh

2. **Authorization**
   - Role-based access control
   - Permission-level enforcement
   - Session validation

3. **NDA Compliance**
   - Mandatory acceptance before access
   - Legal audit trail
   - IP and timestamp logging

4. **File Security**
   - File type validation
   - Size restrictions
   - Access logging
   - Download tracking

5. **Audit Trail**
   - All actions logged
   - User activity tracking
   - Admin action monitoring

## Configuration

### Email Settings
Configure SMTP in `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### File Upload Settings
```env
MAX_FILE_SIZE_MB=50
UPLOAD_DIR=./uploads
ALLOWED_FILE_TYPES=["pdf","doc","docx","xls","xlsx","ppt","pptx"]
```

### Security Settings
```env
SECRET_KEY=your-super-secret-key
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=3
```

## Default Admin Credentials

After running `init_database.py`:
- **Email**: admin@sayetech.com
- **Password**: Admin@123!

⚠️ **IMPORTANT**: Change the password immediately after first login!

## Database Collections

- `access_requests` - Access request submissions
- `access_tokens` - Active access tokens
- `admin_users` - Administrator accounts
- `audit_logs` - System audit trail
- `users` - Investor user accounts
- `otp_codes` - OTP codes (auto-expire)
- `nda_acceptances` - NDA acceptance records
- `permission_levels` - Permission configurations
- `document_categories` - Document organization
- `documents` - Document metadata
- `document_versions` - Version history
- `document_access_logs` - Access tracking

## Testing

### Manual Testing with cURL

**Request OTP:**
```bash
curl -X POST http://localhost:8000/api/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"email": "investor@example.com"}'
```

**Verify OTP:**
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email": "investor@example.com", "otp_code": "123456"}'
```

**Access Protected Endpoint:**
```bash
curl -X GET http://localhost:8000/api/documents/categories \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Production Deployment

### Environment Variables
- Set strong `SECRET_KEY`
- Use production SMTP credentials
- Configure proper CORS origins
- Enable HTTPS

### Security Checklist
- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS properly
- [ ] Enable HTTPS/TLS
- [ ] Set up backup strategy
- [ ] Configure log rotation
- [ ] Set up monitoring
- [ ] Review file upload limits

### Recommended Stack
- **Web Server**: Nginx
- **WSGI**: Uvicorn + Gunicorn
- **Database**: MongoDB Atlas (managed)
- **Email**: SendGrid or AWS SES
- **Storage**: AWS S3 or similar

## Support

For issues or questions:
- Email: support@sayetech.com
- Documentation: https://docs.sayetech.com

## License

Proprietary - SAYeTECH © 2025
"""

# ===============================
# test_api.py - API Test Script
# ===============================
"""
Simple test script to verify API endpoints
Run: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    print(response.json())
    print()

def test_request_access():
    """Test access request submission"""
    data = {
        "email": "investor@example.com",
        "full_name": "John Investor",
        "company": "Investment Firm LLC",
        "phone": "+1234567890",
        "message": "Interested in Series A investment"
    }
    
    response = requests.post(f"{BASE_URL}/api/access-requests/", json=data)
    print(f"Access Request: {response.status_code}")
    print(response.json())
    print()
    return response.json().get("id")

def test_list_categories():
    """Test listing document categories"""
    response = requests.get(f"{BASE_URL}/api/documents/categories")
    print(f"List Categories (no auth): {response.status_code}")
    print(response.json() if response.status_code != 401 else "Authentication required")
    print()

def test_permission_levels():
    """Test listing permission levels"""
    response = requests.get(f"{BASE_URL}/api/permissions/levels")
    print(f"Permission Levels: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def main():
    print("=" * 60)
    print("SAYeTECH Dataroom API - Test Script")
    print("=" * 60)
    print()
    
    test_health()
    test_permission_levels()
    request_id = test_request_access()
    test_list_categories()
    
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main() -->