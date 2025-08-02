import os
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ecommerce_user:password123@localhost:5432/ecommerce"
)
