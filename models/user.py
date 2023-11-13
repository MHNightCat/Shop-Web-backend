from pydantic import BaseModel


class User(BaseModel):
    sub: str
    email: str
    name: str
    picture: str
    createat: int
