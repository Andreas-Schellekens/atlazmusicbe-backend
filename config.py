import os
from dotenv import load_dotenv

load_dotenv()

db_connection = os.environ.get('DB_CONNECTION') or os.environ.get('DATABASE_URL')
docs_url = os.environ.get('DOCS_URL', None)

# keep raw string from env; use "*" to allow all origins
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")

# disable credentials completely for CORS (safer for public API)
allow_credentials = False