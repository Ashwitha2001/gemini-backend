from django.urls import path
from .views import SubscribeProView, StripeWebhookView, SubscriptionStatusView

urlpatterns = [
    path("subscribe/pro/", SubscribeProView.as_view(), name="subscribe_pro"),
    path("webhook/stripe/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("status/", SubscriptionStatusView.as_view(), name="subscription_status"),
]
