from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .models import VehicleService
from .views.serviceView import ServiceListView, CreateServiceView
from .views.companyView import CreateCompanyView, GetMyCompanyView, GetAllCompaniesView
from .views.vehicleServiceView import AssignServicesToVehicleView
from .views.vehicleView import CreateVehicleView, GetAllVehiclesView

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services'),
    path('admin/services/create/', CreateServiceView.as_view(), name='create_services'),
    path('admin/companies/create/', CreateCompanyView.as_view(), name='create-company'),
    path('admin/vehicles/create/', CreateVehicleView.as_view(), name='create-vehicle'),
    path('my_company/', GetMyCompanyView().as_view(), name='my-company'),
    path('admin/companies/list', GetAllCompaniesView.as_view(), name='list-companies'),
    path('admin/vehicles/list', GetAllVehiclesView.as_view(), name='list-vehicles'),
    path('vehicleService/', AssignServicesToVehicleView.as_view(), name='vehicle-service'),
]
