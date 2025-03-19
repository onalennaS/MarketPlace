from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
User = get_user_model()

def email_pending(recipient_email,link ):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("seller/new/email/business_pending.html", {'user': user, 'link': link })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Your Business Registration is Under Review",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_pending(business):
    emails = [business.email, business.owner.email]

    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_pending(emails, page_link)


def email_reject(recipient_email,link ):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("seller/new/email/business_reject.html", {'user': user, 'link': link })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Update on Your Business Registration Request",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_reject(business):
    emails = [business.email, business.owner.email]

    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_reject(emails, page_link)


def email_approve(recipient_email,link ):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("seller/new/email/business_aprove.html", {'user': user, 'link': link })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Update on Your Business Registration Request",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_approve(business):
    emails = [business.email, business.owner.email]

    page_link = f"{settings.SITE_URL}/seller/business/"
    email_approve(emails, page_link)


def email_appeal(recipient_email,link ):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("seller/new/email/business_appeal.html", {'user': user, 'link': link })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Appeal Request Received",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_appeal(business):
    emails = [business.email, business.owner.email]

    page_link = f"{settings.SITE_URL}/seller/business_status/{business.id}"
    email_appeal(emails, page_link)
