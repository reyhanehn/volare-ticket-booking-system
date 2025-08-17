from rest_framework import serializers
from django.db import connection
from cache_utils import get_ticket_cache, set_ticket_cache
from search.es_search import search_tickets_es


def build_ticket_detail(cursor, ticket_id):
    cursor.execute("""
        SELECT 
            t.ticket_id, t.price, t.remaining_seats, t.seat_start_number, t.seat_end_number,
            vs.name AS section, v.name, v.type, v.class_code, v.layout,
            r.route_id, o.city AS origin, d.city AS destination,
            s1.name AS origin_station, s2.name AS destination_station,
            trip.trip_id, trip.departure_datetime, trip.duration,
            c.name AS company_name,
            vs.vehicle_id
        FROM bookings_ticket t
        JOIN bookings_trip trip ON t.trip_id = trip.trip_id
        JOIN companies_vehiclesection vs ON t.section_id = vs.section_id
        JOIN companies_vehicle v ON trip.vehicle_id = v.vehicle_id
        JOIN bookings_route r ON trip.route_id = r.route_id
        JOIN bookings_location o ON r.origin_id = o.location_id
        JOIN bookings_location d ON r.destination_id = d.location_id
        LEFT JOIN bookings_station s1 ON r.origin_station_id = s1.station_id
        LEFT JOIN bookings_station s2 ON r.destination_station_id = s2.station_id
        JOIN companies_company c ON v.company_id = c.company_id
        WHERE t.ticket_id = %s
    """, [ticket_id])
    ticket_detail_row = cursor.fetchone()

    cursor.execute("""
        SELECT ts.stop_order, ts.stop_type, st.name, ts.duration
        FROM bookings_tripstop ts
        LEFT JOIN bookings_station st ON ts.station_id = st.station_id
        WHERE ts.trip_id = %s
        ORDER BY ts.stop_order
    """, [ticket_detail_row[15]])
    stops = cursor.fetchall()
    stop_list = [
        {
            "stop_order": s[0],
            "stop_type": s[1],
            "station_name": s[2],
            "duration": s[3]
        } for s in stops
    ]

    cursor.execute("""
        SELECT s.name
        FROM companies_service s
        JOIN companies_vehicleservice vs ON vs.service_id = s.service_id
        WHERE vs.vehicle_id = %s
    """, [ticket_detail_row[19]])
    services = cursor.fetchall()
    service_list = [
        {"name": s[0]} for s in services
    ]

    return {
        "ticket_id": ticket_detail_row[0],
        "price": ticket_detail_row[1],
        "remaining_seats": ticket_detail_row[2],
        "seat_range": f"{ticket_detail_row[3]}–{ticket_detail_row[4]}",
        "section": ticket_detail_row[5],
        "vehicle": {
            "name": ticket_detail_row[6],
            "type": ticket_detail_row[7],
            "class_code": ticket_detail_row[8],
            "layout": ticket_detail_row[9],
        },
        "route": {
            "origin": ticket_detail_row[11],
            "destination": ticket_detail_row[12],
            "origin_station": ticket_detail_row[13],
            "destination_station": ticket_detail_row[14],
        },
        "trip": {
            "trip_id": ticket_detail_row[15],
            "departure_datetime": ticket_detail_row[16],
            "duration": ticket_detail_row[17],
            "company": ticket_detail_row[18],
        },
        "stops": stop_list,
        "services": service_list
    }


def search(filters):
    # Run ES search
    es_results = search_tickets_es(filters)

    results = []
    for ticket in es_results:
        ticket_id = ticket.get("ticket_id")
        ticket_summary = {
            "ticket_id": ticket_id,
            "price": ticket.get("price"),
            "remaining_seats": ticket.get("remaining_seats"),
            "transport_type": ticket.get("transport_type"),
            "section": ticket.get("section"),
            "origin": ticket.get("origin"),
            "destination": ticket.get("destination"),
            "departure_datetime": ticket.get("departure_datetime"),
            "company": ticket.get("company"),
        }
        results.append(ticket_summary)

        # Cache detailed info if not cached
        if not get_ticket_cache(ticket_id):
            detail = build_ticket_detail(connection.cursor(), ticket_id)
            set_ticket_cache(ticket_id, detail)

    return results

class BaseTicketFilterSerializer(serializers.Serializer):
    origin_id = serializers.IntegerField(required=False)
    destination_id = serializers.IntegerField(required=False)
    departure_date_exact = serializers.DateField(required=False)
    departure_date_start = serializers.DateField(required=False)
    departure_date_end = serializers.DateField(required=False)
    departure_time = serializers.TimeField(required=False)
    transport_type = serializers.CharField(required=False)
    class_code = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    order = serializers.ChoiceField(choices=["ASC", "DESC"], required=False)

    def validate(self, data):
        if 'departure_date_exact' in data and (('departure_date_start' in data) or ('departure_date_end' in data)):
            raise serializers.ValidationError("you can't set an exact date and also an interval")
        return data


class TicketSearchSerializer(BaseTicketFilterSerializer):
    company_id = serializers.IntegerField(required=False)

    def search(self):
        filters = self.validated_data
        filters['search'] = True
        results = search(filters)
        return results


class TicketDetailSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    def to_representation(self, instance):
        ticket_id = instance.get("ticket_id")
        if not ticket_id:
            return {}

        # Try cache first
        cached_data = get_ticket_cache(ticket_id)
        if cached_data:
            return cached_data

        # If no cache, query DB
        ticket_detail = build_ticket_detail(connection.cursor(), ticket_id)
        if not ticket_detail:
            return {}

        # Cache the result for next time
        set_ticket_cache(ticket_id, ticket_detail)

        return ticket_detail


class AdminTicketListSerializer(BaseTicketFilterSerializer):
    company_id = serializers.IntegerField(required=False)

    def search(self):
        filters = self.validated_data
        filters['search'] = True
        results = search(filters)
        return results


class CompanyTicketListSerializer(BaseTicketFilterSerializer):

    def __init__(self, *args, **kwargs):
        self.company_id = kwargs.pop("context")["company_id"]
        super().__init__(*args, **kwargs)


    def search(self):
        filters = self.validated_data
        filters['company_id'] = self.company_id
        results = search(filters)
        return results
