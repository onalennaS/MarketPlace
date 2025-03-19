from functools import wraps
from django.shortcuts import redirect
from seller.wrap_models.product_model import ProductModeration
# Check if uer is authenticated  decorator
# redirect unauthenticated to sign in page
def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('signin')  # Redirect to login page if not authenticated
    return _wrapped_view



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

def email_pending(subject,recipient_email,link,template,reason=None ):
    try:
        user = User.objects.values('username').get(email=recipient_email[1])
    except User.DoesNotExist:
        logger.error(f"No user found with email: {recipient_email[1]}")
        return False  # Return failure if user doesn't exist

    email_content = render_to_string(f"moderator/email/{template}.html", {'user': user, 'link': link, 'reason':reason })
    text_content = strip_tags(email_content)  # Plain text fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_email,
    )
    email.attach_alternative(email_content, "text/html")  # Attach HTML version
    email.send()

    #logger.info(f"Your Business Registration is Under Review email sent to {recipient_email[0]} and {recipient_email[1]}")
    return True  # Indicate success


def send_email_pending_to_user(product):
    emails = [product.business.email, product.business.owner.email]
    page_link = f"{settings.SITE_URL}seller/view_product/{product.id}"
    email_pending( "Product submission revieved", emails, page_link,"user_product_pending")

def send_email_approve_to_user(product):
    emails = [product.business.email, product.business.owner.email]
    page_link = f"{settings.SITE_URL}seller/view_product/{product.id}"
    email_pending("Product Approved",emails, page_link,"user_product_approve")

def send_email_reject_to_user(product):
    emails = [product.business.email, product.business.owner.email]
    page_link = f"{settings.SITE_URL}seller/view_product/{product.id}"
    moderation = ProductModeration.objects.filter(product=product).last()
    email_pending("Product Rejected", emails, page_link,"user_product_reject",moderation.reason)


def send_email_pending_to_moderator(product):
    emails = [product.product_moderation.moderator.email]
    page_link = f"{settings.SITE_URL}moderator/view_product_moderator/{product.id}"
    email_pending(emails, page_link,"moderator_product_pending")

def send_email_approve_to_moderator(product):
    emails = [product.product_moderation.moderator.email]
    page_link = f"{settings.SITE_URL}moderator/view_product_moderator/{product.id}"
    email_pending(emails, page_link,"moderator_product_approve")

def send_email_reject_to_moderator(product):
    emails = [product.product_moderation.moderator.email]
    page_link = f"{settings.SITE_URL}moderator/view_product_moderator/{product.id}"
    email_pending(emails, page_link,"moderator_product_reject")