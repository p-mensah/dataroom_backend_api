# 🚀 SAYeTECH Investor Dataroom

A comprehensive, secure investor dataroom platform built with FastAPI, MongoDB, and Python. This system enables SAYeTECH to manage investor access, share documents, track analytics, and facilitate investor engagement seamlessly.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![FastAPI](https://img.shields.io/badge/fastapi-0.109.0-teal)
![MongoDB](https://img.shields.io/badge/mongodb-4.6+-brightgreen)

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## ✨ Features

### 🔐 Access Management
- **Investor Access Requests**: Email-based access request system with approval workflow
- **Token-based Authentication**: Secure, expiring access tokens for investors
- **Admin Approval System**: Review, approve, deny, or set expiration dates
- **Audit Logging**: Complete trail of all access changes

### 📄 Document Management
- **Secure Upload**: Support for PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX (up to 50MB)
- **Full-Text Search**: Search documents by title, description, tags, and content
- **Auto-suggestions**: Smart search suggestions as you type
- **Category & Tag System**: Organize documents efficiently
- **View/Download Tracking**: Monitor document engagement

### 🔍 Advanced Search
- **Multi-filter Search**: Filter by type, date, category, tags
- **Search History**: Track investor search patterns
- **Quick Access**: Recently viewed documents

### 📊 Real-time Analytics
- **Activity Dashboard**: Live tracking of active users and engagement
- **Document Heatmap**: Visualize most-viewed and downloaded documents
- **Investor Activity Reports**: Time spent, documents viewed, last active
- **Export Functionality**: CSV/PDF reports for any date range
- **30-second Auto-refresh**: Real-time updates

### 🔔 Smart Alert System
- **High-Value Investor Alerts**: Notifications when key investors log in
- **Critical Document Tracking**: Alerts when specific documents are viewed
- **Session Duration Alerts**: Trigger on extended session times
- **Multi-channel Notifications**: Email and Slack integration
- **Configurable Triggers**: Customize alert conditions

### 💬 Q&A System
- **In-app Questions**: Investors submit questions directly
- **Category Tagging**: Organize questions by topic
- **Public/Private Responses**: Choose visibility for each answer
- **Email Notifications**: Auto-notify when questions are answered
- **Search Q&A History**: Find answers to previous questions

### 📅 Meeting Scheduler
- **Calendar Integration**: Google Calendar/Outlook compatible
- **Available Time Slots**: Dynamic slot availability checking
- **Automated Reminders**: 24-hour and 1-hour email reminders
- **Reschedule/Cancel**: Easy meeting management
- **Meeting Links**: Auto-generated secure meeting URLs

### 🏢 Company Showcase
- **Executive Dashboard**: Key metrics and impact indicators
- **Dynamic Metrics**: Real-time company performance data
- **Testimonials**: Customer success stories and social proof
- **Media Coverage**: Press mentions and awards
- **Investment Summary**: Downloadable one-pagers

### 🔒 Security & Compliance
- **TLS/SSL Encryption**: Secure data in transit
- **MongoDB Encryption**: Data at rest protection
- **GDPR Compliance**: Data export and deletion capabilities
- **Audit Trails**: Complete security logging
- **IP Tracking**: Monitor access locations

---

## 🏗 Architecture

```
┌─────────────────┐
│   FastAPI API   │
│   (Python)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼────┐ ┌─▼──────────┐
│MongoDB │ │   Redis    │
│Database│ │   Cache    │
└────────┘ └────────────┘
```

**Tech Stack:**
- **Backend**: FastAPI (Python 3.9+)
- **Database**: MongoDB Atlas
- **Cache**: Redis (optional)
- **File Storage**: Local/Cloud storage
- **Email**: SMTP (Gmail/SendGrid)
- **Notifications**: Slack Webhooks

---

## 📦 Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (or local MongoDB)
- SMTP email account (Gmail recommended)
- Redis (optional, for caching)
- 2GB RAM minimum
- 10GB storage minimum

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/p-mensah/dataroom_backend_api.git
cd dataroom_backend_api
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Required Folders

```bash
# Windows
mkdir uploads\documents
type nul > models\__init__.py
type nul > routers\__init__.py
type nul > services\__init__.py
type nul > utils\__init__.py

# macOS/Linux
mkdir -p uploads/documents
touch models/__init__.py routers/__init__.py services/__init__.py utils/__init__.py
```

---

## ⚙️ Configuration

### 1. Create `.env` File

Create a `.env` file in the root directory:

```env
# Application
APP_NAME=SAYeTECH Investor Dataroom

# MongoDB
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/investor_dataroom?retryWrites=true&w=majority
DATABASE_NAME=investor_dataroom

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Admin
ADMIN_EMAIL=admin@sayetech.com

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production

# File Upload
UPLOAD_DIR=uploads/documents
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=[".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx"]

# Redis (optional)
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Slack (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Calendly (optional)
CALENDLY_API_KEY=your-calendly-api-key
```

### 2. MongoDB Atlas Setup

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database user
3. Whitelist your IP (or use `0.0.0.0/0` for testing)
4. Get your connection string
5. Replace `username`, `password`, and `cluster` in the connection string

### 3. Gmail App Password (for Email)

1. Enable 2-Factor Authentication on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an app password
4. Use this password in `SMTP_PASSWORD`

---

## 💾 Database Setup

The application will automatically create indexes on startup. To manually verify:

```python
from database import create_indexes
create_indexes()
```

**Collections Created:**
- `access_requests` - Investor access requests
- `access_tokens` - Active access tokens
- `investors` - Investor profiles
- `documents` - Uploaded documents
- `document_access` - Document view/download logs
- `qa_threads` - Q&A questions
- `qa_responses` - Q&A answers
- `meetings` - Scheduled meetings
- `alert_configs` - Alert configurations
- `alert_logs` - Triggered alerts
- `search_history` - Search queries
- `company_metrics` - Company KPIs
- `testimonials` - Customer testimonials
- `admin_users` - Admin accounts
- `audit_logs` - System audit trail

---

## 🚀 Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Access the API:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

## 📚 API Documentation

### Core Endpoints

#### Access Requests
```http
POST   /api/access-requests          # Submit access request
GET    /api/access-requests/{id}     # Get request details
GET    /api/admin/access-requests    # List all requests (admin)
PUT    /api/admin/access-requests/{id} # Update request status
```

#### Documents
```http
POST   /api/documents/upload          # Upload document
GET    /api/documents/search          # Search documents
GET    /api/documents/{id}            # Get document details
POST   /api/documents/{id}/download   # Download document
GET    /api/documents/categories/list # List categories
GET    /api/documents/suggestions     # Get search suggestions
```

#### Q&A
```http
POST   /api/qa/threads                    # Create question
GET    /api/qa/threads                    # List questions
POST   /api/qa/threads/{id}/respond       # Answer question
GET    /api/qa/threads/search             # Search Q&A
```

#### Meetings
```http
POST   /api/meetings/schedule             # Schedule meeting
GET    /api/meetings/available-slots      # Get available times
GET    /api/meetings/investor/{id}        # Get investor meetings
PUT    /api/meetings/{id}/cancel          # Cancel meeting
PUT    /api/meetings/{id}/reschedule      # Reschedule meeting
```

#### Analytics
```http
GET    /api/analytics/dashboard           # Dashboard stats
GET    /api/analytics/heatmap             # Document heatmap
GET    /api/analytics/investor/{id}/activity # Investor activity
GET    /api/analytics/investors/list      # All investor activities
GET    /api/analytics/export              # Export CSV report
```

#### Company
```http
GET    /api/company/metrics               # Get company metrics
POST   /api/company/metrics               # Update metrics
GET    /api/company/testimonials          # Get testimonials
POST   /api/company/testimonials          # Add testimonial
```

#### Alerts
```http
POST   /api/alerts/config                 # Create alert config
GET    /api/alerts/config                 # List alert configs
GET    /api/alerts/logs                   # Get alert logs
```

---

## 📁 Project Structure

```
dataroom_backend_api/
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── database.py                # MongoDB connection
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── models/                    # Pydantic models
│   ├── __init__.py
│   ├── access_request.py
│   ├── access_token.py
│   ├── investor.py
│   ├── document.py
│   ├── qa.py
│   ├── meeting.py
│   ├── analytics.py
│   └── audit_log.py
├── routers/                   # API route handlers
│   ├── __init__.py
│   ├── access_requests.py
│   ├── admin.py
│   ├── documents.py
│   ├── qa.py
│   ├── meetings.py
│   ├── analytics.py
│   ├── company.py
│   └── alerts.py
├── services/                  # Business logic
│   ├── __init__.py
│   ├── email_service.py
│   ├── auth_service.py
│   ├── document_service.py
│   ├── analytics_service.py
│   ├── alert_service.py
│   └── meeting_service.py
├── utils/                     # Helper functions
│   ├── __init__.py
│   └── helpers.py
└── uploads/                   # File storage
    └── documents/
```

---

## 💡 Usage Examples

### 1. Submit Access Request

```python
import requests

response = requests.post("http://localhost:8000/api/access-requests", json={
    "email": "investor@example.com",
    "full_name": "John Doe",
    "company": "Investment Firm LLC",
    "phone": "+1234567890",
    "message": "Interested in learning more about SAYeTECH"
})

print(response.json())
# {"message": "Access request submitted successfully", "id": "..."}
```

### 2. Search Documents

```python
response = requests.get("http://localhost:8000/api/documents/search", params={
    "query": "financial statements",
    "category": "financials",
    "investor_id": "investor_123"
})

documents = response.json()
```

### 3. Schedule Meeting

```python
response = requests.post("http://localhost:8000/api/meetings/schedule", json={
    "scheduled_at": "2025-01-15T14:00:00",
    "duration_minutes": 30,
    "notes": "Q4 investment discussion"
}, params={"investor_id": "investor_123"})
```

### 4. Get Analytics Dashboard

```python
response = requests.get("http://localhost:8000/api/analytics/dashboard")
stats = response.json()
print(f"Active users: {stats['active_users']}")
```

---

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt with salt
- **Input Validation**: Pydantic model validation
- **File Type Validation**: Whitelist-based file uploads
- **Rate Limiting**: Prevent abuse (configurable)
- **CORS Protection**: Configurable origins
- **SQL Injection Prevention**: MongoDB parameterized queries
- **XSS Protection**: Input sanitization
- **HTTPS**: TLS/SSL encryption in production

---

## 🌐 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t dataroom-api .
docker run -p 8000:8000 --env-file .env dataroom-api
```

### Production Checklist

- [ ] Change `SECRET_KEY` to a secure random string
- [ ] Set specific CORS origins (not `*`)
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up MongoDB backups
- [ ] Configure Redis for caching
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Enable rate limiting
- [ ] Set up CDN for static files
- [ ] Configure firewall rules
- [ ] Set up automated backups

---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

---

## 📈 Performance Optimization

- **Database Indexing**: Automatically created on startup
- **Caching**: Redis caching for frequently accessed data
- **CDN**: Serve static files via CDN
- **Compression**: Gzip response compression
- **Connection Pooling**: MongoDB connection pooling
- **Async Operations**: Non-blocking file operations

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary and confidential. All rights reserved by SAYeTECH.

---

## 📞 Support

For questions or issues:
- **Email**: admin@sayetech.com
- **GitHub Issues**: [Create an issue](https://github.com/p-mensah/dataroom_backend_api/issues)
- **Documentation**: [Full docs](https://docs.sayetech.com)

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Python](https://www.python.org/)

---

**Made with ❤️ by the SAYeTECH Team**