from pydantic import BaseModel


class shopping_cart_iteam(BaseModel):
    id: str
    sub: str
    iteam_id: str
    amount: int


class shopping_cart_iteam_put(BaseModel):
    product_id: str
    product_option: str or None


class shopping_cart_iteam_edit(BaseModel):
    id: str
    amount: int
