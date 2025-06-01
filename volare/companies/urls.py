from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.serviceView import ServiceListView, CreateServiceView

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services'),
    path('admin/services/create/', CreateServiceView.as_view(), name='create_services'),
]
