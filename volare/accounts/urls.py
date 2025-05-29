from django.urls import path
from .views.signupView import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
]
