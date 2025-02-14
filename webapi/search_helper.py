from typing import AsyncGenerator
import json
import datetime

from graphrag.api import global_search_streaming, local_search_streaming
from graphrag.config.load_config import load_config
from pathlib import Path
from pandas import read_parquet


def warp_to_openai_chunk(content: str, finish: bool = False) -> dict:
    choice = {
        "finish_reason": "stop" if finish else None,
        "index": 0,
        "delta": { } if finish else { "content": content }
    }
    timestamp = datetime.datetime.now().timestamp()
    chunk = {
        "choices": [choice],
        "created": int(timestamp),
        "id": f'graphrag-chatcmpl-{timestamp}',
        "model": "graphrag",
        "system_fingerprint": "graphrag",
        "object": "chat.completion.chunk"
    }
    return chunk


async def do_global_search(root: str, query: str) -> AsyncGenerator[str, None]:
    config = load_config(Path(root))

    communities = read_parquet(root + '/output/communities.parquet')
    community_level = communities['level'].max()

    async for content in global_search_streaming(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=communities,
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        community_level=community_level,
        dynamic_community_selection=True,
        response_type='Multiple Paragraphs',
        query=query
    ):
        if type(content) is str:
            chunk = warp_to_openai_chunk(content)
            yield f'data: {json.dumps(chunk)}\n\n'

    end_chunk = warp_to_openai_chunk(content='', finish=True)
    yield f'data: {json.dumps(end_chunk)}\n\n'
    yield 'data: [DONE]\n\n'


async def do_local_search(root: str, query: str) -> AsyncGenerator[str, None]:
    config = load_config(Path(root))

    communities = read_parquet(root + '/output/communities.parquet')
    community_level = communities['level'].max()

    async for content in local_search_streaming(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=communities,
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        text_units=read_parquet(root + '/output/text_units.parquet'),
        relationships=read_parquet(root + '/output/relationships.parquet'),
        covariates=None,
        community_level=community_level,
        response_type='Multiple Paragraphs',
        query=query
    ):
        if (type(content) is str):
            chunk = warp_to_openai_chunk(content)
            yield f'data: {json.dumps(chunk)}\n\n'

    end_chunk = warp_to_openai_chunk(content='', finish=True)
    yield f'data: {json.dumps(end_chunk)}\n\n'
    yield 'data: [DONE]\n\n'
