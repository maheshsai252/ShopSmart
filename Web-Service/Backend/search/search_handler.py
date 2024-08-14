from search.image_query_handler import handle_image
from prompt.prompt_handler import  create_sales_prompt_existing_products, create_sales_prompt
from helpers.helper_functions import is_greeting
from search.search_helper_functions import pick_products
from snowflake.snowflake_wrapper import insert_user_searches
from genai.embedding_handler import retrieve_products
from genai.genai_handler import call_openai_api
from collections import defaultdict
from snowflake.snowflake_wrapper import retrieve_user_gender, get_product_data
def search_user_query(req):
    message = req.message
    gender = retrieve_user_gender(user_id=req.user_id)
    prompt = ""   
    if req.image != "":
        image_query = handle_image(req.image,message)
        message = image_query['query'] if 'query' in image_query else message

    response = {}

    if is_greeting(message):
        response['bot'] = "Hello! How can I assist you today?"
        response['products'] = []
        response['queries'] = {}
    else:
        all_products = []
        res_cond = pick_products(message, gender=gender)
        response['products']= defaultdict(list)
        response['queries']= defaultdict(str)
        products_descriptions = []
        user_searches = []
        for line in res_cond['products']:
            current_product = {}
            current_product["name"] = line['name']
            current_product["description"] = line['description'] 
            user_searches.append(current_product['description'])
            current_product["category"] = line['category']
            products_descriptions.append(current_product)
        insert_user_searches(req.user_id, user_searches)
        for p in products_descriptions:
            products = retrieve_products(prompt=p['description'] + " " + p['name'] if p['description'] else p['name'], category=p['category'])
            products_data = get_product_data(products)
            response['products'][p['name']] = products_data
            response['queries'][p['name']] = p['description'] + " "+ p['name'] if p['description'] else p['name']
            all_products.extend(products_data)

        sales_prompt = create_sales_prompt(prompt, all_products)
        response['bot'] = call_openai_api(sales_prompt)
   
    return {"response": response}

def show_more_products(req):
    cat = req.category.lower().replace(' ', '_') if req.category else "men_clothing"
    products = retrieve_products(prompt=req.query, category=cat,k=10)
    products = products[5:] if len(products) >5 else products
    products_data = get_product_data(products)
    response = {}   
    response['products'] = products_data
    return {"response": response}