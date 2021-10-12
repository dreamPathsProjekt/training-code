import asyncio


async def download(urls):
    for url in urls:
        await asyncio.sleep(1)
        response = {'status': 200, 'data': f'content of {url}'}
        if url == 'bing.com':
            response['status'] = 500
        yield response


async def handle(err_response):
    print('logging error response for', err_response)


async def main():
    urls = [
        'google.com',
        'bing.com',
        'duckduckgo.com',
    ]

    errors = [r async for r in download(urls) if r['status'] != 200]
    print(errors)

    [await handle(e) for e in errors]


asyncio.run(main())
