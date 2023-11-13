from fastapi import FastAPI
from api import api_router

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000",
    "https://my-computer.nightcat.xyz",
    "https://shop-web.nightcat.xyz/",
    "https://shop-web-api.nightcat.xyz/"
]

app = FastAPI()  # docs_url=None, redoc_url=None)

app.mount("/api", api_router)

@app.get("/")
def test():
    return {"message": "shop web api"}


# if __name__ == '__main__':
#     uvicorn.run(
#         "main:app",
#         host='127.0.0.1',
#         port=8000,
#         reload=True
#     )
