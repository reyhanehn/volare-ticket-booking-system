from celery import shared_task
from bookings.models import Ticket
from elasticsearch import Elasticsearch
from search.indexes import TICKET_INDEX
from search.es_client import get_es

@shared_task(queue='reservations')
def cancel_expired_reservations():
    from django.utils import timezone
    from .models import Reservation, ReservationStatus

    now = timezone.now()
    expired = Reservation.objects.filter(
        status=ReservationStatus.PENDING,
        expiration_time__lte=now
    )

    count = expired.count()
    expired.update(status=ReservationStatus.CANCELLED)

    return f"Cancelled {count} expired reservations"

es: Elasticsearch = get_es()

@shared_task(bind=True, max_retries=5, default_retry_delay=60, queue='tickets')
def index_ticket_to_es(self, ticket_id):
    try:
        # Fetch ticket with related objects
        ticket = Ticket.objects.select_related(
            "trip", "section", "trip__vehicle", "trip__route",
            "trip__route__origin", "trip__route__destination"
        ).get(pk=ticket_id)

        trip = getattr(ticket, "trip", None)
        section = getattr(ticket, "section", None)
        vehicle = getattr(trip, "vehicle", None) if trip else None
        route = getattr(trip, "route", None) if trip else None
        origin = getattr(route, "origin", None) if route else None
        destination = getattr(route, "destination", None) if route else None
        company_name = getattr(trip, "company_name", "") if trip else ""

        doc = {
            "ticket_id": str(getattr(ticket, "ticket_id", ticket.pk)),
            "price": float(getattr(ticket, "price", 0)),
            "remaining_seats": getattr(ticket, "remaining_seats", 0),
            "section": getattr(section, "name", "") if section else "",
            "vehicle": {
                "type": getattr(vehicle, "type", "") if vehicle else "",
                "class_code": str(getattr(vehicle, "class_code", "")) if vehicle else "",
            },
            "route": {
                "origin_id": str(getattr(origin, "location_id", "")) if origin else "",
                "destination_id": str(getattr(destination, "location_id", "")) if destination else "",
                "origin": getattr(origin, "city", "") if origin else "",
                "destination": getattr(destination, "city", "") if destination else "",
            },
            "trip": {
                "trip_id": str(getattr(trip, "trip_id", "")) if trip else "",
                "departure_datetime": trip.departure_datetime.isoformat() if trip and getattr(trip, "departure_datetime", None) else "",
                "company_id": str(getattr(trip, "company_id", "")) if trip else "",
                "company_name": company_name,
            },
        }

        # Index the document in Elasticsearch
        es.index(index=TICKET_INDEX, id=ticket.ticket_id, document=doc)

    except Ticket.DoesNotExist:
        # Ticket no longer exists
        self.retry(exc=Exception(f"Ticket {ticket_id} does not exist"), countdown=60)
    except Exception as exc:
        # Retry on other exceptions
        raise self.retry(exc=exc)