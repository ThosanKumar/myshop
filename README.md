# myshop2 - Minimal E-commerce Django Starter

This is a minimal Django-based e-commerce starter with:
- Product listing and detail
- Shopping cart (session-based)
- Order processing (simple order model)
- User registration and login (Django auth)

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd myshop
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` to view the store.

