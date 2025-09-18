from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Subscription


class SubscribeProView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Mocked checkout URL
        checkout_url = f"http://localhost:8000/mock-stripe-checkout/{request.user.id}/"
        return Response({"checkout_url": checkout_url})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    
    # Mock Stripe Webhook
    def post(self, request):
        data = request.data
        email = data.get("customer_email")
        customer_id = data.get("customer")
        subscription_id = data.get("subscription")

        # Step 1: Fetch user by email
        from django.contrib.auth.models import User
        from .models import Subscription

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Get or create subscription
        sub, created = Subscription.objects.get_or_create(user=user, defaults={"plan": "basic"})

        # Step 3: Update subscription to Pro
        sub.plan = "pro"
        sub.active_until = timezone.now() + timedelta(days=30) 
        sub.stripe_customer_id = customer_id
        sub.stripe_subscription_id = subscription_id
        sub.save()

        return Response({
            "status": "mock webhook processed",
            "user": user.username,
            "plan": sub.plan,
            "subscription_created": created
        })


class SubscriptionStatusView(APIView):
    """Return user subscription plan"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub = Subscription.objects.filter(user=request.user).first()
        return Response({"plan": sub.plan if sub else "basic"})
