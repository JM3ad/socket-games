from functools import wraps
import json

from async_timeout import timeout
import pytest


def with_timeout(corofunc):
    @wraps(corofunc)
    async def wrapper(*args, **kwargs):
        async with timeout(1):
            return await corofunc(*args, **kwargs)

    return wrapper
