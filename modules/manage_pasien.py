"""
business logic dari smart hospital untuk mengelola pasien, termasuk pendaftaran, triase, dan rekam medis.
Tujuan nya menyediakan operasi interaktif terminal validasi, menampilkan input/output
dengan memanggil stuktur data antrean (Queue) dan pembatalan pendaftaran dengan (Stack).
    - Menggunakan struktur data Queue manual (QueuePendaftaran) untuk alur pasien 'antri'.
    - Menggunakan Stack manual (Stack_UGD) untuk keperluan Undo pendaftaran.
    - Rekam medis disimpan menggunakan Single Linked List (sll_rekammedis.py).
    - Data disimpan per-operasi langsung ke data/pasien.json.
"""

from models.pasien import Pasien
from utils.json_handler import load_json, save_json
from modules.queue_pendaftaran import QueuePendaftaran
from modules.undo_stack import UndoStack 
from modules.sll_rekammedis import SingleLinkedListRekamMedis

def lihat_semua_pasien():
    """Menampilkan data semua pasien di database (json) rumah sakit."""
    data_pasien_dict = load_json("data/pasien.json")

    daftar_objek_pasien = []
    for data in data_pasien_dict:
        pasien_obj = Pasien()
        pasien_obj.dict_ke_objek(data)
        daftar_objek_pasien.append(pasien_obj)

    print("\n--- DAFTAR KESELURUHAN PASIEN RUMAH SAKIT ---")
    if not daftar_objek_pasien:
        print("Sistem belum memiliki catatan pasien.")
    else:
        for pasien in daftar_objek_pasien:
            print("-" * 40)
            print(pasien.data_pasien())
    print("-" * 40)


def daftar_pasien_baru(app_state):
    """Fungsi untuk mendaftar pasien baru yang dibuat dengan class Pasien kemudian dari objek diubah
    ke dictionary baru kemudian masuk ke antrian (queue)"""
    data_pasien = load_json("data/pasien.json")

    pasien_antri = [p for p in data_pasien if p.get("status") == "antri"]
    antrean = QueuePendaftaran(pasien_antri)

    while True:
        nik = input("Masukkan NIK (Wajib 6 Angka): ").strip()
        if nik.isdigit() and len(nik) == 6:
            break
        print("NIK harus berupa angka dan tepat 6 digit.")

    # Validasi nik sudah ada atau belum di data pasien
    for pasien in data_pasien:
        if pasien["nik"] == nik:
            print("NIK ini sudah ada di dalam sistem!")
            return

    nama = input("Masukkan Nama: ").strip()
    while True:
        try:
            umur = int(input("Masukkan Umur: ").strip())
            break
        except ValueError:
            print("Umur harus berupa angka.")

    while True:
        print(" Pilih Layanan:")
        print("    [1] UGD")
        print("    [2] Rawat Inap")
        print("    [3] Rawat Jalan")
        pilihan_layanan = input(" Pilih: ").strip()

        if pilihan_layanan == "1":
            layanan = "UGD"
            break
        elif pilihan_layanan == "2":
            layanan = "Rawat Inap"
            break
        elif pilihan_layanan == "3":
            layanan = "Rawat Jalan"
            break
        else:
            print("Masukkan pilihan 1-3")
            

    # Buat objek Pasien dan masukkan ke antrian
    pasien_baru = Pasien(nik, nama, umur, layanan)
    pasien_baru.status = "antri"
    p_dict = pasien_baru.objek_ke_dict()

    berhasil = antrean.enqueue(p_dict)

    if berhasil:
        data_pasien.append(p_dict)
        save_json("data/pasien.json", data_pasien)

        # Simpan ke data pasien baru Stack untuk keperluan Undo
        app_state.stack_pendaftaran.push({
            "nik": nik,
            "nama": nama
        })
 

def proses_antrian_pendaftaran():
    """pasien daftar pertama yang di layani kemudian status berubah selesai."""
    data_pasien = load_json("data/pasien.json")

    # Inisialisasi antrean lokal dengan data
    pasien_antri = [p for p in data_pasien if p.get("status") == "antri"]
    antrean = QueuePendaftaran(pasien_antri)

    pasien_diproses = antrean.dequeue()

    if pasien_diproses:
        # Refleksikan status baru ke master data
        for proses in data_pasien:
            if proses["nik"] == pasien_diproses["nik"]:
                pasien_obj = Pasien()
                pasien_obj.dict_ke_objek(proses)
                pasien_obj.update_status("diperiksa")
                proses.update(pasien_obj.objek_ke_dict())
                break

        save_json("data/pasien.json", data_pasien)


