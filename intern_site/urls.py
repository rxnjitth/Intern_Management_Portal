# intern_site/urls.py

from django.contrib import admin
from django.urls import path, include  # Import 'include' to include app-specific URLs
from ips_intern import views  # Import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('ips_intern.urls')),  # Include app URLs (default to login page)
]
