from cart.user_cart_handler import get_user_cart_products
from cart.user_activities import get_user_activities
def test_non_empty_cart():
    products = get_user_cart_products(1)
    assert len(products) > 0

def test_non_empty_activities():
    activities = get_user_activities(user_id=1)
    assert len(activities) > 0

