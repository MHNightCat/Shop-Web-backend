from pydantic import BaseModel


class iteam(BaseModel):
    id: str
    name: str
    price: int
    describe: str
    category: str
    image: list
    remaining: int
    payment: int
    transport: bool
    sell: int
    updateAt: int


class put_iteam(BaseModel):
    name: str


class update_iteam(BaseModel):
    name: str
    price: int
    describe: str
    image: list
    remaining: int
    payment: int
    transport: int
    category: str


class products_query_params(BaseModel):
    limit: int


class category(BaseModel):
    id: str
    name: str


class category_put(BaseModel):
    name: str


class product_options(BaseModel):
    product_id: str
    name: str
    price: int
    image: str
    remaining: int


class product_update_options(BaseModel):
    name: str
    price: int
    image: str
    remaining: int


# 付款方式:
# 1=貨到付款 2=線上付款 3=不限

# 運送方式 1=可運送 2=不可運送(自取)
