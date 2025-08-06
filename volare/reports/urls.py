from django.urls import path
from .views.customerReportView import CreateReportView, ListMyReportsView
from .views.AdminReportView import SearchReportsView, ViewReportView, AnswerReportView


urlpatterns = [
# for all of the APIs in here you need to be authorized
    path('create/', CreateReportView.as_view(), name='make reports'),
# this is where users can submit a report on a Ticket or Reservation or Payment(these go in the type)
# this is a post request and it needs the id of the thing you are reporting
# it will create a report for you and sets the status to pending and you can wait for the admin to answer
# request format
# {
#     "type" : "Reservation",
#     "text" : "There was a time There was a life",
#     "related_report" : 60
# }

    path('my/reports/', ListMyReportsView.as_view(), name='my reports'),
# this is where users can see all their reports and even filter them (with query params)
# this is a get request that you can filter the search with status and type
# the respond will be all the reports with the filters that you provided
# query params example format
# "type" : "Reservation"
# "status" : "Pending"

    path('search/reports/', SearchReportsView.as_view(), name='search reports'),
# your role should be admin to have access to this API
# this is where admin can see all the reports and filter them (with query params)
# this is a get request that you can filter the search with status and type and admin_id and account_id and related_report
# the respond will be all the reports with the filters that you provided
# query params example format
# "type" : "Reservation"
# "status" : "Pending"
# "admin_id" : "10"
# "account_id" : "234"
# "related_report" : "23"

    path('search/reports/<int:report_id>/', ViewReportView.as_view(), name='view report'),
# your role should be admin to have access to this API
# this is where admin can view a report with full detail
# this is a get request that you give the report_id you want to view in the ulr
# the respond will be the report with the report_id

    path('answer/report/<int:report_id>/', AnswerReportView.as_view(), name='answer report'),
# your role should be admin to have access to this API
# this is where admin can answer a report
# this is a patch request that you give the report_id you want to answer in the ulr and the answer in the request
# this will change the status to changed and the admin_id to the admin that just answered the respond will be the report with full detail
# request format
# {
#     "answer" : "I know right?"
# }

]
