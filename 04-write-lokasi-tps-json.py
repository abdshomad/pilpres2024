# Writing 04-tps.json
import json
import os

# Define the directory containing the JSON files
directory_path = './data/'

# Initialize an empty list to store the combined JSON data
combined_data = []

print('Creating ', directory_path + '04-tps.json')

# Iterate over the range of file numbers from 11 to 55
for kode_tps in range(3671071008000, 3671071008999): # 3671071008
    # Construct the file path for each file

    kode_tps = str(kode_tps)
    kode_propinsi = kode_tps[:2]
    kode_kabupaten_kota = kode_tps[:4]
    kode_kecamatan = kode_tps[:6]
    kode_kelurahan = kode_tps[:8]
    kode_kecamatan_json_file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, f"{kode_kecamatan}.json")
    kelurahan_json_file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, kode_kecamatan, f"{kode_kelurahan}.json")
    tps_json_file_path = os.path.join(directory_path, kode_propinsi, kode_kabupaten_kota, kode_kecamatan, kode_kelurahan, f"{kode_tps}.json")
    print('kelurahan_json_file_path: ', kelurahan_json_file_path)
    print('tps_json_file_path: ', tps_json_file_path)

    # Check if the file exists
    if os.path.exists(kelurahan_json_file_path):
        # Open and load JSON data from the file
        print('Exist ', kelurahan_json_file_path)
        with open(kelurahan_json_file_path, 'r') as file:
            json_data = json.load(file)

            # Extend the combined_data list with the loaded JSON data
            combined_data.extend(json_data)

# Write the combined data to merged.json
with open(directory_path + '04-tps.json', 'w') as merged_file:
    json.dump(combined_data, merged_file)

print("Merged JSON data has been written to 04-tps.json.")
