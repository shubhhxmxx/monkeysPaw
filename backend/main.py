# filepath: /C:/Users/Shubham Semwal/git/monkeyspaw/monkeyspaw/backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.wish import WishRequest, WishResponse
from .services.ai_service import generate_twisted_wish

app = FastAPI()

ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:5173",
]
# Add once during debugging
@app.middleware("http")
async def debug_req(request, call_next):
    print(f"{request.method} {request.url.path} Origin={request.headers.get('origin')} ACRM={request.headers.get('access-control-request-method')}")
    return await call_next(request)
# Middleware to handle CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/wish", response_model=WishResponse)
async def create_wish(wish_request: WishRequest):
    try:
        twisted_wish = generate_twisted_wish(wish_request.wish)
        return WishResponse(wish=wish_request.wish, twisted=twisted_wish)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing wish: {e}")