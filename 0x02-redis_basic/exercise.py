#!/usr/bin/env python3
"""Redis basic"""
import functools
import redis
import uuid
from typing import Union, Callable, Optional


def count_calls(func: Callable) -> Callable:
    """Decorator to count how many times a method is called."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        key = func.__qualname__
        self._redis.incr(key)
        return func(self, *args, **kwargs)

    return wrapper


def call_history(func: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a particular function
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        input_key = f"{func.__qualname__}:inputs"
        output_key = f"{func.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = func(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


class Cache:
    """Class using Redis for storage"""
    def __init__(self):
        """Store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        if isinstance(data, (int, float)):
            data = str(data)
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, None]:
        """
        Get method that takes a key string argument
        and an optional Callable argument named fn
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """Will automatically parametrize Cache.get"""
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Will automatically parametrize Cache.get"""
        return self.get(key, fn=int)


Cache.store = count_calls(Cache.store)
