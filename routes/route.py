from fastapi import APIRouter

router = APIRouter()

# GET Req Method


@router.get("/")
def test():
    return {"message": "api_app"}
