from functools import wraps
from fastapi import Request, HTTPException
import os
from src.shared.constants import STATUS_FORBIDDEN

API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY = os.getenv("API_KEY")


def require_api_key(endpoint_func):
    @wraps(endpoint_func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if not request:
            raise HTTPException(
                status_code=STATUS_FORBIDDEN,
                detail="Forbidden: No Request object found",
            )
        api_key = request.headers.get(API_KEY_NAME)
        if api_key != API_KEY:
            raise HTTPException(
                status_code=STATUS_FORBIDDEN,
                detail="Forbidden: Invalid API Key",
            )
        return await endpoint_func(*args, **kwargs)

    return wrapper
