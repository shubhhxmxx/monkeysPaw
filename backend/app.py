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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from .services.ai_service import generate_twisted_wish
from dotenv import load_dotenv
from .models.wish import WishRequest, WishResponse
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


@app.post("/wishes", response_model=WishResponse)
def add_wish(wish_request: WishRequest):
    global wish_id_counter

    # Check if the maximum number of wishes (3) has been reached
    load_dotenv()
    key = os.environ.get("GENAI_API_KEY")
    print(key)
    key = os.environ.get("GENAI_API_KEY")
    print(key)
    if len(wishes) >= 10000:
        raise HTTPException(
            status_code=400, detail="You have reached the maximum of 3 wishes."
        )

    # Generate a consequence string
    twist = generate_twisted_wish(wish_request.wish)

    consequence = f"Your wish '{wish_request.wish}' is granted... but with a twist. {twist}"

    # Create a new wish
    new_wish = WishResponse(
        id=wish_id_counter,
        wish=wish_request.wish,
        twist=consequence,
        timestamp=datetime.now(),
    )

    # Add the wish to the in-memory list
    wishes.append(new_wish)

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