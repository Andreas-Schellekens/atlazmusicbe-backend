from fastapi import FastAPI
from routes import events
from fastapi.middleware.cors import CORSMiddleware
import config

app = FastAPI(docs_url=config.docs_url)

# safe split: produce empty list if allowed_origins is empty
origins = [o.strip() for o in (config.allowed_origins or "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],  # fallback to allow all if none specified
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(events.router, prefix="/events")

