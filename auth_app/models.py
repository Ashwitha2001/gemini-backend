from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile_number = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"

