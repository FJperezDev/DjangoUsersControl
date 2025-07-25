from .customUser import CustomUser

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