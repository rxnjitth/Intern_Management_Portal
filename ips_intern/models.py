from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('INTERN', 'Intern'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# ips_intern/forms.py

from django import forms

class CourseDuration(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # Example: "3 months", "6 months", etc.
    
    def __str__(self):
        return f'{self.course_name} - {self.duration}'

# InternApplication Model: Stores the data when an intern applies for an internship
class InternApplication(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    arrears = models.IntegerField()  # No of arrears
    gender = models.CharField(max_length=10)
    clg_mailid = models.EmailField()
    course_duration = models.ForeignKey(CourseDuration, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.roll_no}'
    
class TaskReport(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    topic = models.TextField()

    def __str__(self):
        return f'{self.intern.username} - {self.date} - {self.topic[:30]}'