def lihat_antrian_pendaftaran():
    """Menampilkan line up Queue Pendaftaran di layar tanpa memanipulasi datanya."""
    data_pasien = load_json("data/pasien.json")

    # Inisialisasi antrean dengan data
    pasien_antri = [p for p in data_pasien if p.get("status") == "antri"]
    antrean = QueuePendaftaran(pasien_antri)

    print("\n--- ANTRIAN PENDAFTARAN LOKET ---")
    antrean.tampilkan_antrian()
    print("-" * 33)


def undo_pendaftaran_terakhir(app_state):
    if app_state.stack_pendaftaran.is_empty():
        print("[INFO] Tidak ada riwayat pendaftaran yang bisa dibatalkan.")
        return
    
    """Membatalkan (Undo) proses pendaftaran terakhir menggunakan Stack LIFO."""
    aksi_terakhir = app_state.stack_pendaftaran.pop()

    #mengambil nik dari pasien yang daftar terakhir untuk dihapus dari data pasien
    nik_batal = aksi_terakhir["nik"]
    daftar_pasien = load_json("data/pasien.json")
    
    jumlah_pasien_awal = len(daftar_pasien)
    daftar_pasien = [p for p in daftar_pasien if p["nik"] != nik_batal]

    if len(daftar_pasien) < jumlah_pasien_awal:
        save_json("data/pasien.json", daftar_pasien)
        print(f"[SUCCESS] Pendaftaran NIK {nik_batal} berhasil dibatalkan.")
    else:
        print(f"[ERROR] NIK {nik_batal} tidak ditemukan, gagal undo.")


def lihat_rekam_medis_pasien():
    """Melihat rekam medis pasien menggunakan Single Linked List (SLL)."""
    data_pasien = load_json("data/pasien.json")
    nik = input("Masukkan NIK pasien: ").strip()

    pasien_target = None
    for p in data_pasien:
        if p["nik"] == nik:
            pasien_target = p
            break

    if not pasien_target:
        print("[ERROR] Pasien tidak ditemukan.")
        return

    sll = SingleLinkedListRekamMedis()
    sll.from_list(pasien_target.get("rekam_medis", []))

    print(f"\n--- REKAM MEDIS: {pasien_target['nama']} ---")

    if sll.head is None:
        print("  Belum ada catatan rekam medis.")
        return

    # ngeprint rekam medis dengan format yang rapi
    saat_ini = sll.head
    nomor = 1
    while saat_ini is not None:
        catatan = saat_ini.data
        print(f"  [{nomor}] Tanggal  : {catatan.get('tanggal', '-')}")
        print(f"       Diagnosis : {catatan.get('diagnosis', '-')}")
        print(f"       Resep     : {catatan.get('resep', '-')}")
        print("  " + "-" * 38)
        saat_ini = saat_ini.next
        nomor += 1


def tambah_rekam_medis_pasien():
    """Menambah catatan rekam medis terstruktur menggunakan Single Linked List (SLL)."""
    data_pasien = load_json("data/pasien.json")
    nik = input("Masukkan NIK pasien: ").strip()

    pasien_target = None
    for p in data_pasien:
        if p["nik"] == nik:
            pasien_target = p
            break

    if not pasien_target:
        print("[ERROR] Pasien tidak ditemukan.")
        return

    # Pilihan 2: Menggunakan objek Pasien dari models
    pasien_obj = Pasien()
    pasien_obj.dict_ke_objek(pasien_target)

    # Input terstruktur sesuai desain rekam medis
    print(f"\n--- TAMBAH CATATAN REKAM MEDIS: {pasien_obj.nama} ---")
    while True:
        tanggal = input("  Tanggal (YYYY-MM-DD) : ").strip()
        parts = tanggal.split("-")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
            if len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2:
                break
        print("  [ERROR] Format tanggal harus berupa YYYY-MM-DD (Contoh: 2024-12-01).")
    diagnosis = input("  Diagnosis            : ").strip()
    resep     = input("  Resep / Obat         : ").strip()

    # Menggunakan method tingkat model Pasien
    pasien_obj.tambah_rekam_medis(tanggal, diagnosis, resep)

    # Muat ke dalam SLL untuk memenuhi syarat struktur data
    sll = SingleLinkedListRekamMedis()
    sll.from_list(pasien_obj.rekam_medis)

    # Update status via OOP
    pasien_obj.update_status("selesai")
    pasien_target.update(pasien_obj.objek_ke_dict())

    # Timpa atribut rekam_medis menggunakan versi SLL 
    pasien_target["rekam_medis"] = sll.to_list()
    save_json("data/pasien.json", data_pasien)
    print(f"[SUCCESS] Catatan rekam medis berhasil ditambahkan untuk NIK {nik}.")
