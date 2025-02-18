import datetime
from fastapi import APIRouter

from .config import knowledge_base_models


router = APIRouter(
    prefix="",
    tags=["openqi"]
)


@router.get("/v1/models")
def models():
    data = []
    for kb in knowledge_base_models:
        data.append({
            'object': 'model',
            'id': f'{kb.title}:全局搜索',
            'created': int(datetime.datetime.now().timestamp()),
            'owned_by': 'graphrag'
        })
        data.append({
            'object': 'model',
            'id': f'{kb.title}:局部搜索',
            'created': int(datetime.datetime.now().timestamp()),
            'owned_by': 'graphrag'
        })

    return {
        "object": "list",
        "data": data
    }

