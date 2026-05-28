from models.pasien import Pasien
from utils.json_handler import load_json, save_json

def lihat_pasien():

    data_pasien_dict = load_json("data/pasien.json")

    # Mengubah data mentah (dict) menjadi barisan Objek Pasien
    daftar_objek_pasien = []
    for data in data_pasien_dict:
        pasien_obj = Pasien("", "", 0, "")
        pasien_obj.dict_ke_objek(data)
        daftar_objek_pasien.append(pasien_obj)

    # Menampilkan data menggunakan fungsi dari class Pasien
    print("\n--- DAFTAR PASIEN RUMAH SAKIT ---")
    for pasien in daftar_objek_pasien:
        print("-" * 40)
        print(pasien.data_pasien())
    print("-" * 40)

# fungsi untuk menambah pasien baru ke data JSON
def tambah_pasien():
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK: ")

    # validasi NIK
    for pasien in data_pasien:
        if pasien["nik"] == nik:
            print("NIK sudah terdaftar")
            return

    nama = input("Masukkan Nama: ")
    # error handling untuk input umur, memastikan hanya angka yang diterima
    while True:
        try:
            umur = int(input("Masukkan umur: "))
            break

        except ValueError:
            print("Umur harus angka!")
    layanan = input("Masukkan Layanan: ")
    
    # membuat objek pasien baru dengan data yang di input user
    pasien_baru = Pasien(nik, nama, umur, layanan)

    data_pasien.append(pasien_baru.objek_ke_dict())
    
    # menyimpan data pasien yang sudah diperbarui ke file JSON
    save_json("data/pasien.json", data_pasien)

    print("Pasien berhasil ditambahkan")


def sub_menu_pendaftaran(queue_pendaftaran, stack_undo, set_nik, dict_pasien):
    while True:
        print("\n=== PENDAFTARAN PASIEN ===")
        print("  [1] Daftar Pasien Baru")
        print("  [2] Proses Antrian Loket")
        print("  [3] Lihat Antrian Saat Ini")
        print("  [4] Undo Pendaftaran Terakhir")
        print("  [0] Kembali ke Menu Utama")
        pilihan = input(">>> Pilih menu: ")

        if pilihan == "1":
            daftar_pasien_baru(queue_pendaftaran, stack_undo, set_nik, dict_pasien)
        elif pilihan == "2":
            proses_antrian(queue_pendaftaran, dict_pasien)
        elif pilihan == "3":
            lihat_antrian(queue_pendaftaran)
        elif pilihan == "4":
            undo_pendaftaran(queue_pendaftaran, stack_undo, set_nik, dict_pasien)
        elif pilihan == "0":
            break
        else:
            print("[ERROR] Pilihan tidak valid.")