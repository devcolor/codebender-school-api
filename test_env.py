import os
from dotenv import load_dotenv

load_dotenv()

print("Environment variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
