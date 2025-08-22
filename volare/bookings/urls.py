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
from .views.seatsView import AvailableSeatsView

urlpatterns = [
    path('admin/locations/create/', CreateLocationView.as_view(), name='create-location'),
    #this is post request for the admin to add locations which will include the country and the city
    #this is the request format:
    #  {
    #   "country": "France",
    #   "city": "Paris"
    # }
    path('locations/list/', LocationListView.as_view(), name='location-list'),
    #this is a get request to see all the locations and customers can use this as well as the admins and company admins
    path('admin/stations/create/', CreateStationView.as_view(), name='create-station'),
    #this is a post request to add new stations
    #the stations need a location so it will input the location_id from the locations added
    #also the type of the station should be noted(airport or train station or bus station)
    #  {
    #
    #  "name": "ParisBusStation",
    #  "type": "Bus_Station",
    #  "location": 1
    # }
    path('stations/list/', StationListView.as_view(), name='station-list'),
    #this is a get request to see the list of stations
    path('routes/search/', RouteListView.as_view(), name='routes-list'),
    path('admin/routes/create/', RouteCreateView.as_view(), name='create-route'),
    #this is post request for the admin to create routes which includes the locations and stations of the origin and destination
    #  {
    #     "origin_id" : 2,
    #     "destination_id" : 1,
    #     "origin_station_id" : 3,
    #     "destination_station_id" : 2
    #     }
    #it will check the stations to be in the locations and also check the type of the stations to match
    path('company/ticket/create/', TripCreateView.as_view(), name='create-ticket'),
    #this is a post request for the company admin to add tickets
    #the tickets need a vehicle id and route id
    #also the departure time and the duration of the trip
    # the input will include the details of the prices for different sections by section id
    #so in this api first the trip will be created which includes the basic info like the route id and vehicle id and the departure time and duration and then the price and details for sections will be in the ticket and the ticket will have reference to the trip created
    #  sample input :
    #  {
    #     "vehicle_id" : 9,
    #     "route_id" : 17,
    #     "departure_datetime": "2025-08-21",
    #     "duration": "08:30:00",
    #     "ticket_info":[
    #         {"section_id": 25, "price": 40},
    #         {"section_id": 26, "price": 40},
    #         {"section_id": 27, "price": 40},
    #         {"section_id": 28, "price": 40},
    #         {"section_id": 29, "price": 40}
    #     ]
    # }

    # path('trips/list/',   , name='trips-list'),  # not done
    # path('trips/<int:trip_id>/',   , name='trip-details'),  # not done
    path("trips/<int:trip_id>/stops/", TripStopView.as_view(), name="trip-stops"),
    # path('trips/<int:trip_id>/tickets/',  , name='view-trips-tickets'),  # not done
    # path('trips/<int:trip_id>/edit/',  , name='edit-trip'),  # not done
    # path('trips/<int:trip_id>/cancel/',  , name='cancel-trip'),  # not done
    path('customer/tickets/search/', TicketSearchView.as_view(), name='customer-tickets-list'),
    path('admin/tickets/search/', AdminTicketListView.as_view(), name='admin-tickets-list'),
    path('company/tickets/search/', CompanyTicketListView.as_view(), name='company-tickets-list'),
    path('tickets/search/<int:ticket_id>/', TicketCacheDetailView.as_view(), name='ticket-details'),
    path('tickets/<int:ticket_id>/available_seats/', AvailableSeatsView.as_view(), name='available-seats'),
    # path('admin/tickets/<int:ticket_id>/edit/',  , name='edit-ticket'),  # not done
    # path('admin/tickets/<int:ticket_id>/cancel/',  , name='edit-ticket'),  # not done
    path('customer/passenger/create/', CreatePassengerView.as_view(), name='create-passenger'),
    #this is a post request for the customers to add related passengers for themselves to use in the reservation because each reservation needs a specific passenger
    #  {
    #     "name": "ali",
    #     "lastname": "alavi",
    #     "ssn": 1000000000,
    #     "birthdate": "1990-02-12"
    # }
    path('customer/passenger/list/', PassengerListView.as_view(), name='passenger-list'),
    #a get request for the customer to get the list of the customers added for themselves
    path('reservation/create/<int:ticket_id>/', CreateReservationView.as_view(), name='create-reservation'),
    #a post request to actually reserve a ticket
    #this request needs the ticket_id and the seat number as well as the passenger_id(it will be checked that the passenger is related to the account that is making the reservation)
    #it will be checked that the seat number wasn't reserved before
    #this reservation will be reserved in the pending status till the payment is done if the payment hadn't been done by 10 minutes the reservation will be canceled by the system and others can reserve it again
    #  {
    #   "passenger_id": 1,
    #   "seat_number": "10"
    # }
    path('customer/reservation/list/', ReservationListView.as_view(), name='reservation-list'),
    #this is a get request for the customer to see the list of their reservation they can also filter the result list by the date and status
    #the params (date and status will be query params that the user will input)
    #the date can also represent a range like before a certain date or after it all can be done by the queries like this (?date_after=2025-05-01)
    #so this wil give the customer a general info about the reservation and if the customer want to see more details they can use the wanted reservation_id in the next request
    path('customer/reservation/<int:reservation_id>/', CustomerReservationView.as_view(), name='reservation-view'),
    #so this request will give the extra info about the ticket and route and trip of the reservation by the reservation id that is the input
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
    #so this a post request for the customer to pay for thr reservation made by the reservation_id and the specified method()like cash or wallet
    #so if the method is wallet the balance would be checked as well
    #then a confirmation email will be sent to the user with a complete info of the reservation
    path('reservation/<int:reservation_id>/payment_status/', PaymentStatusView.as_view(), name='payment-status'),
    #so this is a get request to show the status of the payment (reservation) by the reservation_id
    #so if the reservation was confirmed by paying it will show something like this
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
    path('payment/history/', PaymentHistoryView.as_view(), name='payment-history'),
    #this is a get request for the customer to see all the payments made
    #this will hae the reservation id  and amount and method of the payment as well as the date-time and the status which can be confirmed of refunded if the reservation was canceled
    path('reservation/<int:reservation_id>/cancellation/info/', ReservationCancelInfoView.as_view(), name='reservation-cancellation-info'),
    #this is a get request for when the customer wants to cancel a reservation so first by using this api they see the full info of the reservation
    #if the reservation was confirmed and had a payment it will also show the penalty that they have to pay and the refund amount which will be returned to their wallet
    #but if the status was pending only the reservation info and the ticket price is shown
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

    path('reservation/<int:reservation_id>/cancel/', ReservationCancelConfirmView.as_view(), name='reservation-cancel'),
    #so this is a post request which will actually cancel the reservation by the reservation id
    #and if the reservation was confirmed it will refund the price of the ticket minus the penalty
    path('admin/cancel/reservation/', AdminCancelReservationView.as_view(), name='admin-cancel-reservation'),
    #this api is used by admins to cancel a reservation for a customer by the reservation_id
    #after the cancellation the price will be refunded to the customers wallet and a notice will be sent to them by email
    path('admin/reservation/list/', AdminReservationFilterView.as_view(), name='admin-reservation-list'),
    #this is a get request for the admin to see the reservation and it will use query params just like the get request for reservation for the customer
    path('admin/reservation/<int:reservation_id>/', AdminReservationView.as_view() , name='admin-view-reservation'),
    #again just like the customer admin can use this api to see the full detailed info of the reservation including trip and ticket and route info
    path('admin/reservation/<int:reservation_id>/edit/', AdminEditReservationView.as_view() , name='admin-edit-reservation'),
    path('admin/reservation/<int:reservation_id>/confirm/', AdminConfirmReservationView.as_view(),name='admin-confirm-reservation'),
]