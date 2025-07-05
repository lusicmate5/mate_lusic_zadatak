import httpx
import hashlib
import json
from typing import List, Optional
from .models import Ticket
from .redis_service import RedisService
import logging

logger = logging.getLogger(__name__)

redis = RedisService()

def calculate_priority(ticket_id: int) -> str:
    priorities = ["low", "medium", "high"]
    return priorities[ticket_id % 3]

def make_cache_key(base: str, params: dict) -> str:
    raw = f"{base}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(raw.encode()).hexdigest()

async def get_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[Ticket]:
    params = {
        "status": status,
        "priority": priority,
        "query": query,
        "limit": limit,
        "offset": offset
    }
    logger.info(
        "get_tickets called with status=%s, priority=%s, query=%s, limit=%d, offset=%d",
        status, priority, query, limit, offset
    )

    cache_key = make_cache_key("tickets", params)

    cached = redis.get(cache_key)
    if cached:
        print("✅ FROM CACHE (get_tickets)")
        return [Ticket(**item) for item in cached]

    async with httpx.AsyncClient() as client:
        todos_response = await client.get("https://dummyjson.com/todos")
        users_response = await client.get("https://dummyjson.com/users")

    todos = todos_response.json()["todos"]
    users = users_response.json()["users"]
    user_map = {user["id"]: user["username"] for user in users}

    tickets = [
        Ticket(
            id=todo["id"],
            title=todo["todo"],
            status="closed" if todo["completed"] else "open",
            priority=calculate_priority(todo["id"]),
            assignee=user_map.get(todo["userId"], "unknown")
        )
        for todo in todos
    ]

    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    if query:
        tickets = [t for t in tickets if query.lower() in t.title.lower()]

    result = tickets[offset:offset + limit]
    redis.set(cache_key, [t.model_dump() for t in result], expire_seconds=60)
    print("🆕 FROM DB (get_tickets)")
    return result


async def get_ticket_by_id(ticket_id: int) -> dict:
    logger.info("Fetching ticket ID %d", ticket_id)

    cache_key = f"ticket:{ticket_id}"

    # ✅ Pokušaj iz cachea
    cached = redis.get(cache_key)
    if cached:
        print("✅ FROM CACHE (get_ticket_by_id)")
        return cached

    # 🌍 Dohvati podatke
    async with httpx.AsyncClient() as client:
        todo_resp = await client.get(f"https://dummyjson.com/todos/{ticket_id}")
        if todo_resp.status_code != 200:
            return None

        todo = todo_resp.json()
        user_resp = await client.get(f"https://dummyjson.com/users/{todo['userId']}")
        user = user_resp.json() if user_resp.status_code == 200 else {}

    ticket = Ticket(
        id=todo["id"],
        title=todo["todo"],
        status="closed" if todo["completed"] else "open",
        priority=calculate_priority(todo["id"]),
        assignee=user.get("username", "unknown")
    )

    result = {
        "ticket": ticket.model_dump(),
        "raw": {
            "todo": todo,
            "user": user
        }
    }

    # 💾 Spremi u cache
    redis.set(cache_key, result, expire_seconds=60)
    print("🆕 FROM DB (get_ticket_by_id)")
    return result

from collections import Counter

async def get_stats():
    logger.info("Generating ticket statistics")

    cache_key = "ticket_stats"
    cached = redis.get(cache_key)
    if cached:
        print("✅ FROM CACHE (stats)")
        return cached

    tickets = await get_tickets(limit=1000, offset=0)  # pretpostavka: max 1000 ticketa

    total = len(tickets)
    open_count = len([t for t in tickets if t.status == "open"])
    closed_count = total - open_count

    priority_counts = Counter([t.priority for t in tickets])
    top_users = Counter([t.assignee for t in tickets]).most_common(5)

    stats = {
        "total": total,
        "open": open_count,
        "closed": closed_count,
        "priority_counts": priority_counts,
        "top_users": [
            {"username": user, "tickets": count} for user, count in top_users
        ]
    }

    redis.set(cache_key, stats, expire_seconds=60)
    print("🆕 FROM DB (stats)")
    return stats
