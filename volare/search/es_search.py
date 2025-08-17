from search.es_client import get_es

es = get_es()
INDEX = "tickets_index"

def search_tickets_es(filters):
    query = {"bool": {"must": [], "filter": []}}

    # Exact match filters
    if "origin_id" in filters:
        query["bool"]["filter"].append({"term": {"route.origin_id": filters["origin_id"]}})
    if "destination_id" in filters:
        query["bool"]["filter"].append({"term": {"route.destination_id": filters["destination_id"]}})
    if "company_id" in filters:
        query["bool"]["filter"].append({"term": {"trip.company_id": filters["company_id"]}})
    if "transport_type" in filters:
        query["bool"]["filter"].append({"term": {"vehicle.type": filters["transport_type"]}})
    if "class_code" in filters:
        query["bool"]["filter"].append({"term": {"vehicle.class_code": filters["class_code"]}})
    if "min_price" in filters:
        query["bool"]["filter"].append({"range": {"price": {"gte": filters["min_price"]}}})
    if "max_price" in filters:
        query["bool"]["filter"].append({"range": {"price": {"lte": filters["max_price"]}}})
    if "departure_date_exact" in filters:
        query["bool"]["filter"].append({
            "term": {"trip.departure_date": filters["departure_date_exact"]}
        })
    if "departure_date_start" in filters or "departure_date_end" in filters:
        range_query = {}
        if "departure_date_start" in filters:
            range_query["gte"] = filters["departure_date_start"]
        if "departure_date_end" in filters:
            range_query["lt"] = filters["departure_date_end"]
        query["bool"]["filter"].append({"range": {"trip.departure_date": range_query}})

    # Text search (optional)
    if "search" in filters:
        query["bool"]["must"].append({"range": {"remaining_seats": {"gt": 0}}})
        query["bool"]["must"].append({"range": {"trip.departure_datetime": {"gt": "now"}}})

    # Sorting
    order = filters.get("order", "DESC")
    sort = [{"trip.departure_datetime": {"order": order.lower()}}]

    # Execute search
    response = es.search(index=INDEX, query=query, sort=sort, size=1000)  # size=1000 can be adjusted

    results = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        results.append({
            "ticket_id": source["ticket_id"],
            "price": source["price"],
            "remaining_seats": source["remaining_seats"],
            "transport_type": source["vehicle"]["type"],
            "section": source["section"],
            "origin": source["route"]["origin"],
            "destination": source["route"]["destination"],
            "departure_datetime": source["trip"]["departure_datetime"],
            "company": source["trip"]["company_name"],
        })
    return results
