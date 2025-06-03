from django.urls import path
from .views.locationView import CreateLocationView, LocationListView
from .views.stationView import CreateStationView, StationListView
from .views.routeView import RouteListView, RouteCreateView
from .views.tripView import TripCreateView

urlpatterns = [
    path('admin/locations/create/', CreateLocationView.as_view(), name='create-location'),
    path('locations/list/', LocationListView.as_view(), name='location-list'),
    path('admin/stations/create/', CreateStationView.as_view(), name='create-station'),
    path('stations/list/', StationListView.as_view(), name='station-list'),
    path('routes/search/', RouteListView.as_view(), name='routes-list'),
    path('admin/routes/create/', RouteCreateView.as_view(), name='create-route'),
    path('company/ticket/create/', TripCreateView.as_view(), name='create-ticket'),
]