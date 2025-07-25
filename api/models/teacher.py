from .customUser import CustomUser

class Teacher(CustomUser):
    """
    Teacher is a subclass of CustomUser that represents a user with
    teacher privileges in the system.
    """
    class Meta:
        proxy = True
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'