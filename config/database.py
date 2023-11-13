from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongodb_secret = os.getenv("MONGODB_SECRET")

client = MongoClient(mongodb_secret)

db = client.shopping_website_database

collection_user = db["user"]
collection_product = db["product"]
collection_shopping_cart = db["shopping_cart"]
collection_category = db["category"]
collecton_product_options = db["product_options"]
collecton_order = db["order"]
collection_comment = db["comment"]