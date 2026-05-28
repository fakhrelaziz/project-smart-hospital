"""
File       : modules/manage_pasien.py
Deskripsi  : Antarmuka CLI untuk manajemen antrian dan daftar pasien Smart Hospital.
Tujuan     : Menyediakan operasi interaktif terminal untuk pasien yang dikombinasikan dengan antrean pendaftaran.
Catatan    : 
             - Menggunakan struktur data Queue manual (QueuePendaftaran) untuk alur pasien 'antri'.
             - Fitur SLL, Tree, dll di-stubbing terlebih dahulu menunggu pengerjaan tim.
Relasi     :
             - models.pasien.Pasien
             - utils.json_handler
             - modules.queue_pendaftaran.QueuePendaftaran
"""
from models.pasien import Pasien
from utils.json_handler import load_json, save_json
from modules.queue_pendaftaran import QueuePendaftaran

# Instansiasi objek struktur data secara global per eksekusi modul
global_queue = QueuePendaftaran()

def _load_data_ke_queue(data_pasien: list):
    """Helper untuk memuat ulang pasien yang statusnya 'antri' ke dalam struktur Queue."""
    global_queue._items.clear()
    antrian = [p for p in data_pasien if p.get("status") == "antri"]
    global_queue.from_list(antrian)

def daftar_pasien_baru():
    """Mendaftar pasien secara FIFO (masuk ke antrean belakang)."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)

    nik = input("Masukkan NIK: ").strip()

    # Validasi mencegah duplikasi
    for pasien in data_pasien:
        if pasien["nik"] == nik:
            print("[INFO] NIK ini sudah ada di dalam sistem!")
            return

    nama = input("Masukkan Nama: ").strip()
    while True:
        try:
            umur = int(input("Masukkan Umur: ").strip())
            break
        except ValueError:
            print("[ERROR] Umur harus berupa angka (integer)!")
            
    layanan = input("Masukkan Layanan (UGD/Rawat Inap/Rawat Jalan): ").strip()
    if not layanan:
        layanan = "Umum"

    # Bikin Objek Models
    pasien_baru = Pasien(nik, nama, umur, layanan)
    # Tetapkan statis saat daftar defaultnya masuk ke dalam antrean pendaftaran
    pasien_baru.status = "antri"
    
    # Parsing Dict
    p_dict = pasien_baru.objek_ke_dict()

    # Eksekusi Queue Pendaftaran Enqueue
    berhasil = global_queue.enqueue(p_dict)
    
    if berhasil:
        data_pasien.append(p_dict)
        save_json("data/pasien.json", data_pasien)

def proses_antrian_pendaftaran():
    """Mengeksekusi Queue Dequeue pada pasien paling depan, status dari 'antri' otomatis berubah 'terdaftar'."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)

    pasien_diproses = global_queue.dequeue()
    
    if pasien_diproses:
        # Refleksikan status baru ke master data list
        for master_p in data_pasien:
            if master_p["nik"] == pasien_diproses["nik"]:
                master_p["status"] = "terdaftar"
                break
        
        save_json("data/pasien.json", data_pasien)

def lihat_antrian_pendaftaran():
    """Menampilkan line up Queue Pendaftaran di layar tanpa memanipulasi datanya."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)
    
    global_queue.tampilkan_antrian()

def undo_pendaftaran_terakhir():
    """Stub / Menunggu Modul Stack UGD/Lainnya yang akan membalikkan Undo (Pop)."""
    print("\n[INFO] Fitur Undo Pendaftaran Terakhir akan memakai struktur STACK.")
    print("       (Menunggu implementasi stack yang fix).")

def lihat_semua_pasien():
    """Menampilkan histori atau status semua pasien di database rumah sakit."""
    data_pasien_dict = load_json("data/pasien.json")

    daftar_objek_pasien = []
    for data in data_pasien_dict:
        pasien_obj = Pasien("", "", 0, "")
        pasien_obj.dict_ke_objek(data)
        daftar_objek_pasien.append(pasien_obj)

    print("\n--- DAFTAR KESELURUHAN PASIEN RUMAH SAKIT ---")
    if not daftar_objek_pasien:
        print("Sistem belum memiliki catatan riwayat pasien satupun.")
    else:
        for pasien in daftar_objek_pasien:
            print("-" * 40)
            print(pasien.data_pasien())
    print("-" * 40)
