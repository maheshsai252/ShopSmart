from helpers.helper_functions import is_greeting
from prompt.prompt_handler import create_user_query_answering_cart
from genai.genai_handler import call_openai_api
import json
from cart.user_cart_handler import get_review_summaries
def condense_messages(messages):
    collective_chat = "User's messages:"
    for msg in messages:
        if msg.role == 'user':
            collective_chat += f"User: {msg.content}\n"
    prompt = collective_chat + """
    Decide if users latest question is follow up to previous ones, if it is followup, create a standalone query else retuen the latest query. 
    If user query is outside fashion suggestions or relaed to products, blend user query into fashion domain. In either case, return query only.
    """
    return call_openai_api(prompt)
def answer_questions_for_cart(cartReq):
    messages = cartReq.messages
    ref_products = cartReq.products
    response = {
        "bot":  "Hello! How can I assist you today?",
        "products": []
    }
    if is_greeting(messages[-1].content):
        response['bot'] = "Hello! How can I assist you today?"
        response['products'] = []
    else:
        product_details = ""
        asins = list(map(lambda x: x.asin, ref_products))
        summaries = get_review_summaries(asins)
        print(summaries,"finally")
        for product in ref_products:
            product_details+=f"\ntitle: {product.title}"
            product_details+= f"\ndescription: {product.summary}"
            product_details+= f"\nasin: {product.asin}"
            product_details+= f"\nReviews: {summaries[product.asin] if product.asin in summaries else '' }"
        final_msg = messages[-1].content
        if len(messages) > 1:
            final_msg = condense_messages(messages=messages)
        print(final_msg)
        prompt = create_user_query_answering_cart(message=final_msg, product_info=product_details)
        response_message = call_openai_api(prompt)
        try:
            response = {}
            start_index = response_message.index('{')
            end_index = response_message.rindex('}')
            print(response_message[start_index:end_index+1])
            res = json.loads(response_message[start_index:end_index+1])
            targets = res['products']
            response['bot'] = res['message']
            response['products'] = list(filter(lambda x: x.asin in targets,ref_products))
        except Exception as e:
            print(str(e))
    return {"response": response}