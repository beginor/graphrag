from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["models"]
)


@router.get("/v1/models")
async def models():
    return {
        "object": "list",
        "data": [
            {
                "id": "环境法规:全局搜索",
                "object": "model",
                "created": 1739352563,
                "owned_by": "graphrag"
            },
            {
                "id": "环境法规:局部搜索",
                "object": "model",
                "created": 1739352563,
                "owned_by": "graphrag"
            }
        ]
    }

