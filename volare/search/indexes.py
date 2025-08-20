from elasticsearch import Elasticsearch
from search.es_client import get_es

es: Elasticsearch = get_es()
TICKET_INDEX = "tickets_index"

TICKET_MAPPING = {
    "settings": {
        "analysis": {
            "normalizer": {
                "lowercase": {
                    "type": "custom",
                    "char_filter": [],
                    "filter": ["lowercase"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "ticket_id": {"type": "keyword"},
            "price": {"type": "float"},
            "remaining_seats": {"type": "integer"},
            "section": {"type": "keyword"},
            "vehicle": {
                "properties": {
                    "type": {"type": "keyword", "normalizer": "lowercase"},
                    "class_code": {"type": "keyword"},
                }
            },
            "route": {
                "properties": {
                    "origin_id": {"type": "keyword"},
                    "destination_id": {"type": "keyword"},
                    "origin": {"type": "keyword"},
                    "destination": {"type": "keyword"},
                    "origin_station": {"type": "keyword"},
                    "destination_station": {"type": "keyword"},
                    "origin_country": {"type": "keyword"},
                    "destination_country": {"type": "keyword"}
                }
            },
            "trip": {
                "properties": {
                    "trip_id": {"type": "keyword"},
                    "departure_datetime": {"type": "date"},
                    "duration": {"type": "keyword"},
                    "company_id": {"type": "keyword"},
                    "company_name": {"type": "keyword"},
                }
            },
        }
    }
}

def create_ticket_index():
    try:
        if es.indices.exists(index=TICKET_INDEX):
            print(f"Index '{TICKET_INDEX}' exists, deleting...")
            es.indices.delete(index=TICKET_INDEX)
        es.indices.create(index=TICKET_INDEX, body=TICKET_MAPPING)
        print(f"Index '{TICKET_INDEX}' created.")
    except Exception as e:
        print(f"Error creating index '{TICKET_INDEX}': {e}")