from django.urls import path

from .views.adminReservationCancellation import AdminCancelReservationView
from .views.locationView import CreateLocationView, LocationListView
from .views.passengerView import CreatePassengerView, PassengerListView
from .views.reservationCancellationView import ReservationCancelInfoView, ReservationCancelConfirmView
from .views.reservationView import CreateReservationView, ReservationListView
from .views.stationView import CreateStationView, StationListView
from .views.routeView import RouteListView, RouteCreateView
from .views.tripView import TripCreateView
from .views.tripStopView import TripStopCreateView
from .views.ticketView import TicketSearchView, TicketCacheDetailView
from .views.paymentView import ReservationPaymentView, PaymentStatusView
from .views.paymentHistoryView import PaymentHistoryView

urlpatterns = [
    path('admin/locations/create/', CreateLocationView.as_view(), name='create-location'),
    path('locations/list/', LocationListView.as_view(), name='location-list'),
    path('admin/stations/create/', CreateStationView.as_view(), name='create-station'),
    path('stations/list/', StationListView.as_view(), name='station-list'),
    path('routes/search/', RouteListView.as_view(), name='routes-list'),
    path('admin/routes/create/', RouteCreateView.as_view(), name='create-route'),
    path('company/ticket/create/', TripCreateView.as_view(), name='create-ticket'),
    path("trips/<int:trip_id>/stops/", TripStopCreateView.as_view(), name="trip-add-stops"),
    path('tickets/search/', TicketSearchView.as_view(), name='tickets-list'),
    path('tickets/search/<int:ticket_id>/', TicketCacheDetailView.as_view(), name='ticket-details'),
    path('customer/passenger/create/', CreatePassengerView.as_view(), name='create-passenger'),
    path('customer/passenger/list/', PassengerListView.as_view(), name='passenger-list'),
    path('reservation/create/', CreateReservationView.as_view(), name='create-reservation'),
    path('customer/reservation/list/', ReservationListView.as_view(), name='reservation-list'),
    path('customer/reservation/<int:reservation_id>/pay/', ReservationPaymentView.as_view(), name='reservation-payment'),
    path('customer/payment/<int:reservation_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
    path('customer/payment/history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('reservation/cancellation/info/', ReservationCancelInfoView.as_view(), name='reservation-cancellation-info'),
    path('reservation/cancel/', ReservationCancelConfirmView.as_view(), name='reservation-cancel'),
    path('admin/cancel/reservation/', AdminCancelReservationView.as_view(), name='admin-cancel-reservation'),
]