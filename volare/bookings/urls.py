from django.urls import path
from .views.locationView import CreateLocationView

urlpatterns = [
    path('locations/create/', CreateLocationView.as_view(), name='create-location'),
]