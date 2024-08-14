from fastapi.testclient import TestClient
import sys
import os
import sys
import pprint
pprint.pprint(sys.path)
import os
from main import app


client = TestClient(app)


def test_product_search():
    payload = {
        "category": "men_clothing",
        "query": "blue jeans",
    }
    response = client.post("/show-more/",  json=payload)
    assert  len(response.json()['response']) > 0
   