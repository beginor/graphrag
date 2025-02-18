from pydantic import BaseModel, Field


class KnowledgeBaseModel(BaseModel):
    root_dir: str = Field(
        description='root directory for the model',
        default=''
    )
    title: str = Field(
        description='title of the model',
        default=''
    )


knowledge_base_models:list[KnowledgeBaseModel] = [
    KnowledgeBaseModel(
        root_dir='ragtest/laws',
        title='环境法规'
    ),
    KnowledgeBaseModel(
        root_dir='ragtest/gdee-rules',
        title='监测中心内部管理规定'
    )
]


def get_model_root(title: str) -> str:
    for kb in knowledge_base_models:
        if kb.title == title:
            return kb.root_dir
    return ''


class QuestionGenModel(BaseModel):
    model: str = Field(
        description='模型名称',
        default='环境法规:局部搜索'
    )
    query_history: list[dict] = Field(
        description='query history',
        default=[]
    )
