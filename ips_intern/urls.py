from django.contrib import admin
from django.urls import path
from ips_intern import views


urlpatterns = [
    #admin urls
    path('', views.custom_login, name='login'), 
    path('logout/', views.custom_logout, name='custom_logout'),
    path('apply/', views.apply_intern, name='apply_intern'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('interns/', views.all_interns_view, name='all_interns'),
    path('intern/<int:user_id>/', views.intern_detail_view, name='intern_detail'),
   
    path('intern/<int:user_id>/certify/<str:action>/', views.mark_certification, name='mark_certification'),
    path('internship_applications/', views.internship_applications, name='internship_applications'),
    path('internship_applications_list/', views.internship_applications_list, name='internship_applications_list'),
    path('internship_applications_detail/<int:id>/', views.internship_applications_detail, name='internship_applications_detail'),
    path('applications/<int:app_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<int:app_id>/reject/', views.reject_application, name='reject_application'),
    path('certified_interns/', views.certified_interns_view, name='certified_interns'),
    path('export/interns/', views.export_interns_excel, name='export_interns_excel'),
   
#interns urls
    path('intern_dashboard/', views.intern_dashboard, name='intern_dashboard'),  # Intern dashboard
    path('intern/<int:user_id>/certificate/download/', views.download_certificate, name='download_certificate'),
    path('download_pdf/', views.download_task_reports_pdf, name='download_task_reports_pdf'),
    path('download_certificate/', views.download_certificate, name='download_certificate'),
   

] 

    