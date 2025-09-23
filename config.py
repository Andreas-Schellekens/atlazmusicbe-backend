import os
from dotenv import load_dotenv

load_dotenv()

# support both names, prefer DB_CONNECTION, fall back to DATABASE_URL
db_connection = os.environ.get('DB_CONNECTION') or os.environ.get('DATABASE_URL')
docs_url = os.environ.get('DOCS_URL', None)
# provide empty string default so splitting is safe in main
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "")