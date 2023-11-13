from pydantic import BaseModel


class orders(BaseModel):
    id: str
    sub: str
    totalprice: int
    phonenumber: str
    payment: str
    product: list
    status: int
    transport: int
    address: str
    remaker: str
    admin: int
    time: int
    createAt: int

class orders_put(BaseModel):
    totalprice: int
    phonenumber: str
    product: list
    transport: str
    payment: str
    address: str
    remaker: str
    admin: bool
    time: int
    
class comment_put(BaseModel):
    product_id: str
    product_option: str
    order_id: str
    content: str
    rate: int

class comment_get(BaseModel):
    product_id: str
    product_option: str or None
    order_id: str
#admin True = 現場購買 False=線上商城

#transport 1=自取 2=配送

#payment 1 = 現場付款 2 = 線上付款

#status 0 = 訂單取消申請 1 = 訂單成立 2 = 已經付款 3 = 尚未付款 4 = 尚未付款，且付款已過期 5 = 訂單取消 6 = 訂單完成

