from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def custom_key_func(request: Request):
    return request.headers.get("X-Forwarded-For", request.client.host)

limiter = Limiter(key_func=custom_key_func)
