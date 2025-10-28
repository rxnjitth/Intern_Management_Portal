# Intern Management Portal

Professional Intern Management Portal for IPS Tech Community — a Django-based application to manage intern applications, task reports, certification workflow, and admin/intern dashboards.

This repository includes the application code, templates, static assets (CSS/JS/images), Docker configuration and scripts for local and containerized deployment.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick start (Docker)](#quick-start-docker)
- [Local development (PowerShell)](#local-development-powershell)
- [Environment variables](#environment-variables)
- [Database migrations & creating a superuser](#database-migrations--creating-a-superuser)
- [Static files & media](#static-files--media)
- [Running tests](#running-tests)
- [Certificate generation](#certificate-generation)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License & Contact](#license--contact)

---

## Features

- Role-based dashboards (Admin and Intern)
- Intern application flow with course/duration selection
- Task reporting and progress tracking for interns
- Certificate generation (server-side image rendering)
- Dark / Light theme toggle on dashboards
- Docker and docker-compose support for quick deployment

## Tech Stack

- Django (Python)
- Pillow (PIL) for image-based certificate creation
- reportlab available in requirements for PDF tasks
- Bootstrap + Font Awesome for the UI
- Docker / Docker Compose for containerization

## Prerequisites

- Docker & Docker Compose (for containerized quick start)
- Python 3.10+ for local development
- Git

## Quick start (Docker)

From the project root on a machine with Docker and Docker Compose installed:

```powershell
# Build and start services in detached mode
docker compose up --build -d

# Follow logs
docker compose logs -f
```

Open `http://localhost:8000/` (or the port configured in `docker-compose.yml`).

## Local development (PowerShell)

1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure environment variables (see below) and run migrations:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Optional: Collect static files for production testing:

```powershell
python manage.py collectstatic --noinput
```

## Environment variables

Typical environment variables you may want to set (use an `.env` file or set them in your container):

- `DJANGO_SECRET_KEY` — Django secret key
- `DJANGO_DEBUG` — `True` or `False`
- `DATABASE_URL` — database connection URL (optional)
- Email settings (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) if email sending is required

When running with Docker Compose you can pass these through the compose file or an `.env` file.

## Database migrations & creating a superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

## Static files & media

- Static files (CSS/JS/fonts/images) live under `ips_intern/static/`.
- Templates are in `ips_intern/templates/`.
- Uploaded/generated media files (e.g., generated certificates) are stored in `media/` (see `media/certificates/`).

In production, configure a proper static/media hosting solution (CDN or cloud storage) and serve static files with your web server.

## Running tests

Run Django tests with:

```powershell
python manage.py test
```

## Certificate generation

Certificates are generated from a template image:

```
ips_intern/static/images/certificate.png
```

When a certificate is generated, the app draws the intern's name on the template using Pillow and saves the output to `media/certificates/`. If you see an incorrect or hardcoded name in generated certificates, ensure the intern's `name` field in the database is populated (the app falls back to the username when `name` is empty).

## Project structure (important files)

- `manage.py` — Django CLI entrypoint
- `ips_intern/` — main app: models, views, templates, static
- `ips_intern/templates/` — HTML templates (admin/intern dashboards)
- `ips_intern/static/` — static assets
- `Dockerfile`, `docker-compose.yml` — container configuration
- `requirements.txt` — Python dependencies

## Contributing

1. Fork the repository and create a branch:

```powershell
git checkout -b feature/your-feature
```

2. Implement your changes and add tests where appropriate.
3. Run tests locally and ensure the code follows the repo style.
4. Open a pull request with a clear description of the change.

If you'd like, I can add a CONTRIBUTING.md with an explicit checklist and PR template.

## License & Contact

This project is maintained by IPS Tech Community. Add your preferred license (e.g., MIT) to the repository if required.

For questions or support, contact: `ipstechcommunity@kgkite.ac.in` or open an issue in this repo.

---

Thanks for using the Intern Management Portal. If you want, I can add badges (build, coverage), screenshots, or CI/CD examples next.

