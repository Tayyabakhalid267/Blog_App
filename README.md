# Message Board

Simple Django message board. Users can post short messages and view them on the homepage. This repo contains a minimal, ready-to-run Django project.

Quick start (Windows PowerShell):

1. Create a virtual environment and install dependencies

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and create a superuser (for admin UI)

```powershell
python manage.py migrate
python manage.py createsuperuser
```

3. Run the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ to see the message board. Admin interface is at /admin/.
Login is available at /accounts/login/ and sign-up at /signup/.

To run tests:

```powershell
python manage.py test
```

Deploying to Heroku: create app, push, then scale web dyno. See Heroku docs. Make sure to set Python runtime in Pipfile or runtime.txt for production.
