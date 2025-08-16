from elasticsearch import Elasticsearch
from django.conf import settings

def get_es() -> Elasticsearch:
    cfg = settings.ELASTICSEARCH
    return Elasticsearch(
        hosts=cfg["hosts"],
        basic_auth=(cfg["username"], cfg["password"]) if cfg["username"] else None,
        verify_certs=cfg.get("verify_certs", True),
        request_timeout=10,
    )
