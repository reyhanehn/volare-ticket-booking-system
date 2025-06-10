from django.urls import path
from .views.customerReportView import CreateReportView, ListMyReportsView
from .views.AdminReportView import SearchReportsView, ViewReportView, AnswerReportView


urlpatterns = [
    path('create/', CreateReportView.as_view(), name='make reports'),
    path('my/reports/', ListMyReportsView.as_view(), name='my reports'),
    path('search/reports/', SearchReportsView.as_view(), name='search reports'),
    path('search/reports/<int:report_id>/', ViewReportView.as_view(), name='view report'),
    path('answer/report/<int:report_id>', AnswerReportView.as_view(), name='answer report'),
]
