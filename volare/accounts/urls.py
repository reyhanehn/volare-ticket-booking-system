from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.signupView import SignupView
from .views.otpLoginView import VerifyOTPView
from .views.otpLoginView import RequestOTPView
from .views.passwordLoginView import PasswordLoginView
from .views.profileView import ProfileView
from .views.walletView import WalletView
from .views.logoutView import LogoutView
from .views.forgotPasswordView import RequestForgotPasswordView
from .views.forgotPasswordView import VerifyForgotPasswordView
from .views.wallet_transactionsView import WalletChargeView, WalletTransactionListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('loginPassword/', PasswordLoginView.as_view(), name='loginPassword'),
    path('password/forgot/', RequestForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/', VerifyForgotPasswordView.as_view(), name='reset_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/transactions/charge/', WalletChargeView.as_view(), name='charge_wallet'),
    path('wallet/transactions/', WalletTransactionListView.as_view(), name='all_transactions'),
]
