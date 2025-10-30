import base64
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import logging

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
    service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()

    logger.info(f"Email sent successfully to {to}")
    return True


# ====================
# EMAIL FUNCTIONS
# ====================

def email_pending(recipient_email, link):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False

    subject = "Your Business Registration is Under Review"
    email_content = render_to_string("seller/new/email/business_pending.html", {'user': user, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_pending(business):
    emails = [business.email, business.owner.email]
    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_pending(emails, page_link)


def email_reject(recipient_email, link):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False

    subject = "Update on Your Business Registration Request"
    email_content = render_to_string("seller/new/email/business_reject.html", {'user': user, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_reject(business):
    emails = [business.email, business.owner.email]
    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_reject(emails, page_link)


def email_approve(recipient_email, link):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False

    subject = "Update on Your Business Registration Request"
    email_content = render_to_string("seller/new/email/business_approve.html", {'user': user, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_approve(business):
    emails = [business.email, business.owner.email]
    page_link = f"{settings.SITE_URL}/seller/business/"
    email_approve(emails, page_link)


def email_appeal(recipient_email, link):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False

    subject = "Appeal Request Received"
    email_content = render_to_string("seller/new/email/business_appeal.html", {'user': user, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_appeal(business):
    emails = [business.email, business.owner.email]
    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_appeal(emails, page_link)


def email_order_tracking_update(recipient_email, link, order):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[0]}")
        return False

    eta = ""
    description = ""
    description2 = ""

    if order.status == "Processing":
        description = "being prepared"
        eta = "35 mins"
        description2 = "acknowledged, our chefs are preparing it for you!"
    elif order.status == "On route":
        description = "on the way"
        eta = "15 minutes"
        description2 = "Completed, our courier is on the way to deliver your order!"

    subject = f"Order Tracking Update {order.status.upper()}"
    email_content = render_to_string("seller/new/email/order_tracking.html", {
        'order': order,
        'user': user,
        'link': link,
        'description': description,
        'description2': description2,
        'eta': eta
    })
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_order_traking_update(order):
    emails = [order.user.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    email_order_tracking_update(emails, page_link, order)


def email_order_delivered(recipient_email, link, order):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[0]}")
        return False

    subject = "Order Delivered"
    email_content = render_to_string("seller/new/email/order_delivered.html", {'order': order, 'user': user, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_order_delivered(order):
    emails = [order.user.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    email_order_delivered(emails, page_link, order)


def email_new_order(recipient_email, link, order):
    subject = "New Order"
    email_content = render_to_string("seller/new/email/new_order.html", {'order': order, 'link': link})
    send_gmail_message(recipient_email, subject, email_content)
    return True


def send_email_new_order(order):
    courier_group = Group.objects.get(name="courier")
    users = courier_group.user_set.all()
    emails = [user.email for user in users if user.email]

    if emails:
        page_link = f"{settings.SITE_URL}/courier/courier_orders/"
        email_new_order(emails, page_link, order)
    return True
