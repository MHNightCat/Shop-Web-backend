import time
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import collection_user, collection_product, collection_category
from models.products import (
    category_put,
    products_query_params,
    iteam,
    put_iteam,
    product_options,
)
from function.ganerate_id import generate_id
from bson.json_util import dumps, loads


category_router = APIRouter()


# test
@category_router.get("/")
def test():
    return {"message": "category_test"}


# create category
@category_router.put("/craete")
async def cetegory_create(category: category_put):
    collection_category.insert_one({"id": generate_id(), "name": category.name})
    return {"message": "successful create"}


# find category
@category_router.delete("/delete/{id}")
async def cetegory_delete(id: str):
    delete_data = collection_category.delete_one({"id": id})
    if delete_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=200, content={"message": "successful delete iteam"})


# update category
@category_router.put("/update/{id}")
async def cetegory_update(id: str, category: category_put):
    update_data = collection_category.update_one(
        {"id": id},
        {
            "$set": {
                "name": category.name,
            }
        },
    )
    if update_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=201, content={"message": "successful update iteam"})
