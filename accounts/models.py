from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Employee(AbstractUser):
        has_access=models.BooleanField(default=True)
        is_admin = models.BooleanField(default=False)  # New field to indicate admin status
        is_approved = models.BooleanField(default=False)  # New field to indicate user approval
        
        def __str__(self):
                return self.username
