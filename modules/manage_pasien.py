"""
File    : modules/manage_pasien.py
Deskripsi: Antarmuka CLI untuk manajemen antrian dan daftar pasien Smart Hospital.
Tujuan  : Menyediakan operasi interaktif terminal untuk pasien yang dikombinasikan
           dengan antrean pendaftaran (Queue) dan riwayat aksi (Stack).
Catatan :
    - Menggunakan struktur data Queue manual (QueuePendaftaran) untuk alur pasien 'antri'.
    - Menggunakan Stack manual (Stack_UGD) untuk keperluan Undo pendaftaran.
    - Rekam medis disimpan menggunakan Single Linked List (sll_rekammedis.py).
    - Data disimpan per-operasi langsung ke data/pasien.json.
Relasi  :
    - models.pasien.Pasien
    - utils.json_handler.load_json / save_json
    - modules.queue_pendaftaran.QueuePendaftaran
    - modules.stack_ugd.Stack_UGD
    - modules.sll_rekammedis.SingleLinkedListRekamMedis
"""

from models.pasien import Pasien
from utils.json_handler import load_json, save_json
from modules.queue_pendaftaran import QueuePendaftaran
from modules.stack_ugd import Stack_UGD
from modules.sll_rekammedis import SingleLinkedListRekamMedis

# Instansiasi objek struktur data secara global per eksekusi modul
global_queue = QueuePendaftaran()
global_stack = Stack_UGD()


# ── HELPER INTERNAL ───────────────────────────────────────────────────────────

def _load_data_ke_queue(data_pasien: list):
    """Helper untuk memuat ulang pasien yang statusnya 'antri' ke dalam struktur Queue."""
    global_queue._items.clear()
    antrian = [p for p in data_pasien if p.get("status") == "antri"]
    global_queue.from_list(antrian)


# ── DAFTAR PASIEN BARU ────────────────────────────────────────────────────────

def daftar_pasien_baru():
    """Mendaftar pasien secara FIFO (masuk ke antrean belakang)."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)

    nik = input("Masukkan NIK: ").strip()

    # Validasi: cegah duplikasi NIK
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
            print("[ERROR] Umur harus berupa angka.")

    layanan = input("Masukkan Layanan (UGD / Rawat Inap / Rawat Jalan): ").strip()
    if not layanan:
        layanan = "Umum"

    # Buat objek Pasien dan masukkan ke antrian
    pasien_baru = Pasien(nik, nama, umur, layanan)
    pasien_baru.status = "antri"
    p_dict = pasien_baru.objek_ke_dict()

    berhasil = global_queue.enqueue(p_dict)

    if berhasil:
        data_pasien.append(p_dict)
        save_json("data/pasien.json", data_pasien)

        # Simpan ke histori Stack untuk keperluan Undo
        global_stack.tambah_aksi({
            "tipe_aksi": "pendaftaran",
            "nik": nik,
            "keterangan": "Pendaftaran pasien baru"
        })


# ── PROSES ANTRIAN PENDAFTARAN ────────────────────────────────────────────────

def proses_antrian_pendaftaran():
    """Mengeksekusi Queue Dequeue pada pasien paling depan, status berubah 'terdaftar'."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)

    pasien_diproses = global_queue.dequeue()

    if pasien_diproses:
        # Refleksikan status baru ke master data
        for master_p in data_pasien:
            if master_p["nik"] == pasien_diproses["nik"]:
                master_p["status"] = "terdaftar"
                break

        save_json("data/pasien.json", data_pasien)


# ── LIHAT ANTRIAN PENDAFTARAN ─────────────────────────────────────────────────

def lihat_antrian_pendaftaran():
    """Menampilkan line up Queue Pendaftaran di layar tanpa memanipulasi datanya."""
    data_pasien = load_json("data/pasien.json")
    _load_data_ke_queue(data_pasien)
    global_queue.tampilkan_antrian()


# ── UNDO PENDAFTARAN ──────────────────────────────────────────────────────────

def undo_pendaftaran_terakhir():
    """Membatalkan (Undo) proses pendaftaran terakhir menggunakan Stack LIFO."""
    aksi = global_stack.batalkan_aksi()

    if not aksi:
        return

    # Validasi: hanya proses undo tipe pendaftaran
    if aksi.get("tipe_aksi") != "pendaftaran":
        print(f"[ERROR] Aksi terakhir bukan pendaftaran ('{aksi.get('tipe_aksi')}'). Harus di-undo dari modul yang sesuai.")
        global_stack.tambah_aksi(aksi)
        return

    nik_target = aksi["nik"]
    data_pasien = load_json("data/pasien.json")

    data_awal_len = len(data_pasien)
    data_pasien = [p for p in data_pasien if p["nik"] != nik_target]

    if len(data_pasien) < data_awal_len:
        save_json("data/pasien.json", data_pasien)
        _load_data_ke_queue(data_pasien)
        print(f"[SUCCESS] Pendaftaran NIK {nik_target} berhasil dibatalkan.")
    else:
        print(f"[ERROR] NIK {nik_target} tidak ditemukan, gagal undo.")


# ── LIHAT SEMUA PASIEN ────────────────────────────────────────────────────────

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
        print("Sistem belum memiliki catatan pasien.")
    else:
        for pasien in daftar_objek_pasien:
            print("-" * 40)
            print(pasien.data_pasien())
    print("-" * 40)


# ── REKAM MEDIS — LIHAT ───────────────────────────────────────────────────────

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

    # Tampilkan setiap entri secara rapi
    saat_ini = sll.head
    nomor = 1
    while saat_ini is not None:
        catatan = saat_ini.data
        if isinstance(catatan, dict):
            print(f"  [{nomor}] Tanggal  : {catatan.get('tanggal', '-')}")
            print(f"       Diagnosis : {catatan.get('diagnosis', '-')}")
            print(f"       Resep     : {catatan.get('resep', '-')}")
        else:
            # Fallback untuk data lama yang masih berupa string
            print(f"  [{nomor}] {catatan}")
        print("  " + "-" * 38)
        saat_ini = saat_ini.next
        nomor += 1


# ── REKAM MEDIS — TAMBAH ──────────────────────────────────────────────────────

def tambah_catatan_rekam_medis():
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

    sll = SingleLinkedListRekamMedis()
    sll.from_list(pasien_target.get("rekam_medis", []))

    # Input terstruktur sesuai desain rekam medis
    print(f"\n--- TAMBAH CATATAN REKAM MEDIS: {pasien_target['nama']} ---")
    tanggal   = input("  Tanggal (DD-MM-YYYY) : ").strip()
    diagnosis = input("  Diagnosis            : ").strip()
    resep     = input("  Resep / Obat         : ").strip()

    catatan_baru = {
        "tanggal"  : tanggal,
        "diagnosis": diagnosis,
        "resep"    : resep
    }

    sll.tambah_riwayat(catatan_baru)

    # Simpan kembali ke JSON
    pasien_target["rekam_medis"] = sll.to_list()
    save_json("data/pasien.json", data_pasien)
    print(f"[SUCCESS] Catatan rekam medis berhasil ditambahkan untuk NIK {nik}.")
