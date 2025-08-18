from django.core.management.base import BaseCommand
from bookings.models import Ticket
from elasticsearch import Elasticsearch
from search.es_client import get_es

# Name of your Elasticsearch index
TICKET_INDEX = "tickets_index"

class Command(BaseCommand):
    help = "Index all tickets in Elasticsearch"

    def handle(self, *args, **kwargs):
        # Connect to Elasticsearch
        es = get_es()

        # Delete index if it exists
        if es.indices.exists(index=TICKET_INDEX):
            self.stdout.write(f"Index '{TICKET_INDEX}' exists, deleting...")
            es.indices.delete(index=TICKET_INDEX)

        # Create index
        es.indices.create(index=TICKET_INDEX)
        self.stdout.write(f"Index '{TICKET_INDEX}' created.")

        # Fetch all tickets
        tickets = Ticket.objects.select_related(
            "trip",
            "section",
            "trip__vehicle",
            "trip__route",
            "trip__route__origin",
            "trip__route__destination"
        ).all()

        for ticket in tickets:
            # Safely fetch related objects
            trip = getattr(ticket, "trip", None)
            section = getattr(ticket, "section", None)
            vehicle = getattr(trip, "vehicle", None) if trip else None
            route = getattr(trip, "route", None) if trip else None
            origin = getattr(route, "origin", None) if route else None
            destination = getattr(route, "destination", None) if route else None

            # Safely get company_name from trip
            company_name = getattr(trip, "company_name", "") if trip else ""

            doc = {
                "ticket_id": str(getattr(ticket, "ticket_id", ticket.pk)),
                "price": float(getattr(ticket, "price", 0)),
                "remaining_seats": getattr(ticket, "remaining_seats", 0),
                "section": getattr(section, "name", "") if section else "",
                "vehicle": {
                    "type": getattr(vehicle, "type", "") if vehicle else "",
                    "class_code": getattr(vehicle, "class_code", "") if vehicle else "",
                    "name": getattr(vehicle, "name", "") if vehicle else "",
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

            # Index the ticket
            es.index(index=TICKET_INDEX, id=ticket.ticket_id, document=doc)

        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {tickets.count()} tickets."))
