from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    username = models.CharField(max_length=100, blank=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    statistics = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username sigue siendo obligatorio si usas AbstractUser

    def save(self, *args, **kwargs):

        # Only for creating first superadmin user
    
        # if self.is_superuser and self.is_staff:
        #     self.role = 'superadmin'
        # elif not self.is_superuser and self.is_staff:
        #     self.role = 'admin'
        # elif not self.is_superuser and not self.is_staff:
        #     self.role = 'user'

        if self.role == 'superadmin':
            self.is_superuser = True
            self.is_staff = True
        elif self.role == 'admin':
            self.is_staff = True
            self.is_superuser = False
        elif self.role == 'user':
            self.is_superuser = False
            self.is_staff = False

        super().save(*args, **kwargs)



    def __str__(self):
        return self.username
