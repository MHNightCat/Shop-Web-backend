import os
from fastapi import FastAPI, HTTPException, Request
from routes.route import router
from routes.auth import auth_router
from routes.admin import admin_router
from routes.user import user_router
from routes.shop import shop_router
from starlette.middleware.sessions import SessionMiddleware
from pymongo import MongoClient
import os
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000",
    "https://my-computer.nightcat.xyz",
    "https://pccuhort.com/",
]

api_router = FastAPI()     

# get env sercet
mongodb_secret = os.getenv("MONGODB_SERCET")
SECRET_KEY = os.getenv("SECRET_KEY")

client = MongoClient(mongodb_secret)

# middleware
api_router.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=43200)
api_router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router.include_router(router, tags=["index"])
api_router.include_router(auth_router, prefix="/oauth", tags=["oauth"])
api_router.include_router(shop_router, prefix="/shop", tags=["shop"])
api_router.mount("/admin", admin_router)
api_router.mount("/user", user_router)
