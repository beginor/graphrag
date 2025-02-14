from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .search_helper import do_local_search, do_global_search

router = APIRouter(
    prefix="",
    tags=["chat"]
)

root = 'ragtest/laws'

@router.post('/v1/chat/completions')
async def completions(request: Request) -> StreamingResponse:
    dict = await request.json()
    model: str = dict['model'] # grimm-stories:local
    search_method = model.split(':')[-1]
    messages: list = dict['messages']
    query = messages[-1]['content']

    if search_method == '全局搜索':
        generator = do_global_search(
            root=root,
            query= query if query else '当前知识库包含哪些环境法律法规？'
        )
    else:
        generator = do_local_search(
            root=root,
            query= query if query else '什么是环保税？'
        )
    return StreamingResponse(
        generator,
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream'
        }
    )
