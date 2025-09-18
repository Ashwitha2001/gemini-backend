from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class SignupSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "mobile_number"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        mobile = validated_data.pop("mobile_number")
        password = validated_data.pop("password")
        email = validated_data.get("email")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=email,
            password=password
        )
        Profile.objects.create(user=user, mobile_number=mobile)
        return user
