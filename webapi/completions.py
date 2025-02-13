from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from graphrag.api import global_search_streaming, local_search_streaming, drift_search_streaming
from graphrag.config.load_config import load_config
from pathlib import Path

import pandas as pd


router = APIRouter(
    prefix="",
    tags=["chat"]
)

root = 'ragtest/grimm-stories'

config = load_config(
    Path(root), 
    Path(root + '/settings.yaml')
)

@router.post('/v1/chat/completions')
async def completions(request: Request) -> StreamingResponse:
    dict = await request.json()
    print(dict)
    generator = local_search_streaming(
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
    )
    return StreamingResponse(
        generator,
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream'
        }
    )
