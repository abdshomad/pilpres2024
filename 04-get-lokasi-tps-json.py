import wget
import pandas as pd
import os 

# Load JSON data into a pandas DataFrame
propinsi_df = pd.read_json('./data/00-propinsi.json')
kabupaten_kota_df = pd.read_json('./data/01-kabupaten_kota.json')
kecamatan_df = pd.read_json('./data/02-kecamatan.json')
kelurahan_df = pd.read_json('./data/03-kelurahan.json')

propinsi_df['kode'] = propinsi_df['kode'].astype(str)
kabupaten_kota_df['kode'] = kabupaten_kota_df['kode'].astype(str)
kecamatan_df['kode'] = kecamatan_df['kode'].astype(str)
kelurahan_df['kode'] = kelurahan_df['kode'].astype(str)

propinsi_df_sorted = propinsi_df.sort_values(by='kode', ascending=True)
filtered_propinsi_df = propinsi_df_sorted[propinsi_df_sorted['kode'] > '00'] # Filetr data by this value 

kabupaten_kota_df = kabupaten_kota_df.sort_values(by='kode', ascending=True)
kecamatan_df = kecamatan_df.sort_values(by='kode', ascending=True)
kelurahan_df = kelurahan_df.sort_values(by='kode', ascending=True)

directory_path = './data'

# Display the DataFrame
# print('propinsi_df', propinsi_df) # OK
# print('kabupaten_kota_df', kabupaten_kota_df) # OK

for kode_propinsi in filtered_propinsi_df['kode']:
    print('Processing Propinsi : ', kode_propinsi)
    filtered_kabupaten_kota_df = kabupaten_kota_df[kabupaten_kota_df['kode'].str[:2] == kode_propinsi]
    # print('filtered_kabupaten_kota_df', filtered_kabupaten_kota_df) # OK
    # print(filtered_df['kode'])
    for kode_kabupaten_kota in filtered_kabupaten_kota_df['kode']:
        print('Processing Kabupaten/Kota : ', kode_kabupaten_kota)
        filtered_kecamatan_df = kecamatan_df[kecamatan_df['kode'].str[:4] == kode_kabupaten_kota]
        # print('filtered_kecamatan_df', filtered_kecamatan_df) # OK
        for kode_kecamatan in filtered_kecamatan_df['kode']:
            print('Processing Kecamatan : ', kode_kecamatan)
            filtered_kelurahan_df = kelurahan_df[kelurahan_df['kode'].str[:6] == kode_kecamatan]
            # print('filtered_kelurahan_df', filtered_kelurahan_df) # OK
            for kode_kelurahan in filtered_kelurahan_df['kode']:
                filtered_tps_df = kelurahan_df[kelurahan_df['kode'].str[:8] == kode_kelurahan]
                # print('filtered_tps_df', filtered_tps_df) # OK
                # url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/36/3671.json' # kecamatan 
                # url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/36/3671/367107.json' # kelurahan 
                url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/'+kode_propinsi+'/'+kode_kabupaten_kota+'/'+kode_kecamatan+'/'+kode_kelurahan+'.json'
                # print(url)
                file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan + '.json' )
                # print(file_path)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                if os.path.exists(file_path):
                    # print('File: ', file_path, ' Exists')
                    pass 
                else:
                    filename = wget.download(url, out=file_path)
                    print(f"File '{filename}' downloaded.")

# import json
# import os

# # Define the directory containing the JSON files
# directory_path = './data/'

# # Initialize an empty list to store the combined JSON data
# combined_data = []

# print('Creating ', directory_path + '03-kelurahan.json')

# # Iterate over the range of file numbers from 11 to 55
# for i in range(110101, 999999):
#     # Construct the file path for each file
#     file_path = os.path.join(directory_path, str(i)[:2], str(i)[:4], f"{i}.json")

#     # Check if the file exists
#     if os.path.exists(file_path):
#         # Open and load JSON data from the file
#         with open(file_path, 'r') as file:
#             json_data = json.load(file)

#             # Extend the combined_data list with the loaded JSON data
#             combined_data.extend(json_data)

# # Write the combined data to merged.json
# with open(directory_path + '03-kelurahan.json', 'w') as merged_file:
#     json.dump(combined_data, merged_file)

# print("Merged JSON data has been written to 03-kelurahan.json.")
