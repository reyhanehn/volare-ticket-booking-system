from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

TICKET_INDEX = "tickets_index"

TICKET_MAPPING = {
    "mappings": {
        "properties": {
            "ticket_id": {"type": "keyword"},
            "price": {"type": "float"},
            "remaining_seats": {"type": "integer"},
            "section": {"type": "keyword"},
            "vehicle": {
                "properties": {
                    "type": {"type": "keyword"},
                    "class_code": {"type": "keyword"},
                }
            },
            "route": {
                "properties": {
                    "origin_id": {"type": "keyword"},
                    "destination_id": {"type": "keyword"},
                    "origin": {"type": "keyword"},
                    "destination": {"type": "keyword"},
                }
            },
            "trip": {
                "properties": {
                    "trip_id": {"type": "keyword"},
                    "departure_datetime": {"type": "date"},
                    "company_id": {"type": "keyword"},
                }
            },
        }
    }
}


def create_ticket_index():
    if es.indices.exists(index=TICKET_INDEX):
        es.indices.delete(index=TICKET_INDEX)
    es.indices.create(index=TICKET_INDEX, body=TICKET_MAPPING)