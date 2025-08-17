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
    #this is a post request for creating new company which only the admins are allowed to do(it will e checked from the permission class which we have a def to check the role of an account)
    #when creating the company the admin will also input's the info of the company admin in the request so the
    #company admin will e added to the accounts with its roel set as Company_Admin
    #the format of the request input is like this:
    #   {
    #   "name": "RandomRoad Tours",
    #   "logo_url": "https://skyroad.com/logo.png",
    #   "website": "https://randomroad.com",
    #   "owner_data": {
    #     "phone_number": "+989109106296",
    #     "email": "reyhanehnemati1383@gmail.com",
    #     "name": "reyhaneh",
    #     "lastname": "nemati",
    #     "password_hash": "StrongPassword123!"
    #   }
    # }
    path('admin/vehicles/create/', CreateVehicleView.as_view(), name='create-vehicle'),
    # this is a post request for creating(adding) vehicles for the company which the company admin can only do (checked role like the admin)
    # we hae three kinds of vehicles (1.airplanes  2.bus  3.train) so the request should include a type to specify the vehicle
    # we also hae a layout in all the vehicles:
            #1. for airplanes layout is(1 or 2 or 3) which will show according that the airplane have(economy, first class, business)
            #so for example if the layout is 2 the airplane has economy and business
            #2. for train layout is the number of the cabins
            #3. and for the bus if the layout is 1 the structure of the seats of the bus is 2+2 and if it is 2 then it is 1 + 2
            #so these are the sections of each vehicle which can have different prices in the thickets and for the airplane we should also input the numer of seats in each of the sections as well
            #we have to also check the number of seats to match in the sections to the total number of seats
   #the request input is like:
    # {
    #   "name": "Boeing 737",
    #   "type": "Airplane",
    #   "class_code": 3,
    #   "total_seats": 180,
    #   "layout": "3",
    #   "sections": [
    #     {"name": "First Class", "seats_count": 20},
    #     {"name": "Business Class", "seats_count": 40},
    #     {"name": "Economy Class", "seats_count": 120}
    #   ]
    # }
    path('my_company/', GetMyCompanyView().as_view(), name='my-company'),
    #this is a get request for the company admin to get the info of its own company
    path('admin/companies/list', GetAllCompaniesView.as_view(), name='list-companies'),
    #this is get request for the admin to see the list of all companies with their info and the info af the company admin of the company
    path('admin/vehicles/list', GetAllVehiclesView.as_view(), name='list-vehicles'),
    #this is a get request for the company admin and the admin to see all the vehicles available in all the companies
    path('vehicleService/', AssignServicesToVehicleView.as_view(), name='vehicle-service'),
]
