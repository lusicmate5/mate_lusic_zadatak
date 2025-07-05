from fastapi import FastAPI, HTTPException, Request, Depends
from typing import List, Optional

from src import auth
from src.auth import get_current_user
from src.services import get_tickets, get_ticket_by_id, get_stats
from src.models import Ticket

from src.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# 🧃 Rate limiting setup
def custom_key_func(request: Request):
    key = request.headers.get("X-Forwarded-For", request.client.host)
    print("🧩 Rate limit key used:", key)
    return key


app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

# ✅ Samo jedan include
app.include_router(auth.router)



# 🎫 GET /tickets
@app.get("/tickets", response_model=List[Ticket])
@limiter.limit("10/minute")
async def tickets_endpoint(
    request: Request,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    logger.info("Fetching tickets with filters: status=%s, priority=%s, query=%s", status, priority, q)
    return await get_tickets(status, priority, q, limit, offset)

# 🎫 GET /tickets/{id}
@app.get("/tickets/{ticket_id}")
async def ticket_detail(ticket_id: int):
    data = await get_ticket_by_id(ticket_id)
    if not data:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return data

# 📊 GET /stats
@app.get("/stats")
async def stats_endpoint():
    return await get_stats()

# ✅ Health check
@app.get("/health")
def health_check():
    logger.info("Health check accessed")
    return {"status": "ok"}
