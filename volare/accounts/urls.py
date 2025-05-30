from django.urls import path
from .views.signupView import SignupView
from .views.otpLoginView import VerifyOTPView
from .views.otpLoginView import RequestOTPView
from .views.profileView import ProfileView
from .views.walletView import WalletView
from .views.wallet_transactionsView import WalletChargeView, WalletTransactionListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('wallet/transactions/charge/', WalletChargeView.as_view(), name='charge_wallet'),
    path('wallet/transactions/', WalletTransactionListView.as_view(), name='all_transactions'),
]
