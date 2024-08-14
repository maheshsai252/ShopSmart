from snowflake.snowflake_wrapper import *
from fastapi import FastAPI
from recommendation.recommendations_handler import send_recommendations
from cart.user_cart_handler import get_user_cart_products, insert_user_cart_products, delete_user_cart_products
from cart.cart_chat_handler import answer_questions_for_cart
from search.search_handler import search_user_query
from models.pydantic_models import Req, cartinsreq, CartBotReq, ShowMoreReq, UserLogin,UserSignup
from search.search_handler import show_more_products
import shutil
from authentication.auth_handler import login_handler, signup_handler
from cart.user_activities import get_user_activities
app = FastAPI(debug=True)

# Signup endpoint
@app.post("/signup")
def signup(user: UserSignup):
    return signup_handler(user)

# Login endpoint with JWT generation
@app.post("/login")
def login(user: UserLogin):
    return login_handler(user=user)

@app.post("/search/")
async def search(req: Req):
    return search_user_query(req)

@app.get("/get-cart/")
async def get_cart(userid: str):
    response = get_user_cart_products(user_id=userid)
    return {"response": response}

@app.get("/get-activities/")
async def get_activities(userid: str):
    response = get_user_activities(user_id=userid)
    return {"response": response}

@app.post("/add-cart/")
async def add_cart(cart_ins: cartinsreq):
    response = insert_user_cart_products(user_id=cart_ins.userid, product_id=cart_ins.product_id)
    return {"response": response}

@app.post("/delete-cart/")
async def delete_cart(cart_ins: cartinsreq):
    response = delete_user_cart_products(user_id=cart_ins.userid, product_id=cart_ins.product_id)
    return {"response": response}

@app.post("/show-more/")
async def show_more(show_more_req: ShowMoreReq):
    response = show_more_products(show_more_req)
    return response

@app.post("/cart-message/")
async def cart_message(cartReq: CartBotReq):
   return answer_questions_for_cart(cartReq=cartReq)

@app.get("/user-recommendations/")
async def recommendations(user_id: int):
    return send_recommendations(user_id=user_id)
    