import os
from dotenv import load_dotenv

load_dotenv()

# DB connection: prefer DB_CONNECTION then DATABASE_URL
db_connection = os.environ.get('DB_CONNECTION') or os.environ.get('DATABASE_URL')
docs_url = os.environ.get('DOCS_URL', None)

# default allowed origins (common local dev ports + production site)
_default_allowed = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173,https://atlazmusic.be"

# read from env (ALLOWED_ORIGINS or ALLOWED_HOSTS) or fall back to defaults
_env_allowed = os.environ.get("ALLOWED_ORIGINS") or os.environ.get("ALLOWED_HOSTS")
allowed_origins = _env_allowed if _env_allowed is not None else _default_allowed

# If running on Vercel they expose VERCEL_URL (e.g. my-project-git-main-username.vercel.app)
# add https://{VERCEL_URL} to allowed_origins so preview deployments work.
vercel_url = os.environ.get("VERCEL_URL")
if vercel_url:
    vercel_origin = f"https://{vercel_url}"
    if vercel_origin not in [o.strip() for o in allowed_origins.split(",")]:
        allowed_origins = (allowed_origins + "," + vercel_origin) if allowed_origins else vercel_origin

# disable credentials completely for CORS (safer for public API)
allow_credentials = False