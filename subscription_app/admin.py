from django.contrib import admin
from .models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'stripe_subscription_id', 'active_until', 'created_at', 'updated_at')
    list_filter = ('plan',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Subscription, SubscriptionAdmin)
