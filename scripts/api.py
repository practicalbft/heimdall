import requests
import logging
import api

logger = logging.getLogger(__name__)

PROM_URL = "http://localhost:6061/api/v1"
NODE_COUNT = 6

def get_number_of_byz():
    n = get_number_of_nodes()
    if n < 11:
        return 1
    elif n < 16:
        return 2
    else:
        return 3

def get_number_of_nodes():
    data = get_time_series_for_q('count(up{job="bft-list"} == 1)')
    if len(data) == 0:
        return 0
    return int(data[0]["value"][1])

def get_time_series_for_q(q):
    logger.info(f"Querying Prometheus for q={q}")
    url = f"{PROM_URL}/query?query={q}"
    r = requests.get(url)
    return r.json()["data"]["result"]

def create_snapshot():
    url = f"{PROM_URL}/admin/tsdb/snapshot"
    logger.info("Creating Prometheus snapshot")
    r = requests.post(url)
    res = r.json()
    if res["status"] == "error":
        raise ValueError(f"Got error when creating snapshot: {res['error']}")

    return res["data"]["name"]