import aiohttp
import asyncio
import os
import json 

async def fetch_url(session, url, index):
    # print('Enter fetch_url', session, url)
    async with session.get(url) as response:
        filename = url.split('/')[-1]
        directory = os.path.dirname(url)
        directory = './hasil-tps/' + os.path.dirname(url)
        directory = directory.replace('/pemilu/hhcw/ppwp/', '')
        directory = directory.replace('https://sirekap-obj-data.kpu.go.id', '')
        os.makedirs(directory, exist_ok=True)
        hasil_tps_json_file_path = os.path.join(directory, filename) 
        if not os.path.exists(hasil_tps_json_file_path):
            result = await response.text()
            # print(f"Fetched data from URL {index}: {url}")
        else: 
            result = ''
        return url, result

async def fetch_urls(urls, batch_index):
    # print('Enter fetch_urls', urls)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, url in enumerate(urls, start=1):
            task = asyncio.ensure_future(fetch_url(session, url, batch_index * 20 + index))
            tasks.append(task)

        # Gather and return results
        return await asyncio.gather(*tasks)

async def main():
    # Read URLs from file
    urls_file = "data/05-tps-url.txt"
    print("Read URLs from file", urls_file)
    with open(urls_file, "r") as file:
        # urls = [line.strip() for line in file.readlines()]
        urls = [line.strip() for line in file.readlines() if "0000000000000" < line.split('/')[-1].strip()]


    # Divide URLs into batches
    batch_size = 100
    url_batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

    # Fetch URLs asynchronously in batches
    i = 0 
    for batch_index, batch in enumerate(url_batches):
        i = i + 1 
        if i < 200000000: 
            results = await fetch_urls(batch, batch_index)
            # Print results for this batch
            for url, result in results:
                print(f"URL Result: {url}")
                filename = url.split('/')[-1]
                directory = os.path.dirname(url)
                directory = './hasil-tps/' + os.path.dirname(url)
                directory = directory.replace('/pemilu/hhcw/ppwp/', '')
                directory = directory.replace('https://sirekap-obj-data.kpu.go.id', '')
                os.makedirs(directory, exist_ok=True)
                hasil_tps_json_file_path = os.path.join(directory, filename) 
                if not os.path.exists(hasil_tps_json_file_path):
                    # print("Result:")
                    # print(result)
                    with open(hasil_tps_json_file_path, 'w') as file:
                        # json.dump(result, file, indent=4)
                        file.write(result)
                        print('Writing : ', hasil_tps_json_file_path)
                else: 
                    print('Exist : ', hasil_tps_json_file_path)
        else: 
            print("Exit, i = ", i)
            exit() 

if __name__ == "__main__":
    asyncio.run(main())
