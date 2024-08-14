def create_sales_prompt(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the user's message: '{message}', provide a persuasive and engaging response in not more than line to sell the following products:\n\n"
    for product in product_info:
        sales_prompt += f"Product: {product['title']}\nDescription: {product['summary']}\n\n"
    sales_prompt += "Give response in not more than single line. Answer as fashion designer not as a chatbot."
    return sales_prompt


def create_sales_prompt_existing_products(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the user's message: '{message}', and following product details\n\n"
    for product in product_info:
        sales_prompt += f"Product: {product.title}\nDescription: {product.summary}\n\n"
    sales_prompt += "provide a persuasive and engaging response in not more than line to answer user question. If user asks to pick one product for them, pick product based on description and convince user that the product is best for their query. Always use product title while refering to product. Response:"
    return sales_prompt

def create_user_query_answering_cart(message, product_info):
    """
    Function to create a prompt for selling the products.
    """
    sales_prompt = f"Based on the following product details: '{product_info}', \n\nAnswer User's query {message}"
    sales_prompt += """
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
    return sales_prompt