from .teacher import Teacher

class SuperTeacher(Teacher):
    """
    SuperTeacher is a subclass of Teacher that represents a user with
    super teacher privileges in the system.
    """
    class Meta:
        proxy = True
        verbose_name = 'Super Teacher'
        verbose_name_plural = 'Super Teachers'