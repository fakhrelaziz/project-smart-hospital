"""
File    : modules/sorting_triase.py
Materi  : Sorting — Bubble Sort manual
Deskripsi:
    Mengurutkan antrean pasien UGD berdasarkan danger_score secara descending
    (danger_score tertinggi = paling kritis = paling atas antrian).
Catatan :
    - Sorting diimplementasikan MANUAL menggunakan Bubble Sort.
    - Tidak menggunakan sorted() atau list.sort() bawaan Python.
    - Hanya memproses pasien dengan layanan == "UGD".
Relasi  :
    - Membaca data dari data/pasien.json via utils.json_handler.
    - Menggunakan models.pasien.Pasien untuk konversi dict → objek.
"""

from models.pasien import Pasien
from utils.json_handler import load_json, save_json
from modules.manage_pasien import global_stack


# ── LABEL KEGAWATAN ───────────────────────────────────────────────────────────

def label_kegawatan(danger_score):
    """
    Mengembalikan label kegawatan berdasarkan nilai danger_score.
    Digunakan saat menampilkan antrian UGD.

    Skala:
        8 - 10 → KRITIS
        5 - 7  → DARURAT
        1 - 4  → Ringan
        0      → Belum dinilai
    """
    if danger_score >= 8:
        return "[KRITIS] "
    elif danger_score >= 5:
        return "[DARURAT]"
    elif danger_score >= 1:
        return "[Ringan] "
    else:
        return "[Belum dinilai]"


# ── BUBBLE SORT MANUAL ────────────────────────────────────────────────────────

def bubble_sort_ugd(daftar_pasien):
    """
    Mengurutkan list objek Pasien berdasarkan danger_score secara descending
    menggunakan algoritma Bubble Sort yang diimplementasikan secara manual.

    Cara kerja Bubble Sort:
        - Loop luar  : berjalan sebanyak (n-1) kali
        - Loop dalam : membandingkan dua elemen bertetangga
        - Jika elemen kiri LEBIH KECIL dari kanan → tukar posisi (swap)
        - Setelah setiap putaran loop luar, elemen terbesar "menggelembung"
          ke posisi yang benar di ujung kanan
        - Ulangi sampai seluruh list terurut descending

    Kompleksitas: O(n²) — sesuai untuk jumlah pasien UGD yang tidak banyak.

    Args:
        daftar_pasien (list): List objek Pasien yang akan diurutkan.
                              List diubah IN-PLACE (langsung di list aslinya).

    Returns:
        list: List objek Pasien yang sudah terurut descending by danger_score.
    """
    n = len(daftar_pasien)

    # Loop luar — sebanyak n-1 putaran
    for i in range(n - 1):

        # Loop dalam — bandingkan elemen bertetangga
        # Setiap putaran loop luar, elemen terbesar sudah di posisi akhir
        # jadi tidak perlu cek sampai ujung lagi (n - 1 - i)
        for j in range(n - 1 - i):

            # Bandingkan danger_score dua pasien bertetangga
            # Jika pasien[j] LEBIH KECIL dari pasien[j+1] → tukar
            # (kita ingin descending, jadi yang BESAR harus di kiri/depan)
            if daftar_pasien[j].danger_score < daftar_pasien[j + 1].danger_score:

                # SWAP — tukar posisi dua elemen
                daftar_pasien[j], daftar_pasien[j + 1] = daftar_pasien[j + 1], daftar_pasien[j]

    return daftar_pasien


# ── AMBIL PASIEN UGD ─────────────────────────────────────────────────────────

def ambil_pasien_ugd():
    """
    Membaca data pasien dari JSON, filter hanya yang layanan == "UGD",
    lalu konversi setiap dict menjadi objek Pasien.

    Returns:
        list: List objek Pasien dengan layanan UGD.
              List kosong jika tidak ada pasien UGD.
    """
    data_semua = load_json("data/pasien.json")

    daftar_ugd = []
    for data in data_semua:
        if data.get("layanan") == "UGD":
            pasien_obj = Pasien("", "", 0, "")
            pasien_obj.dict_ke_objek(data)
            daftar_ugd.append(pasien_obj)

    return daftar_ugd


# ── TAMPILKAN ANTRIAN UGD ────────────────────────────────────────────────────

