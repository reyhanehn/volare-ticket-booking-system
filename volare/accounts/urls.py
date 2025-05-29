url
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.signupView import SignupView
from .views.otpLoginView import VerifyOTPView
from .views.otpLoginView import RequestOTPView
from .views.passwordLoginView import PasswordLoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('loginPassword/', PasswordLoginView.as_view(), name='loginPassword'),
]