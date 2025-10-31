from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
import os
import pickle
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from functools import wraps

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

User = get_user_model()
logger = logging.getLogger(__name__)


def get_gmail_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def send_email_via_gmail(to, subject, html_content, text_content):
    try:
        service = get_gmail_service()
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = settings.EMAIL_HOST_USER
        message['subject'] = subject
        message.attach(MIMEText(text_content, 'plain'))
        message.attach(MIMEText(html_content, 'html'))
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        logger.info(f"Email sent to {to} via Gmail API")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {str(e)}")
        return False


def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login page if not authenticated
    return _wrapped_view



def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except Exception:
        return None


def send_email_verification_link(recipient_email, verify_link):
    try:
        user = User.objects.values('username','email').get(email=recipient_email)
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("authentication/email_activate_account_template.html", {'user': user, 'verify_link': verify_link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    success = send_email_via_gmail(recipient_email, "Verify Your Email", email_content, text_content)

    if success:
        logger.info(f"Verification email sent to {recipient_email}")
        return True  # Indicate success
    else:
        return False

def send_verify_email(email):
    reset_token = generate_reset_token(email)
    reset_link = f"{settings.SITE_URL}/auth/verify_email/{reset_token}/"
    print("================")
    print(reset_link)
    send_email_verification_link(email, reset_link)



def send_gmail_verification_link(recipient_email, verify_link):
    try:
        user = User.objects.values('username','email').get(email=recipient_email)
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("authentication/gmail_activate_account_template.html", {'user': user, 'verify_link': verify_link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    success = send_email_via_gmail(recipient_email, "Verify Your Email", email_content, text_content)

    if success:
        logger.info(f"Verification email sent to {recipient_email}")
        return True  # Indicate success
    else:
        return False

def send_verify_gmail(email):

    reset_link = f"{settings.SITE_URL}/home/"
    print("================")
    print(reset_link)
    send_gmail_verification_link(email, reset_link)


def send_email_reset_link(recipient_email, reset_link):
    try:
        user = User.objects.values('first_name').get(email=recipient_email)
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("authentication/email_reset_password_template.html", {'user': user, 'reset_link': reset_link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    success = send_email_via_gmail(recipient_email, "Reset Your Password", email_content, text_content)

    if success:
        logger.info(f"Password reset email sent to {recipient_email}")
        return True  # Indicate success
    else:
        return False


def verify_role(user):
    

    if user.groups.filter(name="admin").exists():
        return 'admin_dashboard'

    if user.groups.filter(name="moderator").exists():
        return 'moderator'


    if user.groups.filter(name="business").exists():
        return 'business'


    if user.groups.filter(name="courier").exists():
        return 'courier_orders'


    if user.groups.filter(name="customer").exists():
        return 'shop_base'

    group = Group.objects.filter(name="customer").first()

    if group and user:
        user.groups.add(group)
        user.save()
        return 'shop_base'
    else:
        return 'shop_base'