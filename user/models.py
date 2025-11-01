from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests
from django.conf import settings
import random
import string

class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_activities')
    login_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='Success')

    class Meta:
        ordering = ['-login_time']

    def save(self, *args, **kwargs):
        # Parse device from user_agent (simple parsing)
        ua = self.user_agent
        if 'Mobile' in ua or 'Android' in ua or 'iPhone' in ua:
            self.device = 'Mobile Device'
        elif 'Chrome' in ua:
            self.device = 'Desktop - Chrome'
        elif 'Safari' in ua:
            self.device = 'Desktop - Safari'
        else:
            self.device = 'Unknown Device'

        # Get location from IP (using free API)
        try:
            if self.ip_address != '127.0.0.1':  # Skip localhost
                response = requests.get(f'https://ipapi.co/{self.ip_address}/json/', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.location = f"{data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}"
                else:
                    self.location = 'Unknown Location'
            else:
                self.location = 'Localhost'
        except:
            self.location = 'Unknown Location'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class ReferralProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_profile')
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    is_referred = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=6, unique=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    timestamp = models.DateTimeField(default=timezone.now)
    view_clicks = models.PositiveIntegerField(default=0)
    signups = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)

    def generate_unique_referral_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_letters, k=6))
            if not ReferralProfile.objects.filter(referral_code=code).exists():
                return code

    def __str__(self):
        return f"{self.user.username}'s Referral Profile"

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_given')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received')
    timestamp = models.DateTimeField(default=timezone.now)
    is_rewarded = models.BooleanField(default=False)
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referral_type = models.CharField(max_length=20, choices=[('signup', 'Signup'), ('purchase', 'Purchase')])

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username} ({self.referral_type})"
