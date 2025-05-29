from django.urls import path
from .views.signupView import SignupView
from .views.otpLoginView import VerifyOTPView
from .views.otpLoginView import RequestOTPView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
]
