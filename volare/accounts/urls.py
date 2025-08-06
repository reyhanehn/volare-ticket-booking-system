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
# this is the sign up view it is a POST request
# after sign up a jwt token will be created and given to the user as their authentication token
# it also stores the user who entered profiles info into cache
# the inputs are in this format (keep in mind role is not necessary for customers)
# {
#    "phone_number" : "09302842970",
#    "email" : "golshidabtahi@gmail.com",
#    "name" : "Golshid",
#    "lastname": "Abtahi",
#    "password_hash" : "h.tah1584",
#    "role" : "Customer"
# }
    path('loginOTP/', RequestOTPView.as_view(), name='loginOTP'),
# this again is a POST request it is for login the input is identifier which is an email
# and the otp will be sent to the email and also saved in cach(redis)
# the inputs are in this format
# {
#     "identifier" : "mahiozoneborone@gmail.com"
# }
    path('verifyOTP/', VerifyOTPView.as_view(), name='verifyOTP'),
# this is another post request which will check if the identifier and the otp match
# it will retrive the correct otp from cache and compare it to the one user entered
# and if they match there again a jwt token as authentication token is generated
# it also stores the user who entered profiles info into cache
# the inputs are in this format
# {
#     "identifier" : "mahiozoneborone@gmail.com",
#     "otp" : "720872"
# }
    path('loginPassword/', PasswordLoginView.as_view(), name='loginPassword'),
# another way to login which is a post request that gets identifier which is email and the password
# it checks if the password and the identifier are corect if they match there again a jwt token as authentication token is generated
# the inputs are in this format
# {
#     "identifier" : "mahiozoneborone@gmail.com",
#     "password" : "mahi1384@"
# }
    path('password/forgot/', RequestForgotPasswordView.as_view(), name='forgot_password'),
# if you dont remember your password you can use this post request with an identifier as input
# an otp will be sent to your email and you can use it in the password/reset/ api to reset your password
# the inputs are in this format
# {
#     "identifier" : "mahiozoneborone@gmail.com",
# }
    path('password/reset/', VerifyForgotPasswordView.as_view(), name='reset_password'),
# the otp that we got from password/forgot/ is used in this post request
# it first checks if the otp and the identifier are valid and matching and then resets the password you provided in input
# the inputs are in this format
# {
#     "identifier" : "mahiozoneborone@gmail.com",
#     "otp" : "720872"
#     "password" : "mahi1384!"
# }
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# access tokens are only valid for 30 minutes so if the time ends you can use the refresh token to get a new access token
# this post request requires a refresh token as an input
# it checks if the refresh token is still valid (they expire in a week) and returns a new access token
# the inputs are in this format
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDA3MDUxMiwiaWF0IjoxNzQ5NDY1NzEyLCJqdGkiOiI1ZWNiZDI1NjE1NjA0NzgxYjQ3MDFjZmQxNjg4ZGFlNyIsInVzZXJfaWQiOjN9.oXdMxH15tfvNwFsmSTqKqq8XQ2TzKa3ogrCxAna4qBc"
# }
    path('logout/', LogoutView.as_view(), name='logout'),
# the logout just blacklists the refresh token and unusable for future refreshes
# this post request requires a refresh token as an input
# {

#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDA3MDUxMiwiaWF0IjoxNzQ5NDY1NzEyLCJqdGkiOiI1ZWNiZDI1NjE1NjA0NzgxYjQ3MDFjZmQxNjg4ZGFlNyIsInVzZXJfaWQiOjN9.oXdMxH15tfvNwFsmSTqKqq8XQ2TzKa3ogrCxAna4qBc"
# }
    path('profile/', ProfileView.as_view(), name='profile'),
# for profile we have a GET a PUT and a PATCH method
# using the authentication it shows the requests user from that we take the account id then to get users info
# first we check cache if it is available there or not if it wasn't we take the info from database and also store it in cache
# for the put and patch methods given the body they change the users profile info
# but keep in mind they do it by first checking all the constraints and they also update the profile info stored in cache
# also some fields are read only and can not be changed by user like role or status
# GET request has no input and in this case no params
# PUT request is used when we want to change all the data related to profile (except the read only ones)
# {
#     "email": "tahmouressii1584@gmail.com",
#     "phone_number": "+989107654888",
#     "city": 1,
#     "name": "Hedie",
#     "lastname": "Tahmoures",
#     "role": "Admin",
#     "status": "Active",
#     "registration_date": "2025-06-01",
#     "birth_date": "2000-05-02",
#     "last_login": null
# }
# PATCH is a lot similar to PUT but it can change partial information
# {
#     "email":"z.azordeh2006@gmail.com"
# }
    path('wallet/', WalletView.as_view(), name='wallet'),
# this is a GET request this shows information related to the users wallet
# (we access users info as I explained to you by taking account id from requests user and finding his/her wallet by queries)
# info such as balance, number of transactions of each type and ...
    path('wallet/transactions/charge/', WalletChargeView.as_view(), name='charge_wallet'),
# this is a POST request it is supposed to charge users wallet
# as I explained how in the previous api we find the wallet and charge it the amount that the user requested
# the input is something like
# {
#     "amount" : 4587200
# }
    path('wallet/transactions/', WalletTransactionListView.as_view(), name='all_transactions'),
# this is a GET request here we can have params such as Type which can be 3 different types Refund, Payment, Charge
# this request returns the history of transaction done in the users wallet
]
