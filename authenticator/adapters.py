
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the social account already exists, no action is needed
        if sociallogin.is_existing:
            return
        
        # Try to connect this social account to an existing user by email
        user_email = sociallogin.account.extra_data.get('email')
        if user_email:
            try:
                user = User.objects.get(email__iexact=user_email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass