import wget
import pandas as pd
import os 
import json 

def download_images(json_file_path): 
    print('Entering download images')
    print('json_file_path', json_file_path)
    images_url = json.load(open(json_file_path, 'r')).get('images', [])
    # print('images_url', images_url)
    # if images_url : 
    for image_url in images_url: 
        if image_url: 
            # print('image_url', image_url)
            image_filename = os.path.basename(image_url)
            # print('image_filename', image_filename)
            image_file_path = os.path.join(os.path.dirname(json_file_path), image_filename)
            image_file_path = image_file_path.replace('\\', '/')
            image_file_path = image_file_path.replace('/data/', '/images/')
            os.makedirs(os.path.dirname(image_file_path), exist_ok=True)
            print('image_file_path', image_file_path)
            if not os.path.exists(image_file_path):
                downloaded_filename = wget.download(image_url, out=image_file_path)
                # filename = image_filename
                print(f"File '{downloaded_filename}' downloaded.")
            else: 
                # print('image_file_path', image_file_path, ' Existed')
                pass

# url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/36/3671/367107/3671071008.json'

propinsi_df         = pd.read_json('./data/00-propinsi.json')
kabupaten_kota_df   = pd.read_json('./data/01-kabupaten_kota.json')
kecamatan_df        = pd.read_json('./data/02-kecamatan.json')
kelurahan_df        = pd.read_json('./data/03-kelurahan.json')

propinsi_df['kode'] = propinsi_df['kode'].astype(str)
kabupaten_kota_df['kode'] = kabupaten_kota_df['kode'].astype(str)
kecamatan_df['kode'] = kecamatan_df['kode'].astype(str)
kelurahan_df['kode'] = kelurahan_df['kode'].astype(str)

propinsi_df_sorted = propinsi_df.sort_values(by='kode', ascending=True)
filtered_propinsi_df = propinsi_df_sorted[propinsi_df_sorted['kode'] > '00'] # Filetr data by this value 
kabupaten_kota_df = kabupaten_kota_df.sort_values(by='kode', ascending=True)
kecamatan_df = kecamatan_df.sort_values(by='kode', ascending=True)
# kelurahan_df = kelurahan_df.sort_values(by='kode', ascending=True)

directory_path = './data'

# TEST ONLY 
filtered_kelurahan_df = kelurahan_df[kelurahan_df['kode'] > '0000000000'] # 3671071008

for kode_kelurahan in filtered_kelurahan_df['kode']: 
    print('For loop kode kelurahan', kode_kelurahan)
    # kode_kelurahan = '3671071008'
    kode_propinsi = kode_kelurahan[:2]
    kode_kabupaten_kota = kode_kelurahan[:4]
    kode_kecamatan = kode_kelurahan[:6]
    # kode_kelurahan = kode_kelurahan[:8]

    tps_json_kelurahan_file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan + '.json' )

    kelurahan_df = pd.read_json(tps_json_kelurahan_file_path)
    kelurahan_df['kode'] = kelurahan_df['kode'].astype(str)

    # print('kode_propinsi', kode_propinsi)
    # print('kode_kabupaten_kota', kode_kabupaten_kota)
    # print('kode_kecamatan', kode_kecamatan)
    # print('kode_kelurahan', kode_kelurahan)
    # print('json_file_path', json_file_path)
    # print('kelurahan_df', kelurahan_df)

    for kode_tps in kelurahan_df['kode']:
        print('For loop kode tps ', kode_tps)
        # print('kode_tps', kode_tps) 
        # url = 'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/36/3671/367107/3671071008/3671071008003.json' # contoh url TPS 
        tps_url_path = os.path.join('https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/', kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan, kode_tps + '.json' )
        tps_url_path = tps_url_path.replace('\\', '/')
        # print('tps_url_path', tps_url_path)
        tps_json_file_path = os.path.join(tps_json_kelurahan_file_path.replace('.json', ''), kode_tps + '.json')
        # print('json_file_path', json_file_path)
        os.makedirs(os.path.dirname(tps_json_file_path), exist_ok=True)
        if os.path.exists(tps_json_file_path):
            print('File: ', tps_json_file_path, ' Exists')
            # print()
            download_images(tps_json_file_path)
            pass 
        else:
            print(tps_json_file_path, ' Is not exist? Downloading ... ')
            downloaded_filename = wget.download(tps_url_path, out=tps_json_file_path)
            # print(f"File '{json_filename}' downloaded.")
            download_images(tps_json_file_path)
            # images = json.load(filename)
            # print(images)

exit() 
