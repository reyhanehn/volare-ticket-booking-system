from django.urls import path
from .views.signupView import SignupView
from .views.otpLoginView import VerifyOTPView
from .views.otpLoginView import RequestOTPView
from .views.profileView import ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
