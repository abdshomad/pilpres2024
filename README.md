# pilpres2024
Dataset pilpres 2024

# Struktur Directory Data

| Direktori   | Deskripsi           |
| `/data/`   | Tempat menyimpan master data dalam format JSON. Data ini hanya berubah jika terdapat penambahan propinsi, kabupaten/kota, kecamatan, kelurahan/desa, atau TPS. |
| `/hasil-tps/` | Tempat menyimpan data hasil TPS dalam format JSON. Data ini bergerak mengikuti data hasil TPS yang sudah masuk ke sistem KPU. |
| `/images/` | Tempat menyimpan gambar C Plano hasil scan/foto. |

# Level di Struktur Directory `/data/`

| Tingkat  | Lokasi                                      | Keterangan                                     |
|----------|---------------------------------------------|------------------------------------------------|
| Level 0  | `./data/0.json`                             | JSON berisi daftar propinsi dan kodenya        |
| Level 1  | `./data/xx.json`                            | JSON tiap propinsi berisi daftar kabupaten/kota dan kodenya (xx) |
| Level 2  | `./data/xx/xxyy.json`                      | JSON tiap kabupaten/kota (xxyy) berisi daftar kecamatannya (xxyy) |
| Level 3  | `./data/xx/xxyy/xxyyzz.json`               | JSON tiap kecamatan (xxyy) berisi daftar kelurahannya (xxyyzz) |
| Level 4  | `./data/xx/xxyy/xxyyzz/xxyyzzaa.json`      | JSON tiap kelurahan (xxyyzz) berisi daftar TPSnya (xxyyzzaa) |
| Level 5  | `./data/xx/xxyy/xxyyzz/xxyyzzaa/xxyyzzaabb.json` | JSON tiap TPS (xxyyzzaa) berisi URL gambar C Plano |

# Git Clone 
git clone https://github.com/abdshomad/pilpres2024.git
cd pilpres2024

# Install 

## Rekomendasi: Install Anaconda / Miniconda. 
conda create --name pilpres python=3.11
conda activate pilpres 
pip install -r requirements.txt 

## Alternatif, gunakan venv 
Buat Virtual Env 
python3 -m venv myenv

Aktifkan Virtual Env 
Di windows: myenv\Scripts\activate
Di MacOS / Linux: source myenv/bin/activate

# Workflow Pengambilan Data 

| No. | Status       | Tindakan                                | Perintah                              |
|-----|--------------|-----------------------------------------|---------------------------------------|
| 1.  | DONE         | Download json propinsi                  | `python 00-get-provinsi-json.py`      |
| 2.  | DONE         | Download json kabupaten/kota            | `python 01-get-kabupaten-kota-json.py`|
| 3.  | DONE         | Download json kecamatan                 | `python 02-get-kecamatan-json.py`     |
| 4.  | DONE         | Download json kelurahan                 | `python 03-get-kelurahan-json.py`     |
| 5.  | DONE         | Download json tps                       | `python 04-get-lokasi-tps-json.py`           |
| 6.  | IN PROGRESS  | Download json hasil per TPS             | `python 05-get-json-hasil-per-tps.py` |
| 7.  | IN PROGRESS  | Download C Plano hasil per TPS          | `python 06-get-gambar-c-plano-per-tps.py`    |

# Simpan data di git 
git add .
git commit -m "Add data ... (sebutkan datanya)"
git push

# TODO 
* JSON data TPS must be check and refreshed. Indicator: images = [null, null, null]
* OCR AI C Plano : gunakan kawalc1 
* Script untuk upload C Plano ke www.kawalpemilu.org 
