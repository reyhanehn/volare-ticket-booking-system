from elasticsearch import Elasticsearch
from django.conf import settings
import urllib3

# Disable urllib3 warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_es() -> Elasticsearch:
    cfg = settings.ELASTICSEARCH
    return Elasticsearch(
        hosts=cfg["hosts"],
        basic_auth=(cfg["username"], cfg["password"]) if cfg["username"] else None,
        verify_certs=cfg.get("verify_certs", True),
        ssl_show_warn=False,      # suppress SSL warnings in ES client
        request_timeout=60,
    )
