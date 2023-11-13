import os
import time
import json
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import (
    collection_user,
    collecton_product_options,
    collecton_order,
    collection_product,
    collection_shopping_cart,
)
from function.send_email import send_email
from models.order import orders_put
from models.products import products_query_params, iteam, put_iteam
from function.ganerate_id import generate_id
from schema.shop_products import list_products
import importlib.util
from bson.json_util import dumps, loads

order_router = APIRouter()


# test
@order_router.get("/")
def test():
    return {"message": "order_test"}


@order_router.put("/create")
async def Create_Order(order: orders_put, request: Request):
    print(order)
    Id = generate_id()
    EcPayData = None
    if order.payment == "2":
        EcPayData = EcPayCreateOrder(Id, order)
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    collection_shopping_cart.delete_many({"sub": user["sub"]})
    collecton_order.insert_one(
        {
            "id": Id,
            "sub": user["sub"],
            "MacValue": EcPayData["MacValue"] if EcPayData else None,
            "totalprice": order.totalprice,
            "phonenumber": order.phonenumber,
            "product": order.product,
            "payment": order.payment,
            "status": "6" if order.admin else "3",
            "transport": order.transport,
            "address": order.address,
            "remaker": order.remaker,
            "admin": order.admin,
            "time": order.time,
            "html": EcPayData["html"] if EcPayData else None,
            "createAt": int(time.time()),
        }
    )
    text = f"""
    <html>
    <head></head>
    <body>
    <p><span style="color:#000;"><strong>你的購買已經通過</strong></span></p>
    <p><span style="color:#000;"><strong>訂單編號:{Id}</strong></span></p>
    <p><span style="color:#000;"><strong>總價格:{order.totalprice}</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist/{Id}"><span style="color:#000;"><strong>你可以在這裡找到有關這個訂的詳細訊息</strong></span></a><br>&nbsp;</p>
    <p><span class="text-big" style="color:#000;"><strong>請注意! 取貨時請開啟這個訂單的QRCODE給工作人員核對!</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist"><span style="color:#000;"><strong>點我前往QRCODE</strong></span></a></p></body></html>
    <p><span class="text-big" style="color:#000;"><strong>※注意!請於取貨/運送前3小時進行付款，否則訂單將視為不成立!</strong></span></p>
    """
    send_email(f"園氏物語 | 購買通知書 | 訂單編號:{Id}", user_data["email"], text)
    print(order.product)
    for x in order.product:
        print(x)
        if x["product_options"]:
            print("test")
            print({"product_id": x["product_id"], "name": x["product_options"]})
            test_01 = collecton_product_options.update_one(
                {"product_id": x["product_id"], "name": x["product_options"]},
                {
                    "$inc": {
                        "remaining": -x["amount"],
                    }
                }, 
            )
            print(test_01.raw_result)
            collection_product.update_one(
                {"id": x["product_id"]},
                {
                    "$inc": {
                        "sell": x["amount"],
                    }
                },
            )
        else:
            print("aaaaaaaa")
            collection_product.update_one(
                {"id": x["product_id"]},
                {
                    "$inc": {
                        "remaining": -x["amount"],
                        "sell": x["amount"],
                    }
                },
            )
    return JSONResponse(
        status_code=201, content={"message": "successful create Order", "id": Id}
    )


@order_router.get("/getlist")
async def get_List(request: Request):
    user = request.session.get("user")
    data = json.loads(dumps(list(collecton_order.find({"sub": user["sub"]}))))
    return JSONResponse(
        status_code=201, content={"message": "successful find order list", "data": data}
    )


@order_router.get("/allorder")
async def get_order(request: Request):
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    if not user_data["admin"]:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    data = json.loads(dumps(list(collecton_order.find())))
    return JSONResponse(status_code=200, content={"data": data})


