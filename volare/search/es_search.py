from search.es_client import get_es
from elasticsearch import Elasticsearch

es: Elasticsearch = get_es()
INDEX = "tickets_index"


def search_tickets_es(filters):
    query = {"bool": {"must": [], "filter": []}}

    # Exact match filters, using terms for robust matching
    if "origin_id" in filters:
        # Querying the string ID field directly from the index
        query["bool"]["filter"].append({"term": {"route.origin_id": str(filters["origin_id"])}})

    if "destination_id" in filters:
        # Querying the string ID field directly from the index
        query["bool"]["filter"].append({"term": {"route.destination_id": str(filters["destination_id"])}})

    if "company_id" in filters:
        query["bool"]["filter"].append({"term": {"trip.company_id": filters["company_id"]}})
    if "transport_type" in filters:
        transport_type_lower = filters["transport_type"].lower()
        query["bool"]["filter"].append({
            "terms": {
                "vehicle.type": [transport_type_lower, filters["transport_type"]]
            }
        })
    if "class_code" in filters:
        query["bool"]["filter"].append({"term": {"vehicle.class_code": filters["class_code"]}})
    if "min_price" in filters:
        query["bool"]["filter"].append({"range": {"price": {"gte": float(filters["min_price"])}}})
    if "max_price" in filters:
        query["bool"]["filter"].append({"range": {"price": {"lte": float(filters["max_price"])}}})
    if "departure_date_exact" in filters:
        query["bool"]["filter"].append({"term": {"trip.departure_datetime": filters["departure_date_exact"]}})
    if "departure_date_start" in filters or "departure_date_end" in filters:
        range_query = {}
        if "departure_date_start" in filters:
            range_query["gte"] = filters["departure_date_start"]
        if "departure_date_end" in filters:
            range_query["lte"] = filters["departure_date_end"]
        query["bool"]["filter"].append({"range": {"trip.departure_datetime": range_query}})

    # Text search / other conditions
    if "search" in filters:
        query["bool"]["must"].append({"range": {"remaining_seats": {"gt": 0}}})
        query["bool"]["must"].append({"range": {"trip.departure_datetime": {"gt": "now"}}})

    # Sorting
    order = filters.get("order", "DESC")
    sort = [{"trip.departure_datetime": {"order": order.lower()}}]
    print("FILTERS:", filters)
    print("QUERY:", query)

    # Execute search
    response = es.search(index=INDEX, query=query, sort=sort, size=1000)

    results = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        vehicle = source.get("vehicle", {})
        trip = source.get("trip", {})
        results.append({
            "ticket_id": source["ticket_id"],
            "price": source["price"],
            "remaining_seats": source["remaining_seats"],
            "transport_type": source["vehicle"]["type"],
            "section": source["section"],
            "origin": source["route"]["origin"],
            "destination": source["route"]["destination"],
            "departure_datetime": trip.get("departure_datetime"),
            "company": trip.get("company_name"),
        })

    return results