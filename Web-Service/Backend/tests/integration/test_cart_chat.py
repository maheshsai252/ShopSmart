from models.pydantic_models import Message, Product, CartBotReq
from cart.cart_chat_handler import answer_questions_for_cart
from fastapi.testclient import TestClient
import sys
import sys
import pprint
pprint.pprint(sys.path)
from main import app


client = TestClient(app)


def test_greeting():
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "hi"
            }
        ],
        "products": []
    }
    response = client.post("/cart-message/",  json=payload)
    print(response)
    assert 'Hello!' in response.json()['response']['bot']


def test_cart_response():
    m1 = Message(role="user",content = "does jeans suit my shirt?")
    messages = [m1]
    p1 = Product(title= "jeans", imageURLHighRes= "str", category= "men_clothing", asin = "a1", summary= "men blue jeans")
    p2 = Product(title= "shirts", imageURLHighRes= "str", category= "men_clothing", asin = "a1", summary= "men white shirts")

    products = [p1,p2]
    req = CartBotReq(messages = messages, products = products)
    res = answer_questions_for_cart(cartReq=req)
    assert len(res['response']['bot']) > 0
