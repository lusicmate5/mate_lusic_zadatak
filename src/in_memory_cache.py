# src/in_memory_cache.py

import time
import asyncio

class InMemoryCache:
    def __init__(self):
        self.store = {}

    async def get(self, key: str):
        entry = self.store.get(key)
        if not entry:
            return None
        value, expire_at = entry
        if expire_at and time.time() > expire_at:
            del self.store[key]
            return None
        return value

    async def set(self, key: str, value, ttl: int = 60):
        expire_at = time.time() + ttl if ttl else None
        self.store[key] = (value, expire_at)
