"""
File: modules/manage_kamar.py
Deskripsi: Handler CLI untuk menampilkan data kamar dan mengelola keterisian kamar.
Tujuan: Menyediakan fungsi melihat kamar, melihat ketersediaan, serta sinkronisasi pasien-kamar.
Catatan penting: Perubahan disimpan langsung ke data/kamar.json dan data/pasien.json.
Relasi: Menggunakan models.kamar.Kamar dan utils.json_handler untuk load/save JSON.
"""

from models.kamar import Kamar
from utils.json_handler import load_json, save_json

def lihat_kamar():
    """Menampilkan seluruh data kamar dari file JSON."""
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


def lihat_kamar_tersedia():
    """Menampilkan daftar kamar yang masih memiliki kapasitas kosong."""
    data_kamar_dict = load_json("data/kamar.json")

    daftar_objek_kamar = []
    for data in data_kamar_dict:
        kamar_obj = Kamar.from_dict(data)
        daftar_objek_kamar.append(kamar_obj)

    print("\n--- KAMAR TERSEDIA ---")
    ditemukan = False
    for kamar in daftar_objek_kamar:
        if kamar.status_kamar() != "Penuh":
            print(kamar.data_kamar())
            ditemukan = True

    if not ditemukan:
        print("Tidak ada kamar tersedia.")

    print("-" * 32)


def assign_pasien_ke_kamar():
    """Menempatkan pasien ke kamar dan memperbarui data JSON."""
    data_kamar = load_json("data/kamar.json")
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK pasien: ").strip()
    nomor_kamar = input("Masukkan nomor kamar: ").strip()

    pasien_data = None
    for pasien in data_pasien:
        if pasien.get("nik") == nik:
            pasien_data = pasien
            break

    if pasien_data is None:
        print("Pasien tidak ditemukan.")
        return

    if pasien_data.get("nomor_kamar"):
        if pasien_data.get("nomor_kamar") == nomor_kamar:
            print("Pasien sudah berada di kamar tersebut.")
        else:
            print(f"Pasien sudah terdaftar di kamar {pasien_data.get('nomor_kamar')}.")
        return

    kamar_data = None
    for kamar in data_kamar:
        if kamar.get("nomor") == nomor_kamar:
            kamar_data = kamar
            break

    if kamar_data is None:
        print("Kamar tidak ditemukan.")
        return

    kamar_obj = Kamar.from_dict(kamar_data)
    if nik in kamar_obj.pasien_terisi:
        print("Pasien sudah tercatat di kamar ini.")
        return

    if not kamar_obj.pasien_masuk(nik):
        return

    pasien_data["nomor_kamar"] = nomor_kamar
    pasien_data["status"] = "dirawat"

    kamar_data.update(kamar_obj.to_dict())
    save_json("data/kamar.json", data_kamar)
    save_json("data/pasien.json", data_pasien)

    print(f"Pasien {nik} berhasil ditempatkan ke kamar {nomor_kamar}.")


def pasien_keluar_kamar():
    """Mengeluarkan pasien dari kamar dan memperbarui data JSON."""
    data_kamar = load_json("data/kamar.json")
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK pasien: ").strip()

    pasien_data = None
    for pasien in data_pasien:
        if pasien.get("nik") == nik:
            pasien_data = pasien
            break

    if pasien_data is None:
        print("Pasien tidak ditemukan.")
        return

    nomor_kamar = pasien_data.get("nomor_kamar")
    if not nomor_kamar:
        print("Pasien tidak tercatat di kamar.")
        return

    kamar_data = None
    for kamar in data_kamar:
        if kamar.get("nomor") == nomor_kamar:
            kamar_data = kamar
            break

    if kamar_data is None:
        print("Kamar tidak ditemukan.")
        return

    kamar_obj = Kamar.from_dict(kamar_data)
    if nik not in kamar_obj.pasien_terisi:
        print("Pasien tidak ditemukan di kamar ini.")
        return

    kamar_obj.pasien_keluar(nik)

    pasien_data["nomor_kamar"] = None
    pasien_data["status"] = "terdaftar"

    kamar_data.update(kamar_obj.to_dict())
    save_json("data/kamar.json", data_kamar)
    save_json("data/pasien.json", data_pasien)

    print(f"Pasien {nik} berhasil keluar dari kamar {nomor_kamar}.")
    