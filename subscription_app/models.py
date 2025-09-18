from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(
        max_length=20,
        choices=[("basic", "Basic"), ("pro", "Pro")],
        default="basic"
    )
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    active_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True ) 
    updated_at = models.DateTimeField(auto_now=True)     


    def __str__(self):
        return f"{self.user.username} - {self.plan}"
