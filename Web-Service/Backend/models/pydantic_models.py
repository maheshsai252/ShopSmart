from pydantic import BaseModel
from typing import List, Dict
from fastapi import UploadFile
class Message(BaseModel):
    role: str
    content: str
class Product(BaseModel):
    title: str
    imageURLHighRes: str
    category: str
    asin: str
    summary:str
class CartBotReq(BaseModel):
    products: List[Product]
    messages: List[Message]
class Req(BaseModel):
    image: str
    user_id: int
    message: str
class cartinsreq(BaseModel):
    userid: str
    product_id: str
class ReqFile(BaseModel):
    file: UploadFile

class ShowMoreReq(BaseModel):
    query: str
    category: str


# FastAPI models for input validation
class UserSignup(BaseModel):
    username: str
    password: str
    gender: str
    activities: List[str]


class UserLogin(BaseModel):
    username: str
    password: str
