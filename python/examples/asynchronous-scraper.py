
import asyncio
import aiohttp
from time import time


sites = [
    "http://news.ycombinator.com/",
    "https://www.yahoo.com/",
    "http://salmonofcapistrano.com/",
    "https://mail.ru/"
]


async def find_size(session, url):
    async with session.get(url) as response:
        page = await response.read()
        return len(page)


async def show_size(idx, session, url):
    start_time = time()
    size = await find_size(session, url)
    print("Read {:8d} chars from [{}]/{} in {:6.3f} secs".format(size, idx, url, time() - start_time))


async def main(loop):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for idx, site in enumerate(sites):
            tasks.append(loop.create_task(show_size(idx, session, site)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = time()
    print("Start executing...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("Ran in {:6.3f} secs".format(time() - start_time))
    print("End executing...")
