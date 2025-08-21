from elasticsearch import Elasticsearch
from rest_framework import serializers
from django.db import connection
from cache_utils import get_ticket_cache, set_ticket_cache
from search.es_search import search_tickets_es
from search.indexes import TICKET_INDEX
from search.es_client import get_es

es: Elasticsearch = get_es()

def build_ticket_detail(ticket_id):
    cached = get_ticket_cache(ticket_id)
    if cached:
        return cached

    res = es.get(index=TICKET_INDEX, id=ticket_id)
    ticket_data = res["_source"]

    set_ticket_cache(ticket_id, ticket_data)

    return ticket_data


def search(filters):
    es_results = search_tickets_es(filters)

    results = []
    for ticket in es_results:
        ticket_summary = {
            "ticket_id": ticket.get("ticket_id"),
            "price": ticket.get("price"),
            "remaining_seats": ticket.get("remaining_seats"),
            "transport_type": ticket.get('transport_type'),
            "class_code": ticket.get('class_code'),
            "section": ticket.get("section"),
            "origin": ticket.get('origin'),
            "destination": ticket.get('destination'),
            "origin_station": ticket.get('origin_station'),
            "destination_station": ticket.get('destination_station'),
            "departure_datetime": ticket.get('departure_datetime'),
            "company_name": ticket.get('company_name'),
            "duration": ticket.get('duration'),
        }
        results.append(ticket_summary)
        set_ticket_cache(ticket.get("ticket_id"), build_ticket_detail(ticket.get("ticket_id")))

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