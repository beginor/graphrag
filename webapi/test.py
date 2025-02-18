import asyncio

from .search_helper import do_global_search_streaming, do_local_search_streaming, \
    do_local_search, do_global_search, do_question_gen


root = 'ragtest/laws'

async def test_global_search_streaming():

    async for result in do_global_search_streaming(
        root=root,
        query='中华人民共和国大气污染防治法概述'
    ):
        print(result, end='')


async def test_global_search():
    (result, refs) = await do_global_search(
        root=root,
        query='中华人民共和国大气污染防治法概述'
    )
    print(type(result))
    print(result)
    print(type(refs))
    print(refs)


async def test_local_search_streaming():

    async for result in do_local_search_streaming(
        root=root,
        query='什么是水资源？'
    ):
        print(result, end='')


async def test_local_search():
    (result, refs) = await do_local_search(
        root=root,
        query='什么是水资源？'
    )
    print(type(result))
    print(result)
    print(type(refs))
    print(refs)


async def test_question_gen():
    result = await do_question_gen(
        root=root,
        question_history=['什么是水资源？']
    )
    print(result.response)


if __name__ == '__main__':
    # asyncio.run(test_global_search_streaming())
    # asyncio.run(test_local_search_streaming())
    # asyncio.run(test_global_search())
    # asyncio.run(test_local_search())
    # asyncio.run(test_question_gen())
    
