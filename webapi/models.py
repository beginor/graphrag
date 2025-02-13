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
                "id": "grimm-stories:global",
                "object": "model",
                "created": 1739352563,
                "owned_by": "graphrag"
            },
            {
                "id": "grimm-stories:local",
                "object": "model",
                "created": 1739352563,
                "owned_by": "graphrag"
            }
        ]
    }

