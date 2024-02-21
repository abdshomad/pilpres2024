import asyncio
import aiohttp
import json

async def fetch_url(session, url):
    print('Enter fetch_url ', session, url)
    async with session.get(url) as response:
        return await response.json()

async def fetch_urls(urls):
    print('Enter fetch_urls ', urls)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

async def main():
    # Read URLs from file
    print('Entering main ')
    with open("./data/05-tps-url.txt", "r") as file:
        urls = [line.strip() for line in file]

    # Split URLs into batches of size 10
    batch_size = 10
    url_batches = [urls[i:i+batch_size] for i in range(0, len(urls), batch_size)]

    # Fetch data asynchronously for each batch
    all_results = []
    for url_batch in url_batches:
        results = await fetch_urls(url_batch)
        all_results.extend(results)

    # Save the results to "05-suara-per-tps.json"
    with open("./data/06-suara-per-tps.json", "w") as outfile:
        json.dump(all_results, outfile, indent=4)

# Run the main coroutine
asyncio.run(main())
