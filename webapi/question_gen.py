from fastapi import APIRouter, Request

from .config import QuestionGenModel, get_model_root
from .search_helper import do_question_gen


router = APIRouter(
    prefix="",
    tags=["openqi"]
)

@router.post('/v1/chat/question-gen')
async def question_gen(question_gen: QuestionGenModel):

    model = question_gen.model
    query_history = question_gen.query_history
    root = get_model_root(model.split(':')[0])

    if root == '':
        return {
            'error': 'model not found'
        }

    result = await do_question_gen(
        root=root,
        question_history=query_history
    )
