from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import LoginActivity

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def parse_user_agent(user_agent):
    if not user_agent:
        return 'Unknown Device'
    user_agent = user_agent.lower()
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        return 'Mobile Device'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'Tablet'
    else:
        return 'Desktop'

def get_location_from_ip(ip):
    # For now, return a placeholder. In production, you'd use a geolocation service
    return 'Unknown Location'

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    device = parse_user_agent(user_agent)
    location = get_location_from_ip(ip_address)

    LoginActivity.objects.create(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        device=device,
        location=location,
        status='Success'
    )
