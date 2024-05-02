#!/usr/bin/env python3
"""redis basic"""
import redis
import requests
from functools import wraps
from typing import Callable


def cached(func: Callable) -> Callable:
    """Decorator to cache function results"""

    @wraps(func)
    def wrapper(url):
        """Wrapper function"""

        cache_key = f"cached:{url}"
        cached_response = redis_client.get(cache_key)
        if cached_response:
            return cached_response.decode('utf-8')

        response = func(url)
        redis_client.setex(cache_key, 10, response)
        return response

    return wrapper


def count_calls(func: Callable) -> Callable:
    """Decorator to count how many times a function is called"""

    @wraps(func)
    def wrapper(url):
        """Wrapper function"""

        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)

    return wrapper


@count_calls
@cached
def get_page(url: str) -> str:
    """Get the HTML content of the given URL"""
    results = requests.get(url)
    return results.text
