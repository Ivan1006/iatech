# IA Tech - Página Web

Django marketing/contact website for IA Tech, an automation and process optimization company.

## Project Structure

```
paginaweb/
├── iatech/          # Django project config (settings, urls, wsgi, asgi)
├── home/            # Single Django app
│   ├── views.py     # Index view + contact form email handling
│   ├── urls.py      # Routes: / → home
│   ├── templates/home/index.html  # Landing page (Bootstrap 5)
│   └── static/home/ # Logo assets (PNG variants)
├── manage.py
├── db.sqlite3
└── .env             # Local config (not committed)
```

## Common Commands

```bash
# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

## Configuration

Settings are loaded from `.env` in the project root. Copy and fill in:

```
DEBUG=True
SECRET_KEY=change-this-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# Gmail SMTP for contact form
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
CONTACT_EMAIL=contacto@tuempresa.com
```

## Key Details

- **Stack:** Django 6.0.1, Python 3.x, Bootstrap 5.3.2, SQLite
- **No custom models** — the `home` app has no ORM models
- **Contact form** (`POST /`): sends email via Gmail SMTP using `send_mail()`
- **Frontend:** Single template (`index.html`, ~390 lines) with Space Grotesk font, cyan/blue color scheme, scroll animations via Intersection Observer API
- **No requirements.txt** — install Django manually or add one if needed
