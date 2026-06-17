# MarketPlace (Django)

A Django-based marketplace web application.

> Note: This repository uses Django 5.1.x and includes multiple apps (auth, seller, shop, courier, transactions, moderator, etc.).

## Features (high level)
- User authentication (custom user model + django-allauth social login)
- Seller/business profiles
- Product browsing/listing (shop)
- Courier delivery workflow (courier)
- Moderation (moderator)
- Transactions/payment integration (Paystack config present)

## Prerequisites
- Python 3.10+
- pip

## Setup (local development)

### 1) Create and activate a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Environment variables
This project uses `python-decouple` for settings. At minimum you may need:
- `SECRET_KEY` (it has a default for local runs)
- Optional payment/email settings:
  - `PAYSTACK_MAIN_ACCOUNT`
  - `PAYSTACK_SECRET_KEY`
  - `EMAIL_HOST_USER`
  - `DATABASE_URL` (used only when `DEBUG=False`)

### 4) Migrate and run the server
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open:
- http://127.0.0.1:8000

## Admin
Create a superuser:
```powershell
python scripts/create_superuser.py
```
(or use `python manage.py createsuperuser` if preferred)

## Project structure
- `Market/` - Django project settings and routing
- `authenticator/` - authentication utilities/adapters and supporting code
- `user/` - custom user models/views
- `seller/` - seller business models and views
- `shop/` - product browsing/templates
- `courier/` - courier models/views
- `moderator/` - moderation views
- `transactions/` - transaction models/views

## Static & media
- Static files are served from `static/` and collected into `staticfiles/`.
- Uploaded media is stored under `media/`.

## Testing
```powershell
python manage.py test
```

## Troubleshooting
- If you see issues related to `DATABASE_URL`, ensure `DEBUG=True` in `Market/settings.py` (local) or provide a valid `DATABASE_URL`.
- Social login requires valid Google OAuth credentials configured via environment variables as expected by `django-allauth` (see relevant settings/adapters).

## License
MIT (or add your preferred license here).

