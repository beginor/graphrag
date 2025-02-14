import asyncio

from .search_helper import do_global_search, do_local_search, do_drift_search, do_question_gen


root = 'ragtest/laws'

async def test_global_search():
    async for result in do_global_search(
        root=root,
        query='中华人民共和国大气污染防治法概述'
    ):
        print(result, end='')


async def test_local_search():
    async for result in do_local_search(
        root=root,
        query='什么是水资源？'
    ):
        print(result, end='')


async def test_drift_search():
    async for result in do_drift_search(
        root='ragtest/grimm-stories',
        query='比目鱼直接帮渔夫的妻子实现了哪些愿望'
    ):
        print(result, end='')


async def test_question_gen():
    question_history = [
        '渔夫的妻子许下了哪些愿望',
        '比目鱼直接帮渔夫的妻子实现了哪些愿望'
    ]
    print('提问历史:')
    for q in question_history:
        print(f'  - {q}')

    result = await do_question_gen(
        root='ragtest/grimm-stories',
        question_history=question_history
    )
    print('建议的问题：')

    for r in result.response:
        print(f' {r}')


if __name__ == '__main__':
    asyncio.run(test_question_gen())
