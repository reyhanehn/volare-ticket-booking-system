# volare/cache_utils.py

import json
import decimal
import datetime
from redis_client import redis_client


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)  # or str(obj) if preserving precision is key
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        if isinstance(obj, datetime.timedelta):
            # Return total seconds (float), or string if you want ISO 8601 duration format
            return obj.total_seconds()
        return super().default(obj)


def get_ticket_cache(ticket_id):
    key = f"ticket_detail:{ticket_id}"
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_ticket_cache(ticket_id, data, timeout_seconds=60 * 60):
    key = f"ticket_detail:{ticket_id}"
    serialized = json.dumps(data, cls=CustomJSONEncoder)
    redis_client.setex(key, timeout_seconds, serialized)


def delete_ticket_cache(ticket_id):
    key = f"ticket_detail:{ticket_id}"
    redis_client.delete(key)
