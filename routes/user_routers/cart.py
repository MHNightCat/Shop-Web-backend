from bson.json_util import dumps, loads
import json
from fastapi.responses import JSONResponse
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from typing import List, Optional, Type
from config.database import (
    collection_user,
    collection_product,
    collection_shopping_cart,
    collecton_product_options,
)
from models.products import products_query_params, iteam, put_iteam
from function.ganerate_id import generate_id
from models.shopping_cart import shopping_cart_iteam_put, shopping_cart_iteam_edit
from schema.shop_products import list_products
from schema.shopping_cart import list_shopping_cart_iteam

shopping_cart_router = APIRouter()


# test
@shopping_cart_router.get("/")
def test():
    return {"message": "shopping_cart_test"}


# add iteam from shopping cart
@shopping_cart_router.put("/add")
async def add_shopping_cart_ieam(iteam: shopping_cart_iteam_put, request: Request):
    user = request.session.get("user")
    iteam_data = json.loads(
        dumps(
            collection_shopping_cart.find(
                {
                    "sub": user["sub"],
                    "product_id": iteam.product_id,
                    "product_option": iteam.product_option
                }
            )
        )
    )
    if len(iteam_data) == 0:
        collection_shopping_cart.insert_one(
            {
                "id": generate_id(),
                "sub": user["sub"],
                "product_id": iteam.product_id,
                "product_option": iteam.product_option,
                "amount": 1,
            }
        )
    else:
        collection_shopping_cart.update_one(
            {
                "sub": user["sub"],
                "product_id": iteam.product_id,
                "product_option": iteam.product_option,
            },
            {
                "$set": {
                    "amount": iteam_data[0]["amount"] + 1,
                }
            },
        )
    return JSONResponse(
        status_code=201, content={"message": "successful create or add products"}
    )


# edit iteam amount from shopping cart
@shopping_cart_router.put("/editamount")
async def edit_shopping_cart_amount(request: Request, iteam: shopping_cart_iteam_edit):
    user = request.session.get("user")
    iteam_data = collection_shopping_cart.find_one({"sub": user["sub"], "id": iteam.id})
    if iteam_data is None:
        raise HTTPException(status_code=400, detail="can't find this data")
    else:
        collection_shopping_cart.update_one(
            {"sub": user["sub"], "id": iteam.id},
            {
                "$set": {
                    "amount": iteam.amount,
                }
            },
        )
    return JSONResponse(status_code=200, content={"message": "successful add amount"})


# delete iteam from shopping cart
@shopping_cart_router.delete("/delete/{id}")
async def delete_shopping_cart_iteam(request: Request, id: str = None):
    user = request.session.get("user")
    iteam_data = collection_shopping_cart.delete_one({"sub": user["sub"], "id": id})
    if iteam_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=200, content={"message": "successful delete"})


# get iteams from shopping cart
@shopping_cart_router.get("/cartlist")
async def get_shopping_cart_items(request: Request):
    user = request.session.get("user")
    data_list = list(collection_shopping_cart.find({"sub": user["sub"]}))

    send_data = []
    product_ids = set()
    product_option_ids = set()

    for data in data_list:
        product_ids.add(data["product_id"])
        product_option_ids.add(data["product_option"])

    products = {
        product["id"]: product
        for product in collection_product.find({"id": {"$in": list(product_ids)}})
    }
    product_options = {
        option["id"]: option
        for option in collecton_product_options.find(
            {"id": {"$in": list(product_option_ids)}}
        )
    }

    for data in data_list:
        product_data = products.get(data["product_id"], {})
        product_options_data = product_options.get(data["product_option"], {})
        product_options_data_json = {
            "id": data["id"],
            "name": product_data.get("name", ""),
            "product_id": data["product_id"],
            "product_image": product_options_data.get(
                "image", product_data.get("image", [""])[0]
            ),
            "product_options": product_options_data.get("name"),
            "price": product_options_data.get("price", product_data.get("price")),
            "remaining": product_options_data.get(
                "remaining", product_data.get("remaining")
            ),
            "amount": data.get("amount"),
        }
        send_data.append(product_options_data_json)

    return JSONResponse(
        status_code=200,
        content={"message": "successful find products", "data": send_data, "delete": 1},
    )
