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
    path('locations/list/', LocationListView.as_view(), name='location-list'),
    path('admin/stations/create/', CreateStationView.as_view(), name='create-station'),
    path('stations/list/', StationListView.as_view(), name='station-list'),
    path('routes/search/', RouteListView.as_view(), name='routes-list'),
    path('admin/routes/create/', RouteCreateView.as_view(), name='create-route'),
    path('company/ticket/create/', TripCreateView.as_view(), name='create-ticket'),
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
    # path('admin/tickets/<int:ticket_id>/edit/',  , name='edit-ticket'),  # not done
    # path('admin/tickets/<int:ticket_id>/cancel/',  , name='edit-ticket'),  # not done
    path('customer/passenger/create/', CreatePassengerView.as_view(), name='create-passenger'),
    path('customer/passenger/list/', PassengerListView.as_view(), name='passenger-list'),
    path('reservation/create/', CreateReservationView.as_view(), name='create-reservation'),
    path('customer/reservation/list/', ReservationListView.as_view(), name='reservation-list'),
    path('customer/reservation/<int:reservation_id>/', CustomerReservationView.as_view(), name='reservation-view'),
    path('customer/reservation/<int:reservation_id>/pay/', ReservationPaymentView.as_view(), name='reservation-payment'),
    path('reservation/<int:reservation_id>/payment_status/', PaymentStatusView.as_view(), name='payment-status'),
    path('payment/history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('reservation/cancellation/info/', ReservationCancelInfoView.as_view(), name='reservation-cancellation-info'),
    path('reservation/cancel/', ReservationCancelConfirmView.as_view(), name='reservation-cancel'),
    path('admin/cancel/reservation/', AdminCancelReservationView.as_view(), name='admin-cancel-reservation'),
    path('admin/reservation/list/', AdminReservationFilterView.as_view(), name='admin-reservation-list'),
    path('admin/reservation/<int:reservation_id>/', AdminReservationView.as_view() , name='admin-view-reservation'),
    path('admin/reservation/<int:reservation_id>/edit/', AdminEditReservationView.as_view() , name='admin-edit-reservation'),
    path('admin/reservation/<int:reservation_id>/confirm/', AdminConfirmReservationView.as_view(),name='admin-confirm-reservation'),
]