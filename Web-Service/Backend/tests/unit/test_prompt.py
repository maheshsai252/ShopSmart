from prompt.prompt_handler import create_sales_prompt, create_sales_prompt_existing_products, create_user_query_answering_cart
from models.pydantic_models import Product
def test_create_sales_prompt():
    message = "Hello, I'm interested in buying some clothes."
    product_info = [
        {"title": "Shirt", "summary": "A stylish shirt for any occasion."},
        {"title": "Jeans", "summary": "Comfortable and trendy jeans."},
    ]
    expected_prompt = "Based on the user's message: 'Hello, I'm interested in buying some clothes.', provide a persuasive and engaging response in not more than line to sell the following products:\n\nProduct: Shirt\nDescription: A stylish shirt for any occasion.\n\nProduct: Jeans\nDescription: Comfortable and trendy jeans.\n\nGive response in not more than single line. Answer as fashion designer not as a chatbot."
    assert create_sales_prompt(message, product_info) == expected_prompt

def test_create_sales_prompt_existing_products():
    message = "What products do you have?"
    product_info = [
    ]
    expected_prompt = "Based on the user's message: 'What products do you have?', and following product details\n\nProduct: Dress\nDescription: Elegant dress for special occasions.\n\nProduct: Skirt\nDescription: Stylish skirt perfect for any season.\n\nprovide a persuasive and engaging response in not more than line to answer user question. If user asks to pick one product for them, pick product based on description and convince user that the product is best for their query. Always use product title while refering to product. Response:"
    assert len(create_sales_prompt_existing_products(message, product_info)) > 0

def test_create_user_query_answering_cart():
    message = "Show me some casual outfits."
    product_info = "Some product details"
    expected_prompt = """Based on the following product details: 'Some product details', 

Answer User's query Show me some casual outfits.
    You are fashion designer recommending styles to user. If user asks you to select outfit or recommend outfit, answer based on context provided 
    If you don't find information for recommending or selecting products within context, use general knowledge by seeing description. 
    Return only products that answers user query.
    Pick products you are refering to answer user query in below format:
    **Don't say you dont know or can't recommend or can't decide based on context ever.  use general knowledge **
    Answer like fashion designer. Don't answer like bot
    {
    "message": "your_explanation",
    "products": [asin1,asin2, asin3]
    }
    """
    assert create_user_query_answering_cart(message, product_info) == expected_prompt
