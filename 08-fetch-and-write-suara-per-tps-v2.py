import asyncio
import aiohttp
import json
import os

async def fetch_url(session, url):
    # print('Enter fetch_url ', session, url)
    async with session.get(url) as response:
        return await response.json()

async def fetch_and_save(urls):
    # print('Enter fetch_and_save ', urls)
    async with aiohttp.ClientSession() as session:
        for url in urls:
            data = await fetch_url(session, url)
            # Extract filename from URL
            filename = url.split('/')[-1]
            # Extract directory structure from URL
            # directory = '/'.join(url.split('/')[3:-1]) # Assuming URL structure has at least 4 parts (e.g., https://example.com/part1/part2/part3/filename.json)
            directory = './hasil-tps/' + os.path.dirname(url)
            directory = directory.replace('/pemilu/hhcw/ppwp/', '')
            directory = directory.replace('https://sirekap-obj-data.kpu.go.id', '')
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            # Save data to file
            hasil_tps_json_file_path = os.path.join(directory, filename) 
            if not os.path.exists(hasil_tps_json_file_path):
                with open(hasil_tps_json_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                    print('Writing : ', hasil_tps_json_file_path)
            else: 
                print('Exist : ', hasil_tps_json_file_path)

async def main():
    # Read URLs from file
    with open("./data/05-tps-url.txt", "r") as file:
        urls = [line.strip() for line in file]

    # Fetch and save data asynchronously for each URL
    await fetch_and_save(urls)

# Run the main coroutine
asyncio.run(main())
