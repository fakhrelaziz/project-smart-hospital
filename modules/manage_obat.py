"""
File: modules/manage_obat.py
Deskripsi: Handler CLI untuk melihat dan mengubah data obat.
Tujuan: Menyediakan fungsi dasar manajemen obat berbasis JSON.
Catatan penting: Beberapa fungsi menunggu modul struktur data lain selesai.
Relasi: Menggunakan models.obat.Obat dan utils.json_handler untuk load/save JSON.
"""

from models.obat import Obat
from utils.json_handler import load_json, save_json
from modules.hash_obat import HashObat
from modules.tree_katalog import tampilkan_katalog, cari_obat_di_katalog, lihat_obat_per_kategori
from modules.recursive_stok import prediksi_satu_obat, prediksi_semua_obat

def lihat_obat():
    """Menampilkan seluruh data obat dari file JSON."""
    data_obat_dict = load_json("data/obat.json")

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
        print("─" * 42)

    print(f"  Total: {len(data_obat_dict)} jenis obat")

def tambah_obat():
    """Menambahkan obat baru ke data JSON."""
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


def ubah_stok_obat():
    """Mengubah stok obat berdasarkan kode obat."""
    data_obat = load_json("data/obat.json")

    kode = input("Masukkan kode obat: ").strip()
    aksi = input("Pilih aksi [1] Tambah [2] Kurang: ").strip()

    jumlah = int(input("Jumlah stok: "))

    obat_data = None
    for item in data_obat:
        if item.get("kode") == kode:
            obat_data = item
            break

    if obat_data is None:
        print("Kode obat tidak ditemukan.")
        return

    obat_obj = Obat("", "", "", 0, 0, 0)
    obat_obj.dict_ke_objek(obat_data)

    if aksi == "1":
        pesan = obat_obj.tambah_stok(jumlah)
    elif aksi == "2":
        pesan = obat_obj.kurang_stok(jumlah)
    else:
        print("Aksi tidak valid.")
        return

    obat_data.update(obat_obj.objek_ke_dict())
    save_json("data/obat.json", data_obat)

    print(pesan)


def ubah_harga_obat():
    """Mengubah harga obat berdasarkan kode obat."""
    data_obat = load_json("data/obat.json")

    kode = input("Masukkan kode obat: ").strip()
    harga_baru = int(input("Masukkan harga baru: "))

    obat_data = None
    for item in data_obat:
        if item.get("kode") == kode:
            obat_data = item
            break

    if obat_data is None:
        print("Kode obat tidak ditemukan.")
        return

    obat_obj = Obat("", "", "", 0, 0, 0)
    obat_obj.dict_ke_objek(obat_data)
    pesan = obat_obj.ubah_harga(harga_baru)

    obat_data.update(obat_obj.objek_ke_dict())
    save_json("data/obat.json", data_obat)

    print(pesan)


def cari_obat_kode():
    """Mencari obat menggunakan Hash Table (Algoritma Pencarian Cepat O(1))."""
    data_obat = load_json("data/obat.json")
    
    # Inisialisasi Hash Table dan populasi data dari JSON terkini
    hash_tabel = HashObat()
    for item in data_obat:
        hash_tabel.insert(item['kode'], item)
        
    print("\n--- PENCARIAN OBAT (HASH TABLE) ---")
    kode_cari = input("Masukkan Kode Obat secara spesifik (Contoh: OBT001): ").strip()
    
    hasil = hash_tabel.get(kode_cari)
    if hasil:
        print("\n[SUCCESS] Obat ditemukan dengan sangat cepat!")
        hash_tabel.cetak_obat(hasil)
    else:
        print(f"\n[ERROR] Obat dengan kode '{kode_cari}' tidak ditemukan di tabel hash.")


def prediksi_stok_habis():
    """Prediksi masa pakai stok menggunakan Algoritma Rekursif."""
    while True:
        print("\n--- PREDIKSI STOK OBAT (REKURSIF) ---")
        print("1. Prediksi Berapa Hari Semua Stok Obat Akan Habis")
        print("2. Prediksi 1 Obat Secara Spesifik")
        print("3. Kembali")
        
        pilihan = input("Pilih model komputasi: ")
        
        if pilihan == "1":
            prediksi_semua_obat()
        elif pilihan == "2":
            prediksi_satu_obat()
        elif pilihan == "3":
            break
        else:
            print("Pilihan invalid.")


def tampilkan_katalog_obat():
    """Menilik struktur hirarkis obat kategori -> sub -> item via Tree."""
    while True:
        print("\n--- KATALOG OBAT (DIREKTORI TREE) ---")
        print("1. Lihat Keseluruhan Pohon Direktori (Tree)")
        print("2. Cari Item Berdasarkan Level Terdalam (Tree Search DFS)")
        print("3. Filter Kategori Spesifik Saja")
        print("4. Kembali")
        
        pilihan = input("Pilih menu tree: ")
        
        if pilihan == "1":
            tampilkan_katalog()
        elif pilihan == "2":
            cari_obat_di_katalog()
        elif pilihan == "3":
            lihat_obat_per_kategori()
        elif pilihan == "4":
            break
        else:
            print("Pilihan invalid.")

