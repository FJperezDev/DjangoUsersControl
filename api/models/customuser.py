from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superteacher', 'Superteacher'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.name