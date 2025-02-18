from typing import AsyncGenerator
import json
import datetime

import tiktoken

from graphrag.api import global_search_streaming, local_search_streaming, global_search, local_search
from graphrag.api.query import drift_search_streaming, drift_search_streaming
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.indexer_adapters import read_indexer_entities, read_indexer_text_units, read_indexer_reports, \
    read_indexer_relationships
from graphrag.query.question_gen.local_gen import LocalQuestionGen, QuestionResult
from graphrag.config.load_config import load_config
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.vector_stores.lancedb import LanceDBVectorStore

from pathlib import Path
from pandas import read_parquet


def warp_to_openai_streaming_chunk(content: str, finish: bool = False) -> dict:
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


def wrap_to_openai_chat_completion(content: str) -> dict:
    timestamp = datetime.datetime.now().timestamp()
    completion = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                }
            }
        ],
        "created": int(timestamp),
        "id": f'graphrag-chatcmpl-{timestamp}',
        "model": "graphrag",
        "system_fingerprint": "graphrag",
        "object": "chat.completion"
    }
    return completion


COMMUNITY_LEVEL = 1


async def do_global_search_streaming(root: str, query: str) -> AsyncGenerator[str, None]:
    print(f'do global search streaming: {root}, {query}')
    config = load_config(Path(root))

    async for content in global_search_streaming(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=read_parquet(root + '/output/communities.parquet'),
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        community_level=COMMUNITY_LEVEL,
        dynamic_community_selection=True,
        response_type='Multiple Paragraphs',
        query=query
    ):
        if type(content) is str:
            chunk = warp_to_openai_streaming_chunk(content)
            yield f'data: {json.dumps(chunk)}\n\n'
        else:
            print(content)

    end_chunk = warp_to_openai_streaming_chunk(content='', finish=True)
    yield f'data: {json.dumps(end_chunk)}\n\n'
    yield 'data: [DONE]\n\n'


async def do_global_search(root: str, query: str):
    print(f'do global search: {root}, {query}')
    config = load_config(Path(root))

    result = await global_search(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=read_parquet(root + '/output/communities.parquet'),
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        community_level=COMMUNITY_LEVEL,
        dynamic_community_selection=True,
        response_type='Multiple Paragraphs',
        query=query
    )

    return result


async def do_local_search_streaming(root: str, query: str) -> AsyncGenerator[str, None]:
    print(f'do local search streaming: {root}, {query}')
    config = load_config(Path(root))

    async for content in local_search_streaming(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=read_parquet(root + '/output/communities.parquet'),
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        text_units=read_parquet(root + '/output/text_units.parquet'),
        relationships=read_parquet(root + '/output/relationships.parquet'),
        covariates=None,
        community_level=COMMUNITY_LEVEL,
        response_type='Multiple Paragraphs',
        query=query
    ):
        if (type(content) is str):
            chunk = warp_to_openai_streaming_chunk(content)
            yield f'data: {json.dumps(chunk)}\n\n'
        else:
            print(content)

    candidates = await do_question_gen(root, [query])

    more_trunk = warp_to_openai_streaming_chunk('\n\n可以提问更多相关问题吗？\n\n')
    yield f'data: {json.dumps(more_trunk)}\n\n'

    for question in candidates.response:
        chunk = warp_to_openai_streaming_chunk(f'{question}\n')
        yield f'data: {json.dumps(chunk)}\n\n'

    end_chunk = warp_to_openai_streaming_chunk(content='', finish=True)
    yield f'data: {json.dumps(end_chunk)}\n\n'
    yield 'data: [DONE]\n\n'


async def do_local_search(root: str, query: str):
    print(f'do local search: {root}, {query}')
    config = load_config(Path(root))

    result = await local_search(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=read_parquet(root + '/output/communities.parquet'),
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        text_units=read_parquet(root + '/output/text_units.parquet'),
        relationships=read_parquet(root + '/output/relationships.parquet'),
        covariates=None,
        community_level=COMMUNITY_LEVEL,
        response_type='Multiple Paragraphs',
        query=query
    )

    return result


