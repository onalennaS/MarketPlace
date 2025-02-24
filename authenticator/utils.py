from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

User = get_user_model()
logger = logging.getLogger(__name__)


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
        user = User.objects.values('username').get(email=recipient_email)
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("authentication/email_activate_account_template.html", {'user': user, 'verify_link': verify_link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Verify Your Email",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    logger.info(f"Password reset email sent to {recipient_email}")
    return True  # Indicate success

def send_verify_email(email):
    reset_token = generate_reset_token(email)
    reset_link = f"{settings.SITE_URL}/auth/verify_email/{reset_token}/"
    send_email_verification_link(email, reset_link)


def send_email_reset_link(recipient_email, reset_link):
    try:
        user = User.objects.values('first_name').get(email=recipient_email)
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string("authentication/email_reset_password_template.html", {'user': user, 'reset_link': reset_link})
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject="Reset Your Password",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    logger.info(f"Password reset email sent to {recipient_email}")
    return True  # Indicate success

