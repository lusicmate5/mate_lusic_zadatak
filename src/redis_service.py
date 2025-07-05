import os
import json
import redis


class RedisService:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def get(self, key: str):
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"[CACHE GET ERROR] {e}")
        return None

    def set(self, key: str, value: dict, expire_seconds: int = 60):
        try:
            self.client.setex(key, expire_seconds, json.dumps(value))
        except Exception as e:
            print(f"[CACHE SET ERROR] {e}")
