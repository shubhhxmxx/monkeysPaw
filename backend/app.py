# Build a FastAPI backend for a Monkey’s Paw wishes game.
# Requirements:
# - Use FastAPI and Pydantic
# - Create a Wish model with fields: id (int), text (str), consequence (str), timestamp (datetime)
# - Maintain an in-memory list of wishes (no database needed for now)
# - API Endpoints:
#   1. POST /wishes -> Add a new wish (accept "text" as input, auto-generate consequence string)
#      * If there are already 3 wishes, return an HTTP 400 error with message: "You have reached the maximum of 3 wishes."
#   2. GET /wishes -> Return all current wishes
#   3. DELETE /wishes/{wish_id} -> Delete a wish by ID
# - Consequence should be a simple string like: "Your wish '<text>' is granted... but with a twist."
# - Increment wish IDs automatically
# - Store timestamp for each wish
# - Keep the code clean and ready for Angular frontend integration

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from .services.ai_service import generate_twisted_wish
from dotenv import load_dotenv
from .models.wish import WishRequest, WishResponse
from fastapi.responses import JSONResponse
import time
# Import necessary modules
# from fastapi import FastAPI, HTTPException
# In app.py (top)
import os, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

app = FastAPI()

# In-memory storage for wishes
wishes = []
wish_id_counter = 1  # Auto-incrementing ID counter
ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic model for a Wish
class Wish(BaseModel):
    id: int
    text: str
    consequence: str
    timestamp: datetime

RATE_WINDOW_SECONDS = 60
MAX_REQ_PER_IP = 20
DAILY_CAP = 500  # total twists/day
_request_buckets: dict[str, list[float]] = {}
_daily_usage = {"count": 0, "day": time.strftime("%Y-%m-%d")}
_twist_cache: dict[str, str] = {}
CACHE_TTL_SECONDS = 3600

def _clean_daily():
    today = time.strftime("%Y-%m-%d")
    if _daily_usage["day"] != today:
        _daily_usage["day"] = today
        _daily_usage["count"] = 0

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith("/wishes"):
        _clean_daily()
        if _daily_usage["count"] >= DAILY_CAP:
            return JSONResponse(status_code=429, content={"detail": "Daily cap reached"})
        ip = request.client.host or "unknown"
        now = time.time()
        bucket = _request_buckets.setdefault(ip, [])
        # drop old
        cutoff = now - RATE_WINDOW_SECONDS
        while bucket and bucket[0] < cutoff:
            bucket.pop(0)
        if len(bucket) >= MAX_REQ_PER_IP:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        bucket.append(now)
    return await call_next(request)

# Modify the wish creation logic to use cache
def _cached_twist(wish_text: str) -> str:
    now = time.time()
    entry = _twist_cache.get(wish_text.lower())
    if entry:
        twist, ts = entry
        if now - ts < CACHE_TTL_SECONDS:
            return twist
    twist = generate_twisted_wish(wish_text)
    _twist_cache[wish_text.lower()] = (twist, now)
    return twist

@app.post("/wishes", response_model=WishResponse)
def add_wish(wish_request: WishRequest):
    global wish_id_counter
    _clean_daily()
    # existing per-session (list length) check stays
    if len(wishes) >= 3:
        raise HTTPException(status_code=400, detail="You have reached the maximum of 3 wishes.")
    twist_text = _cached_twist(wish_request.wish)
    _daily_usage["count"] += 1
    consequence = f"Your wish '{wish_request.wish}' is granted... but with a twist. {twist_text}"
    new_wish = WishResponse(
        id=wish_id_counter,
        wish=wish_request.wish,
        twist=consequence,
        timestamp=datetime.utcnow(),
    )
    wishes.append(new_wish)
    wish_id_counter += 1
    return new_wish

@app.post("/wishes/reset" ,response_model=dict) 
def reset_wishes():
    global wishes, wish_id_counter
    wishes = []
    wish_id_counter = 1
    return {"message": "Wishes have been reset."}

@app.get("/wishes", response_model=List[Wish])
def get_wishes():
    return wishes


@app.delete("/wishes/{wish_id}", response_model=Wish)
def delete_wish(wish_id: int):
    global wishes

    # Find the wish by ID
    for wish in wishes:
        if wish.id == wish_id:
            wishes.remove(wish)
            return wish

    # If the wish is not found, raise an error
    raise HTTPException(status_code=404, detail="Wish not found.")

@app.get("/limits")
def limits():
    _clean_daily()
    return {
        "per_ip_per_minute": MAX_REQ_PER_IP,
        "daily_remaining": max(0, DAILY_CAP - _daily_usage["count"]),
        "session_remaining": max(0, 3 - len(wishes)),
    }