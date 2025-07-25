from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superteacher', 'Superteacher'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    username = models.CharField(max_length=100, blank=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username sigue siendo obligatorio si usas AbstractUser

    def save(self, *args, **kwargs):
        if self.role == 'superteacher':
            self.is_superuser = True
            self.is_staff = True
        elif self.role == 'teacher':
            self.is_staff = True
            self.is_superuser = False
        elif self.role == 'student':
            self.is_superuser = False
            self.is_staff = False

        if self.is_superuser and self.is_staff:
            self.role = 'superteacher'
        elif not self.is_superuser and self.is_staff:
            self.role = 'teacher'
        elif not self.is_superuser and not self.is_staff:
            self.role = 'student'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    

class Student(CustomUser):
    """
    Student model that inherits from CustomUser.
    This model can have additional fields specific to students if needed.
    """
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.username} - {self.role}"  # Assuming role is a field in CustomUser

class Teacher(CustomUser):
    """
    Teacher is a subclass of CustomUser that represents a user with
    teacher privileges in the system.
    """
    class Meta:
        proxy = True
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

class SuperTeacher(Teacher):
    """
    SuperTeacher is a subclass of Teacher that represents a user with
    super teacher privileges in the system.
    """
    class Meta:
        proxy = True
        verbose_name = 'Super Teacher'
        verbose_name_plural = 'Super Teachers'