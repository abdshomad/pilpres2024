import aiohttp
import asyncio
import os

async def fetch_url(session, url):
    print('Enter fetch_url', session, url)
    async with session.get(url) as response:
        result = await response.text()
        return result

async def fetch_urls(urls):
    # print('Enter fetch_urls', urls)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch_url(session, url))
            tasks.append(task)

        # Gather and return results
        return await asyncio.gather(*tasks)

async def main():
    # Read URLs from file
    urls_file = "data/05-tps-url.txt"
    print("Read URLs from file", urls_file)
    with open(urls_file, "r") as file:
        urls = [line.strip() for line in file.readlines()]

    # Divide URLs into batches
    batch_size = 20
    url_batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
    # print("url_batches", url_batches)
    # Fetch URLs asynchronously in batches
    i = 0 
    for batch in url_batches:
        i = i + 1 
        if i < 2: 
            # print('batch', batch)
            results = await fetch_urls(batch)
            # Print results for this batch
            for result in results:
                print("Result: iterasi ke-", i, "\nResult : ", result, "\nBatch[0] : ", batch[0], "\nurl_batches[0] : ", url_batches[0])
                pass 
        else: 
            print("Exit, i = ", i)
            exit() 

if __name__ == "__main__":
    asyncio.run(main())
