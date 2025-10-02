from fastapi import FastAPI
from routes import events
from fastapi.middleware.cors import CORSMiddleware
import config

app = FastAPI(docs_url=config.docs_url)

# interpret allowed_origins config (string -> list)
raw = config.allowed_origins or ""
origins = [o.strip() for o in raw.split(",") if o.strip()]

# if the env string was a single "*", keep ["*"]
if raw.strip() == "*":
    origins = ["*"]

# enforce no credentials for wildcard or by config
allow_credentials = bool(config.allow_credentials)
if origins == ["*"] and allow_credentials:
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(events.router, prefix="/events")

