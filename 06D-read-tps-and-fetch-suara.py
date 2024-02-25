import duckdb
import os

# Connect to the DuckDB database file
con = duckdb.connect(database='pemilu2024-kpu-release.duckdb')

# Query the data
# result = con.execute("SELECT * FROM tps_data WHERE kode BETWEEN '3671071008000' AND '3671071008999' ORDER BY kode")
result = con.execute("SELECT * FROM tps_data ORDER BY kode")

# Fetch all rows from the result
rows = result.fetchall()

# Print the rows
# i = 0 
dirname_data = './data/'

with open("./data/05-tps-url.txt", "w") as file:

    for row in rows:
        # i = i + 1 
        # if i < 1000: 
        print(row)
        kode_tps = row[2]
        kode_propinsi       = kode_tps[:2]
        kode_kabupaten_kota = kode_tps[:4]
        kode_kecamatan      = kode_tps[:6]
        kode_kelurahan      = kode_tps[:10]
        kode_tps            = kode_tps[:13]
        url_kecamatan       = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_propinsi}/{kode_kabupaten_kota}/{kode_kecamatan}.json";
        url_kelurahan       = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_propinsi}/{kode_kabupaten_kota}/{kode_kecamatan}/{kode_kelurahan}.json";
        #                       https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/36/3671/367107/3671071008/3671071008003.json
        url_tps             = f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/{kode_propinsi}/{kode_kabupaten_kota}/{kode_kecamatan}/{kode_kelurahan}/{kode_tps}.json";
        dirname_kecamatan   = url_kecamatan.replace('.json', '').replace('https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/', dirname_data) # os.path.dirname(url_kelurahan)
        dirname_kelurahan   = url_kelurahan.replace('.json', '').replace('https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/', dirname_data) # os.path.dirname(url_tps)
        dirname_tps         = url_tps.replace('.json', '').replace('https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/', dirname_data) # os.path.dirname(url_tps)
        os.makedirs(dirname_kecamatan, exist_ok=True)
        os.makedirs(dirname_kelurahan, exist_ok=True)
        os.makedirs(dirname_tps, exist_ok=True)
        print("url_kecamatan", url_kecamatan)
        print("dirname_kecamatan", dirname_kecamatan)
        print("url_kelurahan", url_kelurahan)
        print("dirname_kelurahan", dirname_kelurahan)
        print("url_tps", url_tps)
        print("dirname_tps", dirname_tps)
        file.write(url_tps + "\n")

# Close the connection
con.close()
