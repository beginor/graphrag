from graphrag.api import global_search_streaming, local_search_streaming, drift_search_streaming
from graphrag.config.load_config import load_config
from pathlib import Path

import pandas as pd
import asyncio

from .search_helper import do_global_search, do_local_search


root = 'ragtest/laws'

async def test_global_search():

    async for result in do_global_search(
        root=root,
        query='中华人民共和国大气污染防治法概述'
    ):
        print(result, end='')


async def test_local_search():

    async for result in do_local_search(
        root=root,
        query='什么是水资源？'
    ):
        print(result, end='')


if __name__ == '__main__':
    asyncio.run(test_local_search())
