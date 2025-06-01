from django.urls import path
from .views.companyView import CreateCompanyView
from .views.vehicleView import CreateVehicleView

urlpatterns = [
    path('admin/companies/create/', CreateCompanyView.as_view(), name='create-company'),
    path('admin/vehicles/create/', CreateVehicleView.as_view(), name='create-vehicle'),
]