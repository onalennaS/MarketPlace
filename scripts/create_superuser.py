import os
import sys
import secrets
from pathlib import Path

# Ensure project root is on sys.path when running from scripts/
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Market.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists.")
else:
    password = secrets.token_urlsafe(12)
    User.objects.create_superuser(username=username, email=email, password=password)
    print('CREATED_SUPERUSER')
    print('username:', username)
    print('email   :', email)
    print('password:', password)
