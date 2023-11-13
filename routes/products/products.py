import time
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import (
    collection_user,
    collection_product,
    collecton_product_options,
)
from models.products import (
    products_query_params,
    iteam,
    put_iteam,
    product_options,
    product_update_options,
    update_iteam,
)
from function.ganerate_id import generate_id
from bson.json_util import dumps, loads

products_router = APIRouter()

# test
@products_router.get("/")
def test():
    return {"message": "products_test"}


# create iteam
@products_router.put("/create")
async def add_iteam(iteam: put_iteam):
    products_id = generate_id()
    collection_product.insert_one(
        {
            "id": products_id,
            "name": iteam.name,
            "price": 0,
            "describe": '<h1><span style="color: #fd7e14">簡單的範例</span></h1><p><strong><span style="color: #82c91e">這只是一個測試</span></strong></p>',
            "category": None,
            "image": [],
            "remaining": 0,
            "payment": 3,
            "transport": 1,
            "sell": 0,
            "updateAt": int(time.time()),
        }
    )
    return JSONResponse(status_code=201, content={"message": "successful create iteam"})


# create iteam
@products_router.put("/product-options")
async def add_product_options(iteam: product_options):
    collecton_product_options.insert_one(
        {
            "id": generate_id(),
            "product_id": iteam.product_id,
            "name": iteam.name if iteam.name else "",
            "price": iteam.price if iteam.price else 0,
            "image": iteam.image if iteam.image else None,
            "remaining": iteam.remaining if iteam.remaining else 0,
        }
    )
    return JSONResponse(
        status_code=201, content={"message": "successful create product options"}
    )


# delete iteam
@products_router.delete("/delete/{id}")
async def delete_iteam(id: str):
    delete_data = collection_product.delete_one({"id": id})
    collecton_product_options.delete_many({"product_id": id})
    if delete_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=200, content={"message": "successful delete iteam"})


# delete products options


@products_router.delete("/delete-options/{id}")
async def delete_iteam(id: str):
    collecton_product_options.delete_one({"id": id})
    return JSONResponse(
        status_code=200, content={"message": "successful delete options"}
    )


# update products options


@products_router.put("/update-options/{id}")
async def delete_iteam(id: str, iteam: product_update_options):
    collecton_product_options.update_one(
        {"id": id},
        {
            "$set": {
                "name": iteam.name if iteam.name else "",
                "price": iteam.price if iteam.price else 0,
                "image": iteam.image if iteam.image else None,
                "remaining": iteam.remaining if iteam.remaining else 0,
            }
        },
    )
    return JSONResponse(
        status_code=200, content={"message": "successful update options"}
    )


# update iteam


@products_router.put("/update/{id}")
async def update_iteam(iteam: update_iteam, id: str):
    if len(iteam.describe) > 20000:
        raise HTTPException(
            status_code=400, detail="describe too many words(must be less than 20000)"
        )
    if iteam.price > 1000000:
        raise HTTPException(status_code=400, detail="price must be less than 999999")
    if iteam.remaining > 100000:
        raise HTTPException(
            status_code=400, detail="remaining must be less than 100000"
        )
    if iteam.payment not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Payment must be 1 or 2 or 3")
    update_data = collection_product.update_one(
        {"id": id},
        {
            "$set": {
                "name": iteam.name,
                "price": iteam.price,
                "describe": iteam.describe,
                "category": iteam.category,
                "image": iteam.image,
                "remaining": iteam.remaining,
                "payment": iteam.payment,
                "updateAt": int(time.time()),
                "transport": iteam.transport,
            }
        },
    )
    if update_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=201, content={"message": "successful create iteam"})
