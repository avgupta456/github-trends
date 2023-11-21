from asyncio import sleep
from datetime import timedelta
from typing import Tuple

from aiounittest.case import AsyncTestCase

from src.utils import alru_cache


class TestTemplate(AsyncTestCase):
    async def test_basic_alru_cache(self):
        count = 0

        @alru_cache()
        async def f(x: int) -> Tuple[bool, int]:
            nonlocal count
            count += 1
            return (True, x)

        assert count == 0
        assert await f(1) == 1
        assert count == 1
        assert await f(1) == 1
        assert count == 1
        assert await f(2) == 2
        assert count == 2
        assert await f(2) == 2
        assert count == 2
        assert await f(1) == 1
        assert count == 2

    async def test_alru_cache_with_flag(self):
        count = 0

        @alru_cache()
        async def f(x: int) -> Tuple[bool, int]:
            nonlocal count
            count += 1
            return (count % 2 == 0, x)

        assert count == 0
        assert await f(1) == 1
        assert count == 1
        assert await f(1) == 1
        assert count == 2
        assert await f(2) == 2
        assert count == 3
        assert await f(3) == 3
        assert count == 4
        assert await f(3) == 3
        assert count == 4

    async def test_alru_cache_with_maxsize(self):
        count = 0

        @alru_cache(max_size=2)
        async def f(x: int) -> Tuple[bool, int]:
            nonlocal count
            count += 1
            return (True, x)

        assert count == 0
        assert await f(1) == 1
        assert count == 1
        assert await f(2) == 2
        assert count == 2
        assert await f(3) == 3
        assert count == 3
        assert await f(1) == 1
        assert count == 4

    async def test_alru_cache_with_ttl(self):
        count = 0

        @alru_cache(ttl=timedelta(milliseconds=1))
        async def f(x: int) -> Tuple[bool, int]:
            nonlocal count
            count += 1
            return (True, x)

        assert count == 0
        assert await f(1) == 1
        assert count == 1
        assert await f(1) == 1
        assert count == 1
        await sleep(0.01)
        assert await f(1) == 1
        assert count == 2

    async def test_alru_cache_with_no_cache(self):
        count = 0

        @alru_cache()
        async def f(x: int, no_cache: bool = False) -> Tuple[bool, int]:
            nonlocal count
            count += 1
            return (True, x)

        assert count == 0
        assert await f(1) == 1
        assert count == 1
        assert await f(1) == 1
        assert count == 1
        assert await f(2) == 2
        assert count == 2
        assert await f(2, no_cache=True) == 2
        assert count == 3
        assert await f(3) == 3
        assert count == 4
        assert await f(3, no_cache=False) == 3
        assert count == 4