def tampilkan_antrian_ugd(daftar_pasien_terurut):
    """
    Menampilkan daftar antrian UGD yang sudah terurut dalam format tabel CLI.
    Pasien dengan danger_score tertinggi tampil di urutan paling atas.

    Args:
        daftar_pasien_terurut (list): List objek Pasien yang sudah diurutkan
                                      oleh bubble_sort_ugd().
    """
    print("\n" + "=" * 68)
    print("           ANTRIAN UGD — TERURUT BERDASARKAN PRIORITAS")
    print("=" * 68)

    if not daftar_pasien_terurut:
        print("  [INFO] Tidak ada pasien UGD saat ini.")
        print("=" * 68)
        return

    # Header tabel
    print(f"  {'No.':<4} {'NIK':<18} {'Nama':<20} {'Score':<7} {'Status'}")
    print("  " + "─" * 64)

    # Baris data
    for urutan, pasien in enumerate(daftar_pasien_terurut, start=1):
        label  = label_kegawatan(pasien.danger_score)
        nama   = pasien.nama[:18] if len(pasien.nama) > 18 else pasien.nama
        print(f"  {urutan:<4} {pasien.nik:<18} {nama:<20} {pasien.danger_score:<7} {label}")

    print("=" * 68)
    print(f"  Total pasien UGD: {len(daftar_pasien_terurut)} orang")


# ── UPDATE DANGER SCORE ───────────────────────────────────────────────────────

def update_danger_score():
    """
    Memperbarui danger_score pasien UGD berdasarkan input NIK.
    Perubahan langsung disimpan ke data/pasien.json.

    Alur:
        1. Tampilkan antrian UGD saat ini
        2. Input NIK pasien yang ingin diperbarui
        3. Input nilai danger_score baru (1-10)
        4. Simpan perubahan ke JSON
    """
    # Tampilkan antrian dulu agar petugas tahu siapa saja yang ada
    lihat_antrian_ugd()

    data_semua = load_json("data/pasien.json")

    print("\n--- UPDATE DANGER SCORE ---")
    nik = input("Masukkan NIK pasien UGD: ").strip()

    # Cari pasien berdasarkan NIK
    pasien_data = None
    pasien_index = None
    for i, data in enumerate(data_semua):
        if data.get("nik") == nik:
            pasien_data  = data
            pasien_index = i
            break

    if pasien_data is None:
        print(f"[ERROR] Pasien dengan NIK '{nik}' tidak ditemukan.")
        return

    if pasien_data.get("layanan") != "UGD":
        print(f"[ERROR] Pasien '{pasien_data['nama']}' bukan pasien UGD.")
        return

    print(f"[OK] Pasien ditemukan: {pasien_data['nama']}")
    print(f"     Danger score saat ini: {pasien_data['danger_score']}")

    # Input danger score baru dengan validasi
    while True:
        try:
            score_baru = int(input("Masukkan danger score baru (1-10): "))
            if 1 <= score_baru <= 10:
                break
            else:
                print("[ERROR] Nilai harus antara 1 dan 10.")
        except ValueError:
            print("[ERROR] Input harus berupa angka.")

    # Update dan simpan
    score_lama = data_semua[pasien_index]["danger_score"]
    data_semua[pasien_index]["danger_score"] = score_baru
    save_json("data/pasien.json", data_semua)
    
    # Simpan ke histori Stack untuk keperluan Undo
    global_stack.tambah_aksi({
        "tipe_aksi": "triase",
        "nik": nik,
        "skor_lama": score_lama,
        "skor_baru": score_baru,
        "keterangan": "Update danger score triase UGD"
    })

    print(f"[OK] Danger score {pasien_data['nama']} diperbarui: {score_lama} → {score_baru}")
    print(f"     Status kegawatan: {label_kegawatan(score_baru)}")


# ── Batal Skor Triase Terakhir (Undo) ────────────────────────────────────────────────
def undo_skor_triase_terakhir():
    """Membatalkan (Undo) proses update skor triase menggunakan Stack LIFO."""
    aksi = global_stack.batalkan_aksi()
    
    if not aksi:
        return

    # Validasi hanya memproses undo tipe triase dari menu ini
    if aksi.get("tipe_aksi") != "triase":
        print(f"[ERROR] Aksi terakhir bukan triase (Melainkan: {aksi.get('tipe_aksi')}). Harus di-undo dari modul yang sesuai.")
        # Kembalikan lagi ke stack
        global_stack.tambah_aksi(aksi)
        return

    nik_target = aksi["nik"]
    skor_lama = aksi["skor_lama"]
    data_semua = load_json("data/pasien.json")
    
    # Cari dan pulihkan
    pasien_ditemukan = False
    for data in data_semua:
        if data.get("nik") == nik_target:
            data["danger_score"] = skor_lama
            pasien_ditemukan = True
            break
            
    if pasien_ditemukan:
        save_json("data/pasien.json", data_semua)
        print(f"[SUCCESS] Danger score NIK {nik_target} berhasil di-restore ke nilai awal: {skor_lama}.")
    else:
        print(f"[ERROR] Data pasien NIK {nik_target} tidak ditemukan, gagal undo.")


