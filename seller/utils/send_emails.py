from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

from django.contrib.auth.models import User, Group

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

    email_content = render_to_string("seller/new/email/business_approve.html", {'user': user, 'link': link })
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



def email_order_traking_update(recipient_email,link,order):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist
    eta = ""
    description = ""
    descsription2 = ""
    if order.status == "Processing":
        description = "being prepared"
        eta = "1 hour"
        descsription2 = "acknowladged, our chefs are  preparing it for you!"
    if order.status == "On route":
        description = "on the way"
        descsription2 = "Completed , our Courier is on the way to deliver your order right now!"
        eta = "30 minutes"

    email_content = render_to_string("seller/new/email/order_tracking.html", {'order':order,'user': user, 'link': link, 'description':description, 'descsription2':descsription2, 'eta':eta })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=f"Order Tracking Update {order.status.upper()}",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True

def send_email_order_traking_update(order ):
    emails = [order.user.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    email_order_traking_update(emails, page_link, order)


def email_order_delivered(recipient_email,link,order):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist
   
    email_content = render_to_string("seller/new/email/order_delivered.html", {'order':order,'user': user, 'link': link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=f"Order Delivered",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True

def send_email_order_delivered(order):
    emails = [order.user.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    email_order_delivered(emails, page_link, order)


def email_new_order(recipient_email,link,order):# Return failure if user doesn't exist
   
    email_content = render_to_string("seller/new/email/new_order.html", {'order':order, 'link': link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=f"New Order",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True


def send_email_new_order(order):
    courier_group = Group.objects.get(name="courier")
    users = courier_group.user_set.all()
    emails = [user.email for user in users if user.email]

    if emails:
        page_link = f"{settings.SITE_URL}/courier/courier_orders/"
        email_new_order(emails, page_link, order)
    return True