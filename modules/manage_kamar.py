from models.kamar import Kamar
from utils.json_handler import load_json, save_json

def lihat_kamar():
    data_kamar_dict = load_json("data/kamar.json")
    
    # Mengubah data mentah (dict) menjadi barisan Objek Kamar
    daftar_objek_kamar = []
    for data in data_kamar_dict:
        kamar_obj = Kamar.from_dict(data)
        daftar_objek_kamar.append(kamar_obj)

    # Menampilkan data menggunakan fungsi dari class Kamar
    print("\n--- DAFTAR KAMAR RUMAH SAKIT ---")
    for kamar in daftar_objek_kamar:
        print(kamar.data_kamar())
    print("-" * 32)
