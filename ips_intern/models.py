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

from django.utils import timezone
class InternApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)  # Max CGPA: 10.00
    arrears = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    clg_mailid = models.EmailField()
    course_duration = models.ForeignKey('CourseDuration', on_delete=models.SET_NULL, null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    just_approved = models.BooleanField(default=False)

    approved_at = models.DateTimeField(null=True, blank=True)  # ⏳ Used for tracking duration start

    def save(self, *args, **kwargs):
        if self.is_approved and not self.approved_at:
            self.approved_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.roll_no}'


# ✅ 4. Task Report Model
class TaskReport(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    topic = models.TextField()

    def __str__(self):
        return f'{self.intern.username} - {self.date} - {self.topic[:30]}'
