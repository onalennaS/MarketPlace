import base64
import pickle
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from functools import wraps
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

User = get_user_model()
logger = logging.getLogger(__name__)

# ====================
# Gmail API Setup
# ====================
def get_gmail_service():
    """Load Gmail API service using saved token."""
    with open('token.pkl', 'rb') as token:
        creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_gmail_message(to, subject, html_content, text_content=None):
    """Send email via Gmail API."""
    service = get_gmail_service()

    if not text_content:
        text_content = strip_tags(html_content)

    message = MIMEText(html_content, "html")
    message['to'] = ", ".join(to)
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()

    logger.info(f"Email sent to {to}, Message ID: {send_result['id']}")
    return True


# ====================
# Custom Decorators
# ====================
def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('signin')
    return _wrapped_view

def has_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.password.startswith("pbkdf2"):
            return view_func(request, *args, **kwargs)
        return redirect('create_password')
    return _wrapped_view


# ====================
# Email Functions
# ====================
def email_order_confirmation_user(recipient_email, link, order, extras, order_items, total, discount):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[0]}")
        return False

    subject = f"Order {order.order_id} Confirmation"
    email_content = render_to_string(
        "home/email/order_placed.html",
        {'order': order, 'total': total, 'user': user, 'link': link, 'extras': extras, 'order_items': order_items, 'discount': discount}
    )

    send_gmail_message(recipient_email, subject, email_content)
    return True


def email_order_confirmation_business(user_email, recipient_email, link, order, extras, order_items, total, discount):
    try:
        user = User.objects.values('username').get(email=user_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {user_email[0]}")
        return False

    subject = f"Order {order.order_id} Confirmation"
    email_content = render_to_string(
        "home/email/business_order_placed.html",
        {'order': order, 'total': total, 'user': user, 'link': link, 'extras': extras, 'order_items': order_items, 'discount': discount}
    )

    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_order_confirmation(order, extras, order_items, total, discount):
    user_email = [order.user.email]
    business_email = [order.business.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    business_page_link = f"{settings.SITE_URL}/seller/orders/{order.business.id}"

    email_order_confirmation_user(user_email, page_link, order, extras, order_items, total, discount)
    email_order_confirmation_business(user_email, business_email, business_page_link, order, extras, order_items, total, discount)
