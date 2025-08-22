from celery import shared_task
from bookings.models import Ticket
from elasticsearch import Elasticsearch
from bookings.management.commands.index_tickets_es import TICKET_INDEX
from search.es_client import get_es
from cache_utils import get_ticket_cache, set_ticket_cache

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

        trip = ticket.trip
        section = ticket.section
        vehicle = trip.vehicle if trip else None
        route = trip.route if trip else None
        company = vehicle.company if vehicle else None
        origin_station = route.origin_station if route else None

        doc = {
            "ticket_id": str(getattr(ticket, "ticket_id", ticket.pk)),
            "price": float(getattr(ticket, "price", 0)),
            "remaining_seats": getattr(ticket, "remaining_seats", 0),
            "section": getattr(section, "name", "") if section else "",
            "vehicle": {
                "name": getattr(vehicle, "name", "") if vehicle else "",
                "type": getattr(vehicle, "type", "") if vehicle else "",
                "class_code": getattr(vehicle, "class_code", "") if vehicle else "",
            },
            "route": {
                "origin_id": str(getattr(route.origin, "location_id", "")) if route and route.origin else "",
                "destination_id": str(
                    getattr(route.destination, "location_id", "")) if route and route.destination else "",
                "origin": getattr(route.origin, "city", "") if route and route.origin else "",
                "destination": getattr(route.destination, "city", "") if route and route.destination else "",
                "origin_station": getattr(origin_station, "name", "") if origin_station else "",
                "destination_station": getattr(route.destination_station, "name",
                                               "") if route and route.destination_station else "",
                "origin_country": getattr(route.origin, "country", "") if route and route.origin else "",
                # <-- ADDED
                "destination_country": getattr(route.destination, "country",
                                               "") if route and route.destination else "",  # <-- ADDED
            },
            "trip": {
                "trip_id": str(getattr(trip, "trip_id", "")) if trip else "",
                "departure_datetime": trip.departure_datetime.isoformat() if trip and getattr(trip,
                                                                                              "departure_datetime",
                                                                                              None) else "",
                "duration": str(getattr(trip, "duration", "")) if trip else "",
                "company_id": str(getattr(company, "company_id", "")) if company else "",
                "company_name": getattr(company, "name", "") if company else "",
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

@shared_task(bind=True, max_retries=5, default_retry_delay=60, queue='tickets')
def update_ticket_in_es_and_cache(self, ticket_id, fields: dict):
    try:
        es.update(
            index=TICKET_INDEX,
            id=ticket_id,
            body={"doc": fields},
            refresh="wait_for"
        )

        updated_doc = es.get(index=TICKET_INDEX, id=ticket_id)["_source"]

        set_ticket_cache(ticket_id, updated_doc)

        return f"Ticket {ticket_id} updated and cache refreshed"

    except Ticket.DoesNotExist:
        self.retry(exc=Exception(f"Ticket {ticket_id} does not exist"), countdown=60)
    except Exception as exc:
        raise self.retry(exc=exc)