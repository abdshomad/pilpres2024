import aiohttp
import asyncio
import os
import pandas as pd
import json

async def download_file(session, url, file_path):
    print('Entering download_file', session, url, file_path)
    async with session.get(url) as response:
        print('Response status = ', response.status, session, url, file_path, response)
        if response.status == 200:
            print('Response status is 200 ', session, url, file_path, response)
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    print('Write chunk: ', chunk)

async def redownload_json_hasil_tps_if_changed(session, tps_json_file_path, tps_url_path):
    print('Entering redownload_json_hasil_tps_if_changed', session, tps_json_file_path, tps_url_path)
    images_url = json.load(open(tps_json_file_path, 'r')).get('images', [])
    redownload_json_hasil_tps = False
    for image_url in images_url:
        if not image_url:
            redownload_json_hasil_tps = True
            break
    if redownload_json_hasil_tps:
        print('Temporary, skip re-download')
        pass 
        # await download_file(session, tps_url_path, tps_json_file_path)

async def main():
    print('Entering main')
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(10)  # Limiting concurrent connections to 10 per batch

        propinsi_df = pd.read_json('./data/propinsi.json')
        kabupaten_kota_df = pd.read_json('./data/kabupaten_kota.json')
        kecamatan_df = pd.read_json('./data/kecamatan.json')
        kelurahan_df = pd.read_json('./data/kelurahan.json')

        propinsi_df['kode'] = propinsi_df['kode'].astype(str)
        kabupaten_kota_df['kode'] = kabupaten_kota_df['kode'].astype(str)
        kecamatan_df['kode'] = kecamatan_df['kode'].astype(str)
        kelurahan_df['kode'] = kelurahan_df['kode'].astype(str)

        propinsi_df_sorted = propinsi_df.sort_values(by='kode', ascending=True)
        filtered_propinsi_df = propinsi_df_sorted[propinsi_df_sorted['kode'] > '00'] # Filetr data by this value 
        kabupaten_kota_df = kabupaten_kota_df.sort_values(by='kode', ascending=True)
        kecamatan_df = kecamatan_df.sort_values(by='kode', ascending=True)
        kelurahan_df = kelurahan_df.sort_values(by='kode', ascending=True)

        filtered_kecamatan_df = kecamatan_df[kecamatan_df['kode'] > '3173'] # 3671071008
        filtered_kelurahan_df = kelurahan_df[kelurahan_df['kode'] > '3671071008'] # 3671071008

        directory_path = './hasil-tps/'

        for kode_tps in filtered_kelurahan_df['kode']:
            print('Processing tps: ', kode_tps)
            kode_propinsi = kode_tps[:2]
            kode_kabupaten_kota = kode_tps[:4]
            kode_kecamatan = kode_tps[:6]
            kode_kelurahan = kode_tps[:10]
            tps_json_kelurahan_file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan + '.json' )

            print('Processing tps: ', kode_tps)
            test_url = 'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/63/6303/630305/63030510/6303051002.json'
            test_url = 'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/36/3671/367107/3671071008/3671071008003.json' # contoh url TPS 

            tps_url_path = os.path.join('https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/',
                                        kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan,
                                        kode_tps + '.json')
            tps_url_path = tps_url_path.replace('\\', '/')
            tps_json_file_path = os.path.join(tps_json_kelurahan_file_path.replace('.json', ''),
                                                kode_tps + '.json')

            os.makedirs(os.path.dirname(tps_json_file_path), exist_ok=True)
            print('Makedir: ', os.path.dirname(tps_json_file_path))
            if os.path.exists(tps_json_file_path):
                await redownload_json_hasil_tps_if_changed(session, tps_json_file_path, tps_url_path)
            else:
                async with semaphore:
                    tasks.append(download_file(session, tps_url_path, tps_json_file_path))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
