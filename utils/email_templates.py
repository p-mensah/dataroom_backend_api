# Placeholder functions for email body content

def get_confirmation_email_template() -> str:
    """Returns the default confirmation email body."""
    return """
    <h2>Thank you for your request</h2>
    <p>We have received your access request and are reviewing it.</p>
    <p>You will receive an update shortly.</p>
    """

def get_approval_email_template() -> str:
    """Returns the default approval email body."""
    return """
    <h2>Access Approved</h2>
    <p>Your access has been granted. Please use the link provided in the main approval email.</p>
    """

def get_denial_email_template() -> str:
    """Returns the default denial email body."""
    return """
    <h2>Access Request Update</h2>
    <p>Unfortunately, we cannot approve your request at this time.</p>
    """

def get_admin_alert_template() -> str:
    """Returns the default admin alert email body for new requests."""
    return """
    <h2>New Request Alert</h2>
    <p>A new access request has been submitted and requires admin review.</p>
    """