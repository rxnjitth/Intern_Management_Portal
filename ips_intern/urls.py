from django.contrib import admin
from django.urls import path
from ips_intern import views

urlpatterns = [
    #admin urls
    path('admin/', admin.site.urls),
    path('', views.custom_login, name='login'),  # Login page
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('logout/', views.custom_logout, name='custom_logout'),
    path('interns/', views.all_interns_view, name='all_interns'),
    path('intern/<int:user_id>/', views.intern_detail_view, name='intern_detail'),
   
    path('intern/<int:user_id>/certify/<str:action>/', views.mark_certification, name='mark_certification'),
    path('internship_applications/', views.internship_applications, name='internship_applications'),
    path('internship_applications_list/', views.internship_applications_list, name='internship_applications_list'),
    path('internship_applications_detail/<int:id>/', views.internship_applications_detail, name='internship_applications_detail'),
    path('applications/<int:app_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<int:app_id>/reject/', views.reject_application, name='reject_application'),

#interns urls
    path('intern_dashboard/', views.intern_dashboard, name='intern_dashboard'),  # Intern dashboard



]
