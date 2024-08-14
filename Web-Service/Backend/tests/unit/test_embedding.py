from genai.embedding_handler import retrieve_products

def test_retrieve_products():
    products = retrieve_products(prompt="blue jeans", category="men_clothing")
    assert len(products) > 1