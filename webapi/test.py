from graphrag.api import global_search_streaming, local_search_streaming, drift_search_streaming
from graphrag.config.load_config import load_config
from pathlib import Path

import pandas as pd
import asyncio

from .search_helper import do_global_search, do_local_search


root = 'ragtest/grimm-stories'

async def test_global_search():

    async for result in do_global_search(
        root=root,
        query='渔夫和金鱼的故事说明了什么？'
    ):
        print(result, end='')


async def test_local_search():

    async for result in do_local_search(
        root=root,
        query='比目鱼直接实现了渔夫的妻子许下的哪些愿望，请给出一个列表？'
    ):
        print(result, end='')


if __name__ == '__main__':
    asyncio.run(test_local_search())
