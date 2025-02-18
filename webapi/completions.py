from typing import Dict, List
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse

from .search_helper import do_local_search_streaming, do_global_search_streaming, \
    do_local_search, do_global_search, wrap_to_openai_chat_completion
from .config import get_model_root


router = APIRouter(
    prefix="",
    tags=["openqi"]
)


@router.post('/v1/chat/completions')
async def completions(request: Request):
    dict: Dict = await request.json()
    print('request data is:')
    print(dict)
    model: str = dict['model'] # grimm-stories:local
    search_method = model.split(':')[-1]
    last_message: Dict = dict['messages'][-1]
    query: str = last_message['content']
    streaming = dict.get('stream', False)

    root = get_model_root(model.split(':')[0])

    if root == '':
        return JSONResponse(
            status_code=404,
            content={ "error": "model not found" }
        )

    if query.strip() == 'ping':
        return JSONResponse(
            content=wrap_to_openai_chat_completion('hello,world!')
        )

    if streaming != False:
        if search_method == '全局搜索':
            generator = do_global_search_streaming(
                root=root,
                query= query
            )
        else:
            generator = do_local_search_streaming(
                root=root,
                query= query
            )
        return StreamingResponse(
            generator,
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'text/event-stream'
            }
        )

    else:
        if search_method == '全局搜索':
            (content, refs) = await do_global_search(
                root=root,
                query= query
            )
        else:
            (content, refs) = await do_local_search(
                root=root,
                query= query
            )

        return JSONResponse(
            content=wrap_to_openai_chat_completion(content), # type: ignore
        )
