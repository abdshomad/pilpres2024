import wget
import pandas as pd
import os 

# Load JSON data into a pandas DataFrame
propinsi_df = pd.read_json('./data/propinsi.json')
kabupaten_kota_df = pd.read_json('./data/kabupaten_kota.json')

propinsi_df = propinsi_df.sort_values(by='kode', ascending=True)
kabupaten_kota_df = kabupaten_kota_df.sort_values(by='kode', ascending=True)

propinsi_df['kode'] = propinsi_df['kode'].astype(str)
kabupaten_kota_df['kode'] = kabupaten_kota_df['kode'].astype(str)

directory_path = './data'

# Display the DataFrame
# print('propinsi_df', propinsi_df) # OK
# print('kabupaten_kota_df', kabupaten_kota_df) # OK

for kode_propinsi in propinsi_df['kode']:
    print('Processing Propinsi : ', kode_propinsi)
    filtered_kabupaten_kota_df = kabupaten_kota_df[kabupaten_kota_df['kode'].str[:2] == kode_propinsi]
    print('filtered_kabupaten_kota_df', filtered_kabupaten_kota_df) # OK
    # print(filtered_df['kode'])
    for kode_kabupaten_kota in filtered_kabupaten_kota_df['kode']:
        url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/36/3671.json'
        url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/'+kode_propinsi+'/'+kode_kabupaten_kota+'.json'
        print(url)
        file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota + '.json' )
        print('file_path', file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path):
            print('File: ', file_path, ' Exists')
        else:
            filename = wget.download(url, out=file_path)
            print(f"File '{filename}' downloaded.")

import json
import os

# Define the directory containing the JSON files
directory_path = './data/'

# Initialize an empty list to store the combined JSON data
combined_data = []

# Iterate over the range of file numbers from 11 to 55
for i in range(1101, 9999):
    # Construct the file path for each file
    file_path = os.path.join(directory_path, str(i)[:2], f"{i}.json")

    # Check if the file exists
    if os.path.exists(file_path):
        # Open and load JSON data from the file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

            # Extend the combined_data list with the loaded JSON data
            combined_data.extend(json_data)

# Write the combined data to merged.json
with open(directory_path + 'kecamatan.json', 'w') as merged_file:
    json.dump(combined_data, merged_file)

print("Merged JSON data has been written to kecamatan.json.")
