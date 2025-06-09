from rest_framework import serializers
from django.db import connection
from cache_utils import get_ticket_cache, set_ticket_cache



class TicketSearchSerializer(serializers.Serializer):
    origin_id = serializers.IntegerField(required=False)
    destination_id = serializers.IntegerField(required=False)
    departure_date = serializers.DateField(required=False)
    departure_time = serializers.TimeField(required=False)
    transport_type = serializers.CharField(required=False)
    class_code = serializers.IntegerField(required=False)
    company_id = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)

    def search(self):
        filters = self.validated_data
        sql = '''
            SELECT 
                t.ticket_id,
                t.price,
                t.remaining_seats,
                v.type AS transport_type,
                vs.name AS section,
                o.city AS origin,
                d.city AS destination,
                trip.departure_datetime,
                c.name AS company_name
            FROM bookings_ticket t
            JOIN bookings_trip trip ON t.trip_id = trip.trip_id
            JOIN companies_vehicle v ON trip.vehicle_id = v.vehicle_id
            JOIN companies_vehiclesection vs ON t.section_id = vs.section_id
            JOIN bookings_route r ON trip.route_id = r.route_id
            JOIN bookings_location o ON r.origin_id = o.location_id
            JOIN bookings_location d ON r.destination_id = d.location_id
            JOIN companies_company c ON v.company_id = c.company_id
            WHERE 1=1
        '''
        params = []

        # Add filters dynamically
        if 'origin_id' in filters:
            sql += " AND r.origin_id = %s"
            params.append(filters['origin_id'])
        if 'destination_id' in filters:
            sql += " AND r.destination_id = %s"
            params.append(filters['destination_id'])
        if 'departure_date' in filters:
            sql += " AND DATE(trip.departure_datetime) = %s"
            params.append(filters['departure_date'])
        if 'departure_time' in filters:
            sql += " AND TIME(trip.departure_datetime) >= %s"
            params.append(filters['departure_time'])
        if 'transport_type' in filters:
            sql += " AND v.type = %s"
            params.append(filters['transport_type'])
        if 'class_code' in filters:
            sql += " AND v.class_code = %s"
            params.append(filters['class_code'])
        if 'company_id' in filters:
            sql += " AND v.company_id = %s"
            params.append(filters['company_id'])
        if 'min_price' in filters:
            sql += " AND t.price >= %s"
            params.append(filters['min_price'])
        if 'max_price' in filters:
            sql += " AND t.price <= %s"
            params.append(filters['max_price'])

        results = []
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            for row in rows:
                ticket_summary = {
                    "ticket_id": row[0],
                    "price": row[1],
                    "remaining_seats": row[2],
                    "transport_type": row[3],
                    "section": row[4],
                    "origin": row[5],
                    "destination": row[6],
                    "departure_datetime": row[7],
                    "company": row[8],
                }
                results.append(ticket_summary)

                ticket_id = row[0]
                if not get_ticket_cache(ticket_id):
                    # Query full ticket detail
                    cursor.execute("""
                        SELECT 
                            t.ticket_id, t.price, t.remaining_seats, t.seat_start_number, t.seat_end_number,
                            vs.name AS section, v.name, v.type, v.class_code, v.layout,
                            r.route_id, o.city AS origin, d.city AS destination,
                            s1.name AS origin_station, s2.name AS destination_station,
                            trip.trip_id, trip.departure_datetime, trip.duration,
                            c.name AS company_name
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

                    full_ticket_detail = {
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
                        "stops": stop_list
                    }

                    set_ticket_cache(ticket_id, full_ticket_detail)

        return results


class TicketDetailSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()

    def get_ticket_from_db(self, ticket_id):
        with connection.cursor() as cursor:
            # Fetch ticket detail row
            cursor.execute("""
                SELECT 
                    t.ticket_id, t.price, t.remaining_seats, t.seat_start_number, t.seat_end_number,
                    vs.name AS section, v.name, v.type, v.class_code, v.layout,
                    r.route_id, o.city AS origin, d.city AS destination,
                    s1.name AS origin_station, s2.name AS destination_station,
                    trip.trip_id, trip.departure_datetime, trip.duration,
                    c.name AS company_name
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

            if not ticket_detail_row:
                return None

            # Fetch stops
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

            full_ticket_detail = {
                "ticket_id": ticket_detail_row[0],
                "price": ticket_detail_row[1],
                "remaining_seats": ticket_detail_row[2],
                "seat_range": f"{ticket_detail_row[3]}–{ticket_detail_row[4]}",
                "section": {
                    "name": ticket_detail_row[5],
                },
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
                "stops": stop_list
            }

            return full_ticket_detail

    def to_representation(self, instance):
        ticket_id = instance.get("ticket_id")
        if not ticket_id:
            return {}

        # Try cache first
        cached_data = get_ticket_cache(ticket_id)
        if cached_data:
            return cached_data

        # If no cache, query DB
        ticket_detail = self.get_ticket_from_db(ticket_id)
        if not ticket_detail:
            return {}

        # Cache the result for next time
        set_ticket_cache(ticket_id, ticket_detail)

        return ticket_detail
