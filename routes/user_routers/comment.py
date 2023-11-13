import datetime
import time
from bson.json_util import dumps, loads
import json
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import (
    collection_user,
    collection_product,
    collection_shopping_cart,
    collection_comment,
)
from models.order import comment_get, comment_put
from models.products import products_query_params, iteam, put_iteam
from function.ganerate_id import generate_id
from models.shopping_cart import shopping_cart_iteam_put, shopping_cart_iteam_edit
from schema.shop_products import list_products
from schema.shopping_cart import list_shopping_cart_iteam
from bson import json_util

order_comment_router = APIRouter()


# test
@order_comment_router.get("/")
def test():
    return {"message": "order_comment_router_test"}


# add some comment
@order_comment_router.put("/add")
async def add_or_update_comment(item: comment_put, request: Request):
    collection_comment.update_one(
        {
            "product_id": item.product_id,
            "product_option": None if item.product_option == "null" else item.product_option,
            "order_id": item.order_id,
        },
        {
            "$set": {
                "content": item.content,
                "rate": item.rate,
                "update_time": int(time.time()),
            }
        },
        upsert=True,
    )
    return JSONResponse(
        status_code=201, content={"message": "successful create or update comment"}
    )


# get comment
@order_comment_router.put("/get")
async def add_or_update_comment(get_query: comment_get, request: Request):
    data1 = json.loads(json_util.dumps(collection_comment.find_one(
        {
            "product_id": get_query.product_id,
            "product_option": None
            if get_query.product_option == "null"
            else get_query.product_option,
            "order_id": get_query.order_id,
        }
    )))
    print(data1)
    return JSONResponse(status_code=200, content={"data":data1,"message": "successful get the data"})
