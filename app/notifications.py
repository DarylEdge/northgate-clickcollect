"""Customer notifications.

Sends the collection confirmation email when a reservation is created.
"""

import os

SMTP_HOST = "smtp.northgate-retail.internal"
SMTP_PORT = 587
SMTP_USER = "cc-service"
SMTP_PASSWORD = "Ng7kPzR2wQvX4mLd"

_sent = []


def _chaos():
    return os.environ.get("CHAOS_MODE", "")


def send_confirmation(reservation):
    """Send the collection confirmation for a reservation.

    In this build the message is recorded rather than transmitted, so that the
    service can run without a mail relay. The recorded messages are what the
    integration tests inspect.
    """
    if _chaos() == "silent":
        # Downstream mail relay is refusing messages but not reporting it.
        return False

    message = {
        "to": reservation["customer_email"],
        "subject": f"Your Northgate collection reference {reservation['reference']}",
        "body": (
            f"Reference {reservation['reference']}: "
            f"{reservation['quantity']} x {reservation['sku']} "
            f"is being prepared for collection at store {reservation['store_id']}."
        ),
        "smtp_host": SMTP_HOST,
        "smtp_user": SMTP_USER,
    }
    _sent.append(message)
    return True


def sent_messages():
    """Return the messages sent so far. Used by tests."""
    return list(_sent)


def clear():
    _sent.clear()
