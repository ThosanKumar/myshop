# myshop2 - Minimal E-commerce Django Starter

This is a minimal Django-based e-commerce starter with:
- Product listing and detail
- Shopping cart (session-based)
- Order processing (simple order model)
- User registration and login (Django auth)

This repository can be published to GitHub Pages as a static snapshot. GitHub Pages only serves static files, so we export a mirrored static copy of the site and publish that to the `gh-pages` branch. Dynamic server-side features (forms, sessions, user login, server-rendered POST endpoints) will not function on the static site.

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

What I added to support publishing to GitHub Pages:

- `.github/workflows/deploy-gh-pages.yml` — GitHub Actions workflow that starts a dev server in the runner, uses `wget` to mirror the site, and publishes the mirrored files to `gh-pages` using `peaceiris/actions-gh-pages`.
- `scripts/export_static.sh` — local script that runs the dev server, mirrors the site with `wget`, and writes the export into `export/<PORT>`.

Quick local export (Linux / macOS / WSL):

```bash
./scripts/export_static.sh 8000
```

Windows (PowerShell) guidance:

1. In PowerShell, create and activate your virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and collect static files:

```powershell
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

3. Start the dev server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

4. From Git Bash, WSL, or another environment with `wget`, mirror the site (recommended):

```bash
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --directory-prefix=export/8000 http://127.0.0.1:8000/
```

Notes and limitations:

- The exported site is static. Any features that require server execution, database writes, or user sessions will not work on GitHub Pages. The export works best for browsing product pages and static content.
- The workflow uses the Django dev server on the Actions runner. It's a pragmatic approach for a static export but not suitable for production dynamic hosting.
- If you need a live Django app, consider Render, Fly.io, Railway, or a container-based deployment.

If you'd like, I can also:
- Add a small README badge that links to the published GitHub Pages URL once `gh-pages` is created.
- Improve the export to pre-render certain pages or crawl additional URLs.

