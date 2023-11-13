import datetime
import json
import time
from fastapi import APIRouter, HTTPException, status
import os
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, Response
from starlette.config import Config
from dotenv import load_dotenv
from config.database import collection_user, db
import jwt
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse, RedirectResponse

load_dotenv()

auth_router = APIRouter()

# get env secret
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
redirect_uri = os.getenv("redirect_uri")
SECRET_KEY = os.getenv("SECRET_KEY")

# set up authlib
config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# google login
@auth_router.get("/login/google")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri)


# google callback
@auth_router.get("/auth/google")
async def auth(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "This not a successful google login"},
        )
    User_data = list(collection_user.find({"sub": user.sub}))
    if len(User_data) == 0:
        collection_user.insert_one(
            {
                "sub": user.sub,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "admin": False,
                "createat": int(time.time()),
            }
        )
    else:
        collection_user.update_one(
            {"sub": user.sub},
            {
                "$set": {
                    "email": user.email,
                    "name": user.name,
                    "picture": user.picture,
                }
            },
        )
    json = {"sub": user.sub, "avatar": user.picture}
    request.session["user"] = dict(json)
    return RedirectResponse(url=os.getenv("WEB_URL"))


# log out
@auth_router.get("/logout")
async def logout(request: Request, response: Response):
    request.session.pop("user", None)
    response.delete_cookie("session")
    redirect_response = RedirectResponse(url=os.getenv("WEB_URL"))
    return response, redirect_response


# successful
@auth_router.get("/")
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        data = json.dumps(user)
        html = f"<pre>{data}</pre>" '<a href="/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@auth_router.get("/checkpressioms")
async def homepage(request: Request):
    user = request.session.get("user")
    if not user:
        response = JSONResponse({"sub": None, "avatar": None, "admin": None})
        return response
    user_data = collection_user.find_one({"sub": user["sub"]})
    return JSONResponse(
        {"sub": user["sub"], "avatar": user["avatar"], "admin": user_data["admin"]}
    )
