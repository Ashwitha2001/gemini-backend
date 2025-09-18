from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .utils import generate_otp, store_otp, verify_otp
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from rest_framework.permissions import IsAuthenticated


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
    

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile_number")
        if not mobile:
            return Response({"error": "Mobile number required"}, status=status.HTTP_400_BAD_REQUEST)
        otp = generate_otp()
        store_otp(mobile, otp)
        return Response({"otp": otp}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile_number")
        otp = request.data.get("otp")
        if verify_otp(mobile, otp):
            profile = Profile.objects.get(mobile_number=mobile)
            profile.is_verified = True
            profile.save()
            user = profile.user
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile_number")
        if not mobile:
            return Response({"error": "Mobile number required"}, status=status.HTTP_400_BAD_REQUEST)
        otp = generate_otp()
        store_otp(mobile, otp)
        return Response({"otp": otp}, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        user = request.user
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully"})
        return Response({"error": "New password required"}, status=status.HTTP_400_BAD_REQUEST)
