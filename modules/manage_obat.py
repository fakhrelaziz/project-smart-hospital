from models.obat import Obat
from utils.json_handler import load_json, save_json

def lihat_obat():

    data_obat_dict= load_json("data/obat.json")

     # Mengubah data mentah (dict) menjadi barisan Objek Obat
    daftar_objek_obat = []
    for data in data_obat_dict:
        obat_obj = Obat("", "", "", 0, 0, 0)
        obat_obj.dict_ke_objek(data)
        daftar_objek_obat.append(obat_obj)

     # Menampilkan data menggunakan fungsi dari class Obat
    print("\n--- DAFTAR OBAT RUMAH SAKIT ---")
    for obat in daftar_objek_obat:
        print(obat.data_obat())
    print("-" * 32)

def tambah_obat():

    data_obat = load_json("data/obat.json")

    kode = input("Masukkan kode obat: ")
    nama = input("Masukkan nama: ")
    kategori = input("Masukkan kategori: ")
    stok = int(input("Berapa stok?:  "))
    harga = int(input("Harga: "))
    dosis_harian = int(input("Dosis harian: "))
     
    obat_baru = Obat(kode, nama, kategori, stok, harga, dosis_harian)

    data_obat.append(obat_baru.objek_ke_dict())

    save_json("data/obat.json", data_obat)

    print("Obat berhasil ditambahkan")