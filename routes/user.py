from fastapi.responses import JSONResponse
from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
from config.database import collection_user, collection_product
from .user_routers.order import order_router
from .user_routers.cart import shopping_cart_router
from .user_routers.comment import order_comment_router

user_router = FastAPI()

# GET Req Method
user_router.include_router(order_router, prefix="/order", tags=["order"])
user_router.include_router(
    shopping_cart_router, prefix="/cart", tags=["cart"]
)
user_router.include_router(order_comment_router, prefix="/comment", tags=["comment"])

# authorized function
async def authentication_middleware(request: Request, call_next):
    user = request.session.get("user")
    if not user:
        response = JSONResponse(content={"detail": "Unauthorized"}, status_code=401)
        return response  # 返回响应而不引发异常
    response = await call_next(request)
    return response


# auth middleware
user_router.middleware("http")(authentication_middleware)


# test
@user_router.get("/")
def test():
    return {"message": "user_test"}
