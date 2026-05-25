"""
File: modules/manage_obat.py
Deskripsi: Handler CLI untuk melihat dan mengubah data obat.
Tujuan: Menyediakan fungsi dasar manajemen obat berbasis JSON.
Catatan penting: Beberapa fungsi menunggu modul struktur data lain selesai.
Relasi: Menggunakan models.obat.Obat dan utils.json_handler untuk load/save JSON.
"""

from models.obat import Obat
from utils.json_handler import load_json, save_json

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
    """Placeholder hingga modul hash_obat selesai."""
    pass


def prediksi_stok_habis():
    """Placeholder hingga modul recursive_stok selesai."""
    pass


def tampilkan_katalog_obat():
    """Placeholder hingga modul tree_katalog selesai."""
    pass

