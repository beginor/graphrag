from graphrag.api import global_search_streaming, local_search_streaming, drift_search_streaming
from graphrag.config.load_config import load_config
from pathlib import Path

import pandas as pd
import asyncio


root = 'ragtest/grimm-stories'

async def test_global_search():

    config = load_config(
        Path(root), 
        Path(root + '/settings.yaml')
    )

    async for result in global_search_streaming(
        config,
        pd.read_parquet(root + '/output/entities.parquet'),
        pd.read_parquet(root + '/output/communities.parquet'),
        pd.read_parquet(root + '/output/community_reports.parquet'),
        None,
        True,
        'Multiple Paragraphs',
        '渔夫和金鱼的故事说明了什么？'
    ):
        print(result, end='')


async def test_local_search():
    config = load_config(
        Path(root), 
        Path(root + '/settings.yaml')
    )

    async for result in local_search_streaming(
        config,
        pd.read_parquet(root + '/output/entities.parquet'),
        pd.read_parquet(root + '/output/communities.parquet'),
        pd.read_parquet(root + '/output/community_reports.parquet'),
        pd.read_parquet(root + '/output/text_units.parquet'),
        pd.read_parquet(root + '/output/relationships.parquet'),
        None,
        0,
        'Multiple Paragraphs',
        '比目鱼直接实现了渔夫的妻子许下的哪些愿望，请给出一个列表？'
    ):
        print(result, end='')


if __name__ == '__main__':
    asyncio.run(test_local_search())
