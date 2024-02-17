import json
import pandas as pd
import os
import wget

# Assuming '0.json' is in the 'data' directory
file_path = "data/0.json"

# Load JSON data from the file
with open(file_path, "r") as f:
    propinsi_json = json.load(f)

# Convert the JSON data into a Pandas DataFrame
propinsi_df = pd.DataFrame(propinsi_json)

# Display the DataFrame
print(propinsi_df)

directory_path = './data/'
for kode in propinsi_df['kode']:
    url = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/'+kode+'.json'
    file_path = os.path.join(directory_path, kode + '.json')
    if os.path.exists(file_path):
        print('File: ', file_path, ' Exists')
    else:
        filename = wget.download(url)
        print(f"File '{filename}' downloaded.")

# Define the directory containing the JSON files
directory_path = './data/'

# Initialize an empty list to store the combined JSON data
combined_data = []

# Iterate over the range of file numbers from 11 to 55
for i in range(11, 99):
    # Construct the file path for each file
    file_path = os.path.join(directory_path, f"{i}.json")

    # Check if the file exists
    if os.path.exists(file_path):
        # Open and load JSON data from the file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

            # Extend the combined_data list with the loaded JSON data
            combined_data.extend(json_data)

# Write the combined data to merged.json
with open(directory_path + 'kabupaten_kota.json', 'w') as merged_file:
    json.dump(combined_data, merged_file)

print("Merged JSON data has been written to kabupaten_kota.json.")
