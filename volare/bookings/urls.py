from django.urls import path
from .views.locationView import CreateLocationView, LocationListView
from .views.stationView import StationView, StationListView

urlpatterns = [
    path('locations/create/', CreateLocationView.as_view(), name='create-location'),
    path('locations/list/', LocationListView.as_view(), name='location-list'),
    path('stations/create/', CreateStationView.as_view(), name='create-station'),
    path('stations/list/', StationListView.as_view(), name='station-list'),

]