from django.shortcuts import render, redirect
from functools import wraps
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
User = get_user_model()

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('signin')  # Redirect to login page if not authenticated
    return _wrapped_view

def has_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.password.startswith("pbkdf2"):
            return view_func(request, *args, **kwargs)
        return redirect('create_password')
    return _wrapped_view


def email_order_confirmation(recipient_email,link,order,extras, order_items,total):
    try:
        user = User.objects.values('username').get(email=recipient_email[0])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("home/email/order_placed.html", {'order':order,'total':total,'user': user, 'link': link ,'extras':extras,'order_items':order_items,'discount':discount})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=f"Order {order.order_id} Confirmation ",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True

def send_email_order_confirmation(order,extras, order_items, total,discount ):
    emails = [order.user.email,order.business.email, order.business.owner.email]
    page_link = f"{settings.SITE_URL}/account/dashboard/track_orders/{order.id}"
    email_order_confirmation(emails, page_link, order, extras, order_items, total,discount)
