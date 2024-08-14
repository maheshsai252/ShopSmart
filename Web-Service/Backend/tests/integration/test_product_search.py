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
        "image": "",
        "user_id": 1,
        "message": "blue jeans",
    }
    response = client.post("/send/",  json=payload)
    assert 'blue jeans' in response.json()['response']['products'].keys()
    products = response.json()['response']['products']
    for i in products:
        for product in products[i]:
            assert len(product) == 5
            assert 'title' in product
            assert 'asin' in product
            assert 'summary' in product
    queries = response.json()['response']['queries']
    assert len(queries) == 1

