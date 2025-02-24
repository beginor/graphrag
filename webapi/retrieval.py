from typing import Dict, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .search_helper import get_local_search_context_data
from .config import get_model_root


router = APIRouter(
    prefix="",
    tags=["dify"]
)


class RetrievalSetting(BaseModel):
    top_k: int = Field(
        description="Maximum number of retrieved results",
        default=5
    )
    score_threshold: float = Field(
        description="The score limit of relevance of the result to the query, scope: 0~1",
        default=0.5
    )


class RetrievalRequest(BaseModel):
    knowledge_id: str = Field(
        description="Your knowledge's unique ID",
        default=''
    )
    query: str = Field(
        description="User's query",
        default=''
    )
    retrieval_setting: RetrievalSetting = Field(
        description="Knowledge's retrieval parameters",
        default=RetrievalSetting()
    )


class RetrievalRecord(BaseModel):
    content: str = Field(
        description="Contains a chunk of text from a data source in the knowledge base.",
        default=''
    )
    score: float = Field(
        description="The score of relevance of the result to the query, scope: 0~1",
        default=0.5
    )
    title: str = Field(
        description="Document title",
        default=''
    )
    metadata: Dict[str, str] = Field(
        description="Contains metadata attributes and their values for the document in the data source.",
        default={}
    )


class RetrievalResponse(BaseModel):
    records: List[RetrievalRecord] = Field(
        description="A list of records from querying the knowledge base.",
        default=[]
    )



@router.post("/v1/retrieval")
async def retrieval(req: RetrievalRequest) -> RetrievalResponse:
    root = get_model_root(req.knowledge_id)

    if root == '':
        raise Exception('Knowledge not found')

    context_data: str = get_local_search_context_data(root, req.query) # type: ignore
    record = RetrievalRecord(
        content=context_data,
        title=f'知识图谱中关于“{req.query}”的相关资料',
        score=0.99,
        metadata={}
    )

    content = RetrievalResponse(
        records=[record]
    )

    return content
