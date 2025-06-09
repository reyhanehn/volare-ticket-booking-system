from django.urls import path
from .views.costumerReportView import CreateReportView

urlpatterns = [
    path('create/', CreateReportView.as_view(), name='reports'),
]
