# SAYeTECH Investor Dataroom API

This is the backend API for the SAYeTECH Investor Dataroom. It provides a secure and efficient way to manage access requests to the dataroom, ensuring that only authorized individuals can view sensitive investor documents.

## About The Project

The SAYeTECH Investor Dataroom API is a FastAPI-based application that manages access to a secure online dataroom. It provides the following features:

*   **Access Request Management**: Allows potential investors to request access to the dataroom.
*   **Admin Dashboard**: Provides an admin interface for managing access requests, approving or denying them, and setting expiration dates for access tokens.
*   **Secure Token Generation**: Generates secure, time-sensitive tokens for authorized users to access the dataroom.
*   **Email Notifications**: Automatically sends email notifications to users and admins for various events, such as new access requests, approvals, and denials.
*   **Audit Logging**: Logs all important actions for security and compliance purposes.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8+
*   MongoDB

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/your_username/dataroom_backend_api.git
    ```
2.  **Create a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python packages**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the root directory and add the following environment variables:
    ```
    APP_NAME="SAYeTECH Investor Dataroom"
    MONGODB_URL="your_mongodb_url"
    DATABASE_NAME="investor_dataroom"
    SMTP_HOST="your_smtp_host"
    SMTP_PORT=587
    SMTP_USER="your_smtp_user"
    SMTP_PASSWORD="your_smtp_password"
    FROM_EMAIL="your_from_email"
    ADMIN_EMAIL="your_admin_email"
    SECRET_KEY="your_secret_key"
    ```

## Usage

To run the application, use the following command:

```sh
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

The following are the available API endpoints:

### Access Requests

*   `POST /api/access-requests/`: Creates a new access request.
*   `GET /api/access-requests/{request_id}`: Retrieves a specific access request by its ID.

### Admin

*   `GET /api/admin/access-requests`: Lists all access requests, optionally filtering by status.
*   `PUT /api/admin/access-requests/{request_id}`: Updates an access request's status and admin notes.