async def do_drift_search(root: str, query: str) -> AsyncGenerator[str, None]:
    config = load_config(Path(root))

    async for content in drift_search_streaming(
        config=config,
        entities=read_parquet(root + '/output/entities.parquet'),
        communities=read_parquet(root + '/output/communities.parquet'),
        community_reports=read_parquet(root + '/output/community_reports.parquet'),
        text_units=read_parquet(root + '/output/text_units.parquet'),
        relationships=read_parquet(root + '/output/relationships.parquet'),
        community_level=COMMUNITY_LEVEL,
        response_type='Multiple Paragraphs',
        query=query
    ):
        if type(content) is str:
            chunk = warp_to_openai_streaming_chunk(content)
            yield f'data: {json.dumps(chunk)}\n\n'
        else:
            print(content)

    end_chunk = warp_to_openai_streaming_chunk(content='', finish=True)
    yield f'data: {json.dumps(end_chunk)}\n\n'
    yield 'data: [DONE]\n\n'


async def do_question_gen(root: str, question_history: list[str]) -> QuestionResult:
    config = load_config(Path(root))
    chat_model = config.models['default_chat_model']
    embedding_model = config.models['default_embedding_model']
    chat_llm = ChatOpenAI(
        model=chat_model.model,
        api_base=chat_model.api_base,
        api_key=chat_model.api_key,
        max_retries=chat_model.max_retries,
    )

    text_embedding = OpenAIEmbedding(
        model=embedding_model.model,
        api_base=embedding_model.api_base,
        api_key=embedding_model.api_key,
        max_retries=embedding_model.max_retries,
    )

    entity_df = read_parquet(root + '/output/entities.parquet')
    community_df = read_parquet(root + '/output/communities.parquet')
    entities = read_indexer_entities(entity_df, community_df, COMMUNITY_LEVEL)

    entity_embeddings = LanceDBVectorStore(
        collection_name='default-entity-description'
    )
    entity_embeddings.connect(db_uri=root + '/output/lancedb')

    text_unit_df = read_parquet(root + '/output/text_units.parquet')
    text_units = read_indexer_text_units(text_unit_df)

    community_report_df = read_parquet(root + '/output/community_reports.parquet')
    community_reports = read_indexer_reports(
        community_report_df,
        community_df,
        COMMUNITY_LEVEL,
        dynamic_community_selection=True,
        content_embedding_col='full_content_embedding',
        config=config
    )
    relationship_df = read_parquet(root + '/output/relationships.parquet')
    relationships = read_indexer_relationships(relationship_df)

    token_encoder = tiktoken.get_encoding('cl100k_base')

    context_builder = LocalSearchMixedContext(
        entities=entities,
        entity_text_embeddings=entity_embeddings,
        text_embedder=text_embedding,
        text_units=text_units,
        community_reports=community_reports,
        relationships=relationships,
        covariates=None,
        token_encoder=token_encoder,
    )

    local_question_gen = LocalQuestionGen(
        llm=chat_llm,
        context_builder=context_builder,
        token_encoder=token_encoder,
        llm_params={ "max_tokens": 2_000, "temperature": 0.0, },
        context_builder_params= {
            "text_unit_prop": 0.5,
            "community_prop": 0.1,
            "conversation_history_max_turns": 5,
            "conversation_history_user_turns_only": True,
            "top_k_mapped_entities": 10,
            "top_k_relationships": 10,
            "include_entity_rank": True,
            "include_relationship_weight": True,
            "include_community_rank": False,
            "return_candidate_context": False,
            "embedding_vectorstore_key": EntityVectorStoreKey.ID,  # set this to EntityVectorStoreKey.TITLE if the vectorstore uses entity title as ids
            "max_tokens": 12_000,  # change this based on the token limit you have on your model (if you are using a model with 8k limit, a good setting could be 5000)
        }
    )
    question_result = await local_question_gen.agenerate(
        question_history=question_history,
        context_data=None,
        question_count=5
    )
    return question_result
