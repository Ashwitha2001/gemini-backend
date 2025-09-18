from django.urls import path
from .views import UserMeView, SignupView, SendOTPView, VerifyOTPView,  ChangePasswordView,  ForgotPasswordView

urlpatterns = [
    path("user/me/", UserMeView.as_view(), name="user_me"),
    path("signup/", SignupView.as_view()),
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),

]
