from django.contrib import admin
from django.urls import path
from ips_intern import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.custom_login, name='login'),  # Login page
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('intern_dashboard/', views.intern_dashboard, name='intern_dashboard'),  # Intern dashboard
    path('logout/', views.custom_logout, name='logout'),

]
