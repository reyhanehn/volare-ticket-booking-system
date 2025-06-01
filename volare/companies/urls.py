from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.serviceView import ServiceListView, CreateServiceView
from .views.companyView import CreateCompanyView
from .views.vehicleView import CreateVehicleView

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services'),
    path('admin/services/create/', CreateServiceView.as_view(), name='create_services'),
    path('admin/companies/create/', CreateCompanyView.as_view(), name='create-company'),
    path('admin/vehicles/create/', CreateVehicleView.as_view(), name='create-vehicle'),
]
