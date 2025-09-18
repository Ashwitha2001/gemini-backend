import time
import redis
from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve
from .models import Subscription

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

    def __call__(self, request):
        # only apply to authenticated users
        if request.user.is_authenticated:
            match = resolve(request.path_info)

            # check only chat message endpoint
            if match.url_name == "send-message" and request.method == "POST":
                sub = Subscription.objects.filter(user=request.user).first()
                plan = sub.plan if sub else "basic"

                if plan == "basic":
                    today = time.strftime("%Y-%m-%d")
                    key = f"user:{request.user.id}:msgcount:{today}"

                    count = self.redis.get(key)
                    count = int(count) if count else 0

                    if count >= 5:
                        return JsonResponse(
                            {"error": "Daily limit reached (5 msgs/day). Upgrade to Pro."},
                            status=429,
                        )

                    # increment counter with 24h expiry
                    pipe = self.redis.pipeline()
                    pipe.incr(key, 1)
                    pipe.expire(key, 86400) 
                    pipe.execute()

        return self.get_response(request)