# ── LIHAT ANTRIAN UGD (ENTRY POINT UTAMA) ────────────────────────────────────

def lihat_antrian_ugd():
    """
    Fungsi utama yang dipanggil dari main.py.
    Mengambil pasien UGD, mengurutkan dengan Bubble Sort,
    lalu menampilkan hasilnya.
    """
    daftar_ugd = ambil_pasien_ugd()
    daftar_terurut = bubble_sort_ugd(daftar_ugd)
    tampilkan_antrian_ugd(daftar_terurut)


# ── TEST MANDIRI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  TEST MANDIRI — modules/sorting_triase.py")
    print("=" * 50)

    # ── Test 1: Bubble Sort dengan data dummy ─────────────────────────────
    print("\n[TEST 1] Bubble Sort manual dengan data dummy")
    print("─" * 50)

    # Buat list pasien dummy dengan danger_score acak
    data_dummy = [
        {"nik": "0001", "nama": "Pasien A", "umur": 30,
         "layanan": "UGD", "status": "terdaftar", "danger_score": 3,
         "nomor_kamar": None, "rekam_medis": []},
        {"nik": "0002", "nama": "Pasien B", "umur": 25,
         "layanan": "UGD", "status": "terdaftar", "danger_score": 9,
         "nomor_kamar": None, "rekam_medis": []},
        {"nik": "0003", "nama": "Pasien C", "umur": 50,
         "layanan": "UGD", "status": "terdaftar", "danger_score": 1,
         "nomor_kamar": None, "rekam_medis": []},
        {"nik": "0004", "nama": "Pasien D", "umur": 40,
         "layanan": "UGD", "status": "terdaftar", "danger_score": 7,
         "nomor_kamar": None, "rekam_medis": []},
        {"nik": "0005", "nama": "Pasien E", "umur": 60,
         "layanan": "UGD", "status": "terdaftar", "danger_score": 10,
         "nomor_kamar": None, "rekam_medis": []},
    ]

    # Konversi ke objek Pasien
    daftar_test = []
    for d in data_dummy:
        p = Pasien("", "", 0, "")
        p.dict_ke_objek(d)
        daftar_test.append(p)

    # Tampilkan sebelum sorting
    print("Sebelum sorting:")
    for p in daftar_test:
        print(f"  {p.nama} — danger_score: {p.danger_score}")

    # Jalankan Bubble Sort
    bubble_sort_ugd(daftar_test)

    # Tampilkan setelah sorting
    print("\nSetelah Bubble Sort (descending):")
    for p in daftar_test:
        print(f"  {p.nama} — danger_score: {p.danger_score} {label_kegawatan(p.danger_score)}")

    # Verifikasi urutan benar
    scores = [p.danger_score for p in daftar_test]
    assert scores == sorted(scores, reverse=True), "GAGAL: Urutan tidak descending!"
    print("\n✅ Bubble Sort menghasilkan urutan yang benar (descending).")

    # ── Test 2: List kosong ───────────────────────────────────────────────
    print("\n[TEST 2] Bubble Sort dengan list kosong")
    print("─" * 50)
    hasil_kosong = bubble_sort_ugd([])
    assert hasil_kosong == [], "GAGAL: List kosong harus tetap kosong!"
    print("  Hasil: [] ✅ Tidak error.")

    # ── Test 3: List 1 elemen ─────────────────────────────────────────────
    print("\n[TEST 3] Bubble Sort dengan 1 pasien")
    print("─" * 50)
    satu = Pasien("", "", 0, "")
    satu.dict_ke_objek(data_dummy[0])
    hasil_satu = bubble_sort_ugd([satu])
    assert len(hasil_satu) == 1
    print(f"  Hasil: [{hasil_satu[0].nama}] ✅ Tidak error.")

    # ── Test 4: Data nyata dari JSON ──────────────────────────────────────
    print("\n[TEST 4] Ambil dan tampilkan data nyata dari pasien.json")
    print("─" * 50)
    lihat_antrian_ugd()

    # ── Test 5: Label kegawatan ───────────────────────────────────────────
    print("\n[TEST 5] Label kegawatan")
    print("─" * 50)
    for score in [0, 1, 4, 5, 7, 8, 10]:
        print(f"  Score {score:>2} → {label_kegawatan(score)}")

    print("\n" + "=" * 50)
    print("  SEMUA TEST SELESAI ✅")
    print("=" * 50)