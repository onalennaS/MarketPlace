from django.shortcuts import render, redirect
from functools import wraps
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
import re
from datetime import datetime
User = get_user_model()


def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login page if not authenticated
    return _wrapped_view




def validate_full_name(full_name):
    return bool(full_name.strip()) and len(full_name) >= 3

def validate_dob(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = (today - birth_date).days // 365
        return age >= 16  # Must be 16+ years old
    except ValueError:
        return False

def validate_phone(phone):
    pattern = r"^(\+27|0)[6-8][0-9]{8}$"
    return re.match(pattern, phone) is not None

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_address(address):
    return bool(address.strip())

def validate_file_uploaded(file):
    return file is not None

def validate_sa_id(id_number):
    """
    Validate South African ID:
    - 13 digits
    - Luhn algorithm check
    """
    if not id_number.isdigit() or len(id_number) != 13:
        return False

    # Luhn algorithm for checksum
    def luhn_checksum(id_num):
        digits = [int(d) for d in id_num]
        odd_sum = sum(digits[-1::-2])
        even_sum = sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
        return (odd_sum + even_sum) % 10 == 0

    return luhn_checksum(id_number)

def validate_transport(transport):
    valid_options = ['Skateboard', 'Bicycle', 'Hoverboard', 'Roller Blades', 'Car', 'Motorcycle', 'Walking']
    return transport.capitalize() in valid_options

def validate_agreements(terms, privacy, conduct):
    return terms and privacy and conduct




def email_withdrawal(recipient_email,link, user,ref):
   

    email_content = render_to_string("seller/new/email/withdrawal.html", {'user': user, 'link': link,'ref':ref })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Withdrwal transaction",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_withdrawal(user,ref):
    emails = [user.email, 'support@onecartdiscovery.com']
    page_link = f"{settings.SITE_URL}/courier/courier_earnings/"
    email_withdrawal(emails, page_link,user,ref)





def email_withdrawal_failed(recipient_email,link, user,ref):
    email_content = render_to_string("seller/new/email/withdrawal_failed.html", {'user': user, 'link': link,'ref':ref })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Withdrwal transaction",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_withdrawal_failed(user,ref):
    emails = [user.email, 'support@onecartdiscovery.com']

    page_link = f"{settings.SITE_URL}/courier/courier_earnings/"
    email_withdrawal_failed(emails, page_link,user,ref)

    



def email_withdrawal_success(recipient_email,link, user,ref,amount):
    email_content = render_to_string("seller/new/email/withdrawal_success.html", {'user': user, 'link': link,'ref':ref,'amount':amount })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Withdrwal transaction",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success

def send_email_withdrawal_success(user,ref,amount):
    emails = [user.email, 'support@onecartdiscovery.com']

    page_link = f"{settings.SITE_URL}/courier/courier_earnings/"
    email_withdrawal_success(emails, page_link,user,ref,amount)