import json
import time
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from config.database import collection_user, collection_product, collection_user
from models.products import iteam, put_iteam
from function.ganerate_id import generate_id
from .products.category import category_router
from .products.products import products_router
from bson.json_util import dumps, loads

admin_router = FastAPI()
admin_router.include_router(products_router, prefix="/products", tags=["products"])
admin_router.include_router(category_router, prefix="/category", tags=["category"])


# authorized function
async def authentication_middleware(request: Request, call_next):
    user = request.session.get("user")
    if not user:
        response = JSONResponse(content={"detail": "Unauthorized"}, status_code=401)
        return response
    user_data = collection_user.find_one({"sub": user["sub"]})
    if not user_data["admin"]:
        response = JSONResponse(content={"detail": "Unauthorized"}, status_code=401)
        return response
    response = await call_next(request)
    return response


# auth middleware
admin_router.middleware("http")(authentication_middleware)


# test
@admin_router.get("/")
def test():
    return {"message": "admin_test"}


@admin_router.get("/adminlist")
async def Get_Admin_List():
    admin_data_ = collection_user.find({"admin": True})
    admin_data_list = list(admin_data_)
    admin_data = json.loads(dumps(admin_data_list))
    return {"message": "successful create", "data": admin_data}


@admin_router.put("/addadmin/{email}")
async def add_admin(email: str):
    update_data = collection_user.update_one(
        {"email": email},
        {
            "$set": {
                "admin": True,
            }
        },
    )
    if update_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=201, content={"message": "successful update iteam"})

@admin_router.delete("/deleteadmin/{sub}")
async def delete_admin(sub: str):
    update_data = collection_user.update_one(
        {"sub": sub},
        {
            "$set": {
                "admin": False,
            }
        },
    )
    if update_data.raw_result["n"] == 0:
        raise HTTPException(status_code=400, detail="can't find this data")
    return JSONResponse(status_code=201, content={"message": "successful update iteam"})
