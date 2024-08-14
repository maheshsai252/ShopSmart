from snowflake.snowflake_wrapper import  retrieve_last_5_user_searches,retrieve_user_activities,retrieve_user_gender
from genai.genai_handler import call_openai_api
from genai.embedding_handler import retrieve_products
from snowflake.snowflake_wrapper import get_product_data
import json

def send_recommendations(user_id):
    response = {}
    print("FOR USER", user_id)
    user_searches = retrieve_last_5_user_searches(user_id)
    user_activities =  retrieve_user_activities(user_id)
    user_gender = retrieve_user_gender(user_id)
    print(user_gender, "USER GENDER")
    prompt = f"Considering previous user searches and users interest in activities: {user_searches}\n\n user activities: {user_activities}"+f"""
    curate query to retrieve relevant products under each category:
    ['{user_gender}_clothing', '{user_gender}_watches', '{user_gender}_shoes']
    """+"""
    Don't give none for any category.
    The format of response should be:
    {
        "category1": "query",
        "category2": "query",
        "category3": "query",
    }
    sample response: 
    {
    "men_clothing" : "white men shirts for hiking",
    "men_shoes" : "men shoes for skating",
    "men_watches" : "men watches for gym"
    }
    """
    
    response_message = call_openai_api(prompt)
    try:
        response = {}
        start_index = response_message.index('{')
        end_index = response_message.rindex('}')
        print(response_message[start_index:end_index+1])
        res = json.loads(response_message[start_index:end_index+1])
        for cat in res.keys():
            products = retrieve_products(prompt=res[cat], category=cat)
            products_data = get_product_data(products)
            response[res[cat]] = products_data
    except Exception as e:
        print(str(e))
    return {"response": response}