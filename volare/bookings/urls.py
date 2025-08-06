from django.urls import path

from .views.adminReservationCancellation import AdminCancelReservationView
from .views.locationView import CreateLocationView, LocationListView
from .views.passengerView import CreatePassengerView, PassengerListView
from .views.reservationCancellationView import ReservationCancelInfoView, ReservationCancelConfirmView
from .views.reservationView import CreateReservationView, ReservationListView, AdminReservationFilterView, CustomerReservationView, AdminReservationView
from .views.stationView import CreateStationView, StationListView
from .views.routeView import RouteListView, RouteCreateView
from .views.tripView import TripCreateView
from .views.tripStopView import TripStopView
from .views.ticketView import TicketSearchView, TicketCacheDetailView, AdminTicketListView, CompanyTicketListView
from .views.paymentView import ReservationPaymentView, PaymentStatusView
from .views.paymentHistoryView import PaymentHistoryView
from .views.adminReservationView import AdminEditReservationView, AdminConfirmReservationView

urlpatterns = [
    path('admin/locations/create/', CreateLocationView.as_view(), name='create-location'),
# this is POST request for the admin to add locations which will include the country and the city
# this is the request format:
#   {
#    "country": "France",
#    "city": "Paris"
#  }
    path('locations/list/', LocationListView.as_view(), name='location-list'),
# this is a GET request to see all the locations and customers can use this as well as the admins and company admins
# it is useful for searching for tickets and trips and routes
    path('admin/stations/create/', CreateStationView.as_view(), name='create-station'),
# this is a POST request to add new stations
# the stations need a location so it will input the location_id from the locations added
# (for front since users don't know location id we will create a drop down for all locations and choosing one will return the id to backend)
# also the type of the station should be noted(airport or train station or bus station)
#  {
#  "name": "ParisBusStation",
#  "type": "Bus_Station",
#  "location": 1
# }
    path('stations/list/', StationListView.as_view(), name='station-list'),
# this is a GET request to see the list of stations
    path('admin/routes/create/', RouteCreateView.as_view(), name='create-route'),
# this is POST request for the admin to create routes which includes the locations and stations of the origin and destination
#   {
#      "origin_id" : 2,
#      "destination_id" : 1,
#      "origin_station_id" : 3,
#      "destination_station_id" : 2
#   }
#it will check the stations to be in the locations and also check the type of the stations to match
    path('routes/search/', RouteListView.as_view(), name='routes-list'),
# this is a GET request it will return all the matching routes
# it can be filtered by origin, destination, origin_station and destination_station
# again routes are used to find related tickets (and also when creating a ticket we need the route)
# the params defined keys are "origin", "destination", "origin_station" and "destination_station" remember all the values are the wanted ids for each
    path('company/ticket/create/', TripCreateView.as_view(), name='create-ticket'),
# this is a POST request for the company admin to add tickets
# the tickets need a vehicle id and route id
# also the departure time and the duration of the trip
# the input will include the details of the prices for different sections by section id
# so in this api first the trip will be created which includes the basic info
# like the route id and vehicle id and the departure time and duration
# and then the price and details for sections will be in the ticket and the ticket will have reference to the trip created
# sample input :
#   {
#      "vehicle_id" : 9,
#      "route_id" : 17,
#      "departure_datetime": "2025-08-21",
#      "duration": "08:30:00",
#      "ticket_info":[
#          {"section_id": 25, "price": 40},
#          {"section_id": 26, "price": 40},
#          {"section_id": 27, "price": 40},
#          {"section_id": 28, "price": 40},
#          {"section_id": 29, "price": 40}
#      ]
#  }
    # path('trips/list/',   , name='trips-list'),  # not done
    # path('trips/<int:trip_id>/',   , name='trip-details'),  # not done
    path("trips/<int:trip_id>/stops/", TripStopView.as_view(), name="trip-stops"),
# this end point has both GET and POST method
# the GET request returns the related stops to that specific trip (the trip id is given in the end point)
# the POST request adds stops to a trip
# company admins after creating the trip and its related tickets can add stops to that trip
# the stops people encounter during that trip which can be a layover or transit or refuel or meal stop
# all these are specified in the body and added to the trips
# the input is like this (a list of stops are given and each has their specific details)
# keep in mind every kind of stop is not allowed for every trip cause like flights don't have meal stops
# {
#   "stops": [
#     {
#       "stop_order": 1,
#       "stop_type": "Meal",
#       "station_id": 20,
#       "duration": "01:30:00"
#     },
#     {
#       "stop_order": 2,
#       "stop_type": "Refuel",
#       "station_id": 25,
#       "duration": "01:30:00"
#     }
#   ]
# }
    # path('trips/<int:trip_id>/tickets/',  , name='view-trips-tickets'),  # not done
    # path('trips/<int:trip_id>/edit/',  , name='edit-trip'),  # not done
    # path('trips/<int:trip_id>/cancel/',  , name='cancel-trip'),  # not done
# There are 3 different types of ticket search provided (3 different GET requests)
# each has their own specific constraints but one thing is the same for all and that is these filters
# origin_id, destination_id, departure_date_exact, departure_date_start,
# departure_date_end, departure_time, transport_type, class_code, min_price, max_price, order
# these filters exist for all of these 3 searches
# the other thing they all have in common they all store the whole ticket list in the cache
# so when users are going through them they don't access database each time
    path('customer/tickets/search/', TicketSearchView.as_view(), name='customer-tickets-list'),
# this one is for customers it only returns valid tickets tickets which still have capacity and their departure time isn't passed
# and they are not cancelled
# the permission class for this view is allow any cause anybody can view the tickets list
# also we can filter this by company_id too
    path('admin/tickets/search/', AdminTicketListView.as_view(), name='admin-tickets-list'),
# this one is for admins the permission class is IsAuthenticated and IsAdmin and it has no inner filter
# this can be filtered by company_id too
    path('company/tickets/search/', CompanyTicketListView.as_view(), name='company-tickets-list'),
# this one is used by comany admins the permission class is IsAuthenticated and IsCompanyAdmin
# it only shows the tickets that belong to that specific company
# so by default it has an inner filter for company so it doesn't have that as a param
    path('tickets/search/<int:ticket_id>/', TicketCacheDetailView.as_view(), name='ticket-details'),
# this is another GET request this shows the ticket info with full details
# info like price remaining seats and stuff data related to the vehicle everything about vehiclesection
# all the stops and services related to that trip or vehicle stuff related to ticket like departure time which are trip details
# and how it gets the information is first it tries to see if they exist in the cache and then if not it accesses the data base and returns the needed info
    # path('admin/tickets/<int:ticket_id>/edit/',  , name='edit-ticket'),  # not done
    # path('admin/tickets/<int:ticket_id>/cancel/',  , name='edit-ticket'),  # not done
    path('customer/passenger/create/', CreatePassengerView.as_view(), name='create-passenger'),
# this is a POST request for the customers to add related passengers for themselves to use in the reservation
# (because each reservation needs a specific passenger)
#  {
#     "name": "ali",
#     "lastname": "alavi",
#     "ssn": 1000000000,
#     "birthdate": "1990-02-12"
# }
    path('customer/passenger/list/', PassengerListView.as_view(), name='passenger-list'),
# a GET request for the customer to get the list of the customers added for themselves
    path('reservation/create/', CreateReservationView.as_view(), name='create-reservation'),
# a POST request to actually reserve a ticket
# this request needs the ticket_id and the seat number as well as the passenger_id
# (it will be checked that the passenger is related to the account that is making the reservation)
# it will be checked that the seat number wasn't reserved before
# this reservation will be reserved in the pending status till the payment is done
# if the payment hadn't been done by 10 minutes the reservation will be canceled by the system and others can reserve it again
#  {
#   "passenger_id": 1,
#   "ticket_id": 1,
#   "seat_number": "10"
# }
    path('customer/reservation/list/', ReservationListView.as_view(), name='reservation-list'),
# this is a GET request for the customer to see the list of their reservation they can also filter the result list by the date and status
# the params (date and status will be query params that the user will input)
# the date can also represent a range like before a certain date or after it all can be done by the queries like this (?date_after=2025-05-01)
# so this wil give the customer a general info about the reservation
# and if the customer want to see more details they can use the wanted reservation_id in the next request
    path('customer/reservation/<int:reservation_id>/', CustomerReservationView.as_view(), name='reservation-view'),
# this another GET one
# so this request will give the extra info about the ticket and route and trip of the reservation by the reservation id that is the input
#   {
#     "reservation_id": 1,
#     "seat_number": "3",
#     "status": "Cancelled",
#     "reservation_date": "2025-06-11",
#     "reservation_time": "22:02:27.487632",
#     "passenger_id": "ali alavi",
#     "ticket_info": {
#         "ticket_id": 1,
#         "price": 10.0,
#         "remaining_seats": 20,
#         "seat_range": "1–20",
#         "section": "First Class",
#         "vehicle": {
#             "name": "Boeing 737",
#             "type": "Airplane",
#             "class_code": 3,
#             "layout": "3"
#         },
#         "route": {
#             "origin": "Tehran",
#             "destination": "Paris",
#             "origin_station": "Tehran airport",
#             "destination_station": "Paris airport"
#         },
#         "trip": {
#             "trip_id": 1,
#             "departure_datetime": "2026-01-02T00:00:00Z",
#             "duration": "9000.0",
#             "company": "RandomRoad Tours"
#         },
#         "stops": [],
#         "services": []
#     }
# }
    path('customer/reservation/<int:reservation_id>/pay/', ReservationPaymentView.as_view(), name='reservation-payment'),
# so this a POST request for the customer to pay for thr reservation made by the reservation_id and the specified method like cash or wallet
# so if the method is wallet the balance would be checked as well
# then a confirmation email will be sent to the user with a complete info of the reservation
# the input is something like this
# also this is atomic transaction
# {
#     "method" : "Cash"
# }
    path('reservation/<int:reservation_id>/payment_status/', PaymentStatusView.as_view(), name='payment-status'),
# so this is a GET request to show the status of the payment (reservation) by the reservation_id
# so if the reservation was confirmed by paying it will show something like this
# {
#     "status": "Completed",
#     "method": "Wallet",
#     "amount": 10.0,
#     "paid_on": "2025-06-12",
#     "paid_at": "18:40:25.753792",
#     "reservation": {
#         "id": 7,
#         "ticket": 1,
#         "status": "Confirmed",
#         "seat": "11",
#         "passenger": "ali alavi"
#     }
# }
# and even if the reservation had been cancelled it shows the refund info
# also if the user who is accessing these is an admin it will show the name of the user who made this reservation as well
    path('payment/history/', PaymentHistoryView.as_view(), name='payment-history'),
# this is a GET request for the customer to see all the payments made
# this will hae the reservation id  and amount and method of the payment as well as the date-time
# and the status which can be confirmed of refunded if the reservation was canceled
# we can also filter these based on method, status, start_date, end_date, start_time, end_time
# and if the user who is accessing the list is an admin they can filter these based on account_id too to see payments related to one user
    path('reservation/cancellation/info/', ReservationCancelInfoView.as_view(), name='reservation-cancellation-info'),
# this is a GET request for when the customer wants to cancel a reservation
# so first by using this api they see the full info of the reservation
# if the reservation was confirmed and had a payment it will also show the penalty that they have to pay
# and the refund amount which will be returned to their wallet
# but if the status was pending only the reservation info and the ticket price is shown
# the body only contains the reservation id
# {
#     "reservation_id" : 71
# }
# and this is the response
#  {
#     "reservation": {
#         "reservation_id": 7,
#         "seat_number": "11",
#         "status": "Confirmed",
#         "reservation_date": "2025-06-12",
#         "reservation_time": "18:39:07.551231",
#         "ticket_id": 1,
#         "passenger_id": 1,
#         "expiration_time": "2025-06-12T18:42:07.550535+00:00"
#     },
#     "ticket_price": 10.0,
#     "penalty_percentage": 10,
#     "penalty_amount": 1.0,
#     "refund_amount": 9.0
# }
    path('reservation/cancel/', ReservationCancelConfirmView.as_view(), name='reservation-cancel'),
# so this is a POST request which will actually cancel the reservation by the reservation id
# and if the reservation was confirmed it will refund the price of the ticket minus the penalty
# it also will send a notice by email to user that their reservation has been cancelled
# the body only contains the reservation id
# {
#     "reservation_id" : 71
# }
    path('admin/cancel/reservation/', AdminCancelReservationView.as_view(), name='admin-cancel-reservation'),
# this api is used by admins to cancel a reservation for a customer by the reservation_id
# after the cancellation the price will be refunded to the customers wallet and a notice will be sent to them by email
    path('admin/reservation/list/', AdminReservationFilterView.as_view(), name='admin-reservation-list'),
# this is a GET request for the admin to see the reservation
# and it will use query params just like the get request for reservation for the customer
    path('admin/reservation/<int:reservation_id>/', AdminReservationView.as_view() , name='admin-view-reservation'),
# again just like the customer admin can use this api to see the full detailed info of the reservation including trip and ticket and route info
# keep in mind admin sees data about the user who made the reservation also
    path('admin/reservation/<int:reservation_id>/edit/', AdminEditReservationView.as_view() , name='admin-edit-reservation'),
# this is a PUT request admins are able to edit a reservation they can change passenger and seat id
# for passenger they can enter passenger name and passenger last name and it checks if there exists a passenger
# with this info in the users passengers list
# and if it does it changes the passenger
# it also checks if the new seat isn't previously reserved
# the body is something like this
# {
#     "seat_number" : "13",
#     "passenger_name": "asal",
#     "passenger_lastname": "asghari"
# }
# not all these 3 is required but at least one of them needs to be there
    path('admin/reservation/<int:reservation_id>/confirm/', AdminConfirmReservationView.as_view(),name='admin-confirm-reservation'),
# this one is a POST method
# sometimes mistakes are made and maybe admin needs to confirm a reservation that was wrongfully cancelled or is still pending so we have an API for this
# the body is empty
# and also after the reservation is confirmed a confirmation email will be sent to user
]
