FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    build-essential \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell


# Replace CMD or ENTRYPOINT with this:
CMD ["sh", "-c", "python manage.py migrate && gunicorn intern_site.wsgi:application --bind 0.0.0.0:8000"]

