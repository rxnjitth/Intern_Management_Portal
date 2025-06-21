# ips_intern/models.py

from django.db import models
from django.contrib.auth.models import User

# ✅ 1. User Role Model
class UserRole(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('INTERN', 'Intern'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ✅ 2. Course Duration Model
class CourseDuration(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # Example: "3 months", "6 months", etc.

    def __str__(self):
        return f'{self.course_name} - {self.duration}'


# ✅ 3. Intern Application Model
class InternApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)  # Max CGPA: 10.00 (so use max_digits=4)
    arrears = models.PositiveIntegerField()  # IntegerField is fine, but PositiveIntegerField prevents negative input
    gender = models.CharField(max_length=10)
    clg_mailid = models.EmailField()
    course_duration = models.ForeignKey(CourseDuration, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)  # auto-triggered when course ends
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.name} - {self.roll_no}'


# ✅ 4. Task Report Model
class TaskReport(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    topic = models.TextField()

    def __str__(self):
        return f'{self.intern.username} - {self.date} - {self.topic[:30]}'
