import json
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from models.order import comment_get
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import (
    collection_user,
    collection_product,
    collection_category,
    collecton_product_options,
    collecton_order,
    collection_comment,
)
from function.send_email import send_email
from models.products import products_query_params, iteam, put_iteam
from function.ganerate_id import generate_id
from schema.shop_products import list_products
from bson.json_util import dumps, loads
from bson import json_util

load_dotenv()

shop_router = APIRouter()


# test
@shop_router.get("/")
def test():
    return {"message": "shop_test"}


@shop_router.get("/products")
async def get_products(limit: int = 10):
    if limit > 50:
        raise HTTPException(
            status_code=400, detail="You only can get 50 products in one time"
        )
    data_list = json.loads(
        dumps(list(collection_product.find().sort("sell", -1).limit(limit)))
    )
    return JSONResponse(
        status_code=201,
        content={"message": "successful find products", "data": data_list},
    )


@shop_router.get("/category")
async def cetegory():
    cetegory_data_ = collection_category.find()
    cetegory_data_list = list(cetegory_data_)
    cetegory_data = json.loads(dumps(cetegory_data_list))
    return {"message": "successful create", "data": cetegory_data}


@shop_router.get("/products/{id}")
async def get_products(id: str):
    data = json.loads(dumps(collection_product.find_one({"id": id})))
    return JSONResponse(
        status_code=201, content={"message": "successful find products", "data": data}
    )


@shop_router.get("/products-options/{id}")
async def get_products_options(id: str):
    data = json.loads(dumps(list(collecton_product_options.find({"product_id": id}))))
    return JSONResponse(
        status_code=201,
        content={"message": "successful find products options", "data": data},
    )


@shop_router.get("/pupular/products")
async def get_products_options():
    data = json.loads(dumps(list(collection_product.find().sort("sell", -1).limit(4))))
    return JSONResponse(
        status_code=200,
        content={"message": "successful find products options", "data": data},
    )


# get comment
@shop_router.get("/rate/{id}")
async def add_or_update_comment(id: str, request: Request):
    data = json.loads(json_util.dumps(collection_comment.aggregate(
        [
            {"$match": {"product_id": id}},
            {"$group": {"_id": None, "averageValue": {"$avg": "$rate"}}},
        ]
    )))
    print(data)
    return JSONResponse(status_code=200, content={"data":data})


@shop_router.post("/ecpay/return/result")
async def get_products_options(request: Request):
    form_data = await request.form()
    if not form_data:
        return "2|FAILE"
    result = form_data["CheckMacValue"]
    OrderId = form_data["MerchantTradeNo"]
    order_data = collecton_order.find_one({"id": OrderId})
    if order_data["admin"]:
        return "2|FAILE"
    data = collecton_order.update_one(
        {"id": OrderId},
        {
            "$set": {
                "status": "6",
            }
        },
    )
    text = f"""
    <html>
    <head></head>
    <body>
    <p><span style="color:#000;"><strong>你的訂單已經成功進行付款!</strong></span></p>
    <p><span style="color:#000;"><strong>訂單編號:{OrderId}</strong></span></p>
    <p><span style="color:#000;"><strong>總價格:{order_data["totalprice"]}</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist/{OrderId}"><span style="color:#000;"><strong>你可以在這裡找到有關這個訂的詳細訊息</strong></span></a><br>&nbsp;</p>
    <p><span class="text-big" style="color:#000;"><strong>請注意! 取貨時請開啟這個訂單的QRCODE給工作人員核對!</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist"><span style="color:#000;"><strong>點我前往QRCODE</strong></span></a></p></body></html>
    """
    user_data = collection_user.find_one({"sub": order_data["sub"]})
    send_email(f"園氏物語 | 訂單成功付款通知 | 訂單編號:{OrderId}", user_data["email"], text)
    return "1|OK"
