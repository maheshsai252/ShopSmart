from cart.user_cart_handler import get_review_summaries
from cart.cart_chat_handler import condense_messages
from models.pydantic_models import Message

def test_non_empty_activities():
    reviews = get_review_summaries(asins=['B00004VWJ3'])
    assert len(reviews) > 0

def test_condense_messages():
    m1 = Message(role="user",content = "does jeans suit my shirt?")
    messages = [m1]
    response = condense_messages(messages=messages)
    assert len(response) > 0