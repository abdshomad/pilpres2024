import os
import wget

file_name = "0.json"
data_dir = "data"
file_path = os.path.join(data_dir, file_name)
url = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json"

if not os.path.exists(file_path):
    os.makedirs(data_dir, exist_ok=True)  # Create the data directory if it doesn't exist
    wget.download(url, file_path)
else:
    print(f"File {file_name} already exists in {data_dir}")
