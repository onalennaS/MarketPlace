from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests
from django.conf import settings

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
