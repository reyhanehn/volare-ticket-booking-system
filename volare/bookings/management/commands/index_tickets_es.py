# In bookings/management/commands/index_tickets_es.py

from django.core.management.base import BaseCommand
from bookings.models import Ticket
from search.es_client import get_es
from search.indexes import TICKET_INDEX, TICKET_MAPPING

class Command(BaseCommand):
    help = "Index all tickets in Elasticsearch"

    def handle(self, *args, **kwargs):
        es = get_es()

        if es.indices.exists(index=TICKET_INDEX):
            self.stdout.write(f"Index '{TICKET_INDEX}' exists, deleting...")
            es.indices.delete(index=TICKET_INDEX)

        es.indices.create(index=TICKET_INDEX, body=TICKET_MAPPING)
        self.stdout.write(self.style.SUCCESS(f"Index '{TICKET_INDEX}' created."))

        tickets = Ticket.objects.select_related(
            "trip",
            "section",
            "trip__vehicle",
            "trip__vehicle__company",
            "trip__route",
            "trip__route__origin",
            "trip__route__destination",
            "trip__route__origin_station",
            "trip__route__destination_station",
        ).all()

        indexed_count = 0
        for ticket in tickets:
            # Safely fetch related objects
            trip = ticket.trip
            section = ticket.section

            vehicle = trip.vehicle if trip else None
            route = trip.route if trip else None
            company = vehicle.company if vehicle else None
            origin_station = route.origin_station if route else None

            # Build the document with all fields, correctly extracting data
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
                    "destination_country": getattr(route.destination, "country", "") if route and route.destination else "",
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

            es.index(index=TICKET_INDEX, id=ticket.ticket_id, document=doc)
            indexed_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {indexed_count} tickets."))