@order_router.get("/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    data = json.loads(dumps(collecton_order.find_one({"id": id})))
    if not user_data["admin"] and user["sub"] != data["sub"]:
        return JSONResponse(
            status_code=401, content={"message": "Unauthorized", "data": data}
        )
    return JSONResponse(
        status_code=201, content={"message": "successful find order list", "data": data}
    )


@order_router.get("/pay/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    data = json.loads(dumps(collecton_order.find_one({"sub": user["sub"], "id": id})))
    return HTMLResponse(
        status_code=201,
        content=data["html"],
    )


@order_router.put("/accomplish/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    if not user_data["admin"]:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    data = collecton_order.update_one(
        {"id": id},
        {
            "$set": {
                "status": "6",
            }
        },
    )

    return JSONResponse(
        status_code=201, content={"message": "successful update status"}
    )


@order_router.put("/cancelrequest/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    data = collecton_order.update_one(
        {"sub": user["sub"], "id": id},
        {
            "$set": {
                "status": "0",
            }
        },
    )
    return JSONResponse(
        status_code=201,
        content={"message": "successful request cancel order"},
    )


@order_router.put("/agreecancel/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    if not user_data["admin"]:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    data = collecton_order.update_one(
        {"id": id},
        {
            "$set": {
                "status": "5",
            }
        },
    )
    order_data = collecton_order.find_one({"id": id})
    text = f"""
    <html>
    <head></head>
    <body>
    <p><span style="color:#000;"><strong>你的訂單取消申請已經通過</strong></span></p>
    <p><span style="color:#000;"><strong>訂單編號:{id}</strong></span></p>
    <p><span style="color:#000;"><strong>總價格:{order_data["totalprice"]}</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist/{id}"><span style="color:#000;"><strong>你可以在這裡找到有關這個訂的詳細訊息</strong></span></a><br>&nbsp;</p>
    """
    send_email(f"園氏物語 | 訂單取消通知 | 訂單編號:{id}", user_data["email"], text)
    return JSONResponse(
        status_code=201, content={"message": "successful update status"}
    )


@order_router.put("/expired/{id}")
async def get_order(request: Request, id: str):
    user = request.session.get("user")
    user_data = collection_user.find_one({"sub": user["sub"]})
    if not user_data["admin"]:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    data = collecton_order.update_one(
        {"id": id},
        {
            "$set": {
                "status": "4",
            }
        },
    )
    order_data = collecton_order.find_one({"id": id})
    text = f"""
    <html>
    <head></head>
    <body>
    <p><span style="color:#000;"><strong>你的訂單已經被標注為期限內為繳費</strong></span></p>
    <p><span style="color:#000;"><strong>訂單編號:{id}</strong></span></p>
    <p><span style="color:#000;"><strong>總價格:{order_data["totalprice"]}</strong></span></p>
    <p><a href="{os.getenv("WEB_URL")}user/orderlist/{id}"><span style="color:#000;"><strong>你可以在這裡找到有關這個訂的詳細訊息</strong></span></a><br>&nbsp;</p>
    """
    send_email(f"園氏物語 | 訂單期限內未繳費 | 訂單編號:{id}", user_data["email"], text)
    return JSONResponse(
        status_code=200, content={"message": "successful update status"}
    )


def EcPayCreateOrder(Id: str, order: orders_put):
    spec = importlib.util.spec_from_file_location(
        "ecpay_payment_sdk", "./sdk/ecpay_payment_sdk.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    from datetime import datetime

    names = [item["name"] for item in order.product]

    result = "#".join(names)

    order_params = {
        "MerchantTradeNo": Id,
        "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": order.totalprice,
        "TradeDesc": f"中國文化大學 園藝系商店 | 訂單編號:{Id}",
        "ItemName": result,
        "ReturnURL": os.getenv("WEB_URL") + "api/shop/ecpay/return/result",
        "ChoosePayment": "ALL",
        "ClientBackURL": f'{os.getenv("WEB_URL")}user/orderlist/{Id}',
        "Remark": "有部分商品可能會因為長度過長而被截取，為正常現象，請確保金額正常即可!",  # 要改
        "NeedExtraPaidInfo": "Y",
        "EncryptType": 1,
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID=os.getenv("MerchantID"),
        HashKey=os.getenv("HashKey"),
        HashIV=os.getenv("HashIV"),
    )

    # 合併延伸參數
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
        # 產生 html 的 form 格式
        action_url = os.getenv("action_url")  # 測試環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        return {"html": html, "MacValue": final_order_params["CheckMacValue"]}
    except Exception as error:
        print("An exception happened: " + str(error))
