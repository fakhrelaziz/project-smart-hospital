"""
File    : modules/searching.py
Materi  : Searching — Linear Search dan Binary Search
Deskripsi:
    Menyediakan fungsi pencarian data pasien menggunakan dua algoritma:
    1. Linear Search  — mencari pasien berdasarkan nama (tidak harus terurut)
    2. Binary Search  — mencari pasien berdasarkan NIK (data harus terurut dulu)
    Serta fungsi filter pasien berdasarkan kategori layanan.
Catatan :
    - Linear Search  : O(n)      — cek satu per satu dari awal sampai akhir
    - Binary Search  : O(log n)  — bagi dua area pencarian setiap iterasi
    - Binary Search diimplementasikan MANUAL (tanpa modul bisect bawaan Python)
    - Semua pencarian nama bersifat case-insensitive (tidak peka huruf besar/kecil)
Relasi  :
    - Membaca data dari data/pasien.json via utils.json_handler
    - Menggunakan models.pasien.Pasien untuk konversi dict → objek
"""

from models.pasien import Pasien
from utils.json_handler import load_json


# ── HELPER: LOAD SEMUA PASIEN SEBAGAI OBJEK ──────────────────────────────────

def _load_daftar_pasien():
    """
    Membaca pasien.json dan mengembalikan list objek Pasien.
    Fungsi internal — diawali _ karena hanya dipakai di dalam file ini.

    Returns:
        list: List objek Pasien. List kosong jika file bermasalah.
    """
    data_dict = load_json("data/pasien.json")
    daftar = []
    for data in data_dict:
        p = Pasien("", "", 0, "")
        p.dict_ke_objek(data)
        daftar.append(p)
    return daftar


# ── HELPER: TAMPILKAN HASIL PENCARIAN ────────────────────────────────────────

def _tampilkan_hasil(daftar_hasil, keyword=""):
    """
    Menampilkan list objek Pasien hasil pencarian ke terminal.

    Args:
        daftar_hasil (list): List objek Pasien yang akan ditampilkan.
        keyword      (str) : Kata kunci yang dipakai saat pencarian (opsional).
    """
    if not daftar_hasil:
        if keyword:
            print(f"\n  [INFO] Tidak ada pasien yang cocok dengan '{keyword}'.")
        else:
            print("\n  [INFO] Tidak ada data yang ditemukan.")
        return

    print(f"\n  Ditemukan: {len(daftar_hasil)} pasien")
    print("  " + "─" * 60)
    for pasien in daftar_hasil:
        print(f"  NIK          : {pasien.nik}")
        print(f"  Nama         : {pasien.nama}")
        print(f"  Umur         : {pasien.umur} tahun")
        print(f"  Layanan      : {pasien.jenis_layanan}")
        print(f"  Status       : {pasien.status}")
        print(f"  Danger Score : {pasien.danger_score}")
        print(f"  Kamar        : {pasien.kamar if pasien.kamar else '-'}")
        print("  " + "─" * 60)


# ── 1. LINEAR SEARCH — CARI PASIEN BERDASARKAN NAMA ──────────────────────────

def linear_search_nama(daftar_pasien, keyword):
    """
    Mencari pasien yang namanya mengandung keyword menggunakan Linear Search.

    Cara kerja:
        Loop seluruh list dari index 0 sampai akhir.
        Setiap pasien dicek apakah keyword ada di dalam namanya.
        Semua pasien yang cocok dikumpulkan ke list hasil.
        Tidak berhenti di hasil pertama — mengembalikan SEMUA yang cocok.

    Kompleksitas: O(n) — harus cek setiap elemen satu per satu.

    Args:
        daftar_pasien (list): List objek Pasien yang akan dicari.
        keyword       (str) : Kata kunci nama yang dicari (case-insensitive).

    Returns:
        list: List objek Pasien yang namanya mengandung keyword.
              List kosong jika tidak ada yang cocok.
    """
    hasil = []
    keyword_lower = keyword.lower()   # ubah ke huruf kecil untuk perbandingan

    # Loop dari index 0 sampai akhir — inilah Linear Search
    for pasien in daftar_pasien:
        # Cek apakah keyword ada di dalam nama pasien (case-insensitive)
        if keyword_lower in pasien.nama.lower():
            hasil.append(pasien)

    return hasil


# ── 2. BINARY SEARCH — CARI PASIEN BERDASARKAN NIK ───────────────────────────

def _urutkan_by_nik(daftar_pasien):
    """
    Mengurutkan list pasien berdasarkan NIK secara ascending (A→Z).
    Menggunakan Bubble Sort manual agar konsisten dengan sorting_triase.py.

    Binary Search MEMBUTUHKAN data yang sudah terurut — ini pra-syaratnya.

    Args:
        daftar_pasien (list): List objek Pasien.

    Returns:
        list: List objek Pasien terurut ascending by NIK.
    """
    n = len(daftar_pasien)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if daftar_pasien[j].nik > daftar_pasien[j + 1].nik:
                daftar_pasien[j], daftar_pasien[j + 1] = \
                    daftar_pasien[j + 1], daftar_pasien[j]
    return daftar_pasien


def binary_search_nik(daftar_pasien, target_nik):
    """
    Mencari satu pasien berdasarkan NIK menggunakan Binary Search.

    Cara kerja:
        1. Pastikan list sudah terurut ascending by NIK (dilakukan di dalam fungsi ini)
        2. Set low = 0 (index paling kiri), high = len-1 (index paling kanan)
        3. Hitung mid = (low + high) // 2 (tengah)
        4. Bandingkan NIK di index mid dengan target_nik:
           - Sama      → DITEMUKAN, return pasien
           - Lebih kecil → target ada di kanan, set low  = mid + 1
           - Lebih besar → target ada di kiri,  set high = mid - 1
        5. Ulangi sampai ditemukan atau low > high (tidak ada)

    Kompleksitas: O(log n) — setiap iterasi membuang separuh data.

    Args:
        daftar_pasien (list): List objek Pasien (belum harus terurut).
        target_nik    (str) : NIK pasien yang dicari (16 digit).

    Returns:
        Pasien | None: Objek Pasien jika ditemukan, None jika tidak ada.
    """
    # Urutkan dulu berdasarkan NIK — syarat wajib Binary Search
    daftar_terurut = _urutkan_by_nik(daftar_pasien[:])  # copy agar list asli tidak berubah

    low  = 0
    high = len(daftar_terurut) - 1

    # Loop selama area pencarian masih valid
    while low <= high:

        # Hitung index tengah
        mid = (low + high) // 2

        nik_mid = daftar_terurut[mid].nik

        if nik_mid == target_nik:
            # DITEMUKAN — kembalikan objek pasien
            return daftar_terurut[mid]

        elif nik_mid < target_nik:
            # NIK target ada di KANAN — buang separuh kiri
            low = mid + 1

        else:
            # NIK target ada di KIRI — buang separuh kanan
            high = mid - 1

    # Jika loop selesai tanpa return → tidak ditemukan
    return None


# ── 3. FILTER BERDASARKAN LAYANAN ────────────────────────────────────────────

def filter_layanan(daftar_pasien, layanan):
    """
    Memfilter pasien berdasarkan jenis layanan menggunakan Linear Search.

    Args:
        daftar_pasien (list): List objek Pasien.
        layanan       (str) : Kategori layanan ("UGD", "Rawat Inap", "Rawat Jalan").

    Returns:
        list: List objek Pasien yang layanannya sesuai.
    """
    hasil = []
    layanan_lower = layanan.lower()

    for pasien in daftar_pasien:
        if pasien.jenis_layanan.lower() == layanan_lower:
            hasil.append(pasien)

    return hasil


# ── FUNGSI CLI — DIPANGGIL DARI main.py ──────────────────────────────────────

def cari_pasien_nama():
    """
    Entry point untuk pencarian pasien by nama via CLI.
    Menggunakan Linear Search.
    Dipanggil dari main.py saat pengguna memilih menu cari pasien.
    """
    print("\n" + "=" * 44)
    print("     CARI PASIEN BERDASARKAN NAMA")
    print("     Algoritma: Linear Search O(n)")
    print("=" * 44)

    keyword = input("  Masukkan nama (atau sebagian): ").strip()
    if not keyword:
        print("  [ERROR] Keyword tidak boleh kosong.")
        return

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  [INFO] Belum ada data pasien.")
        return

    print(f"\n  Mencari '{keyword}' dari {len(daftar_pasien)} data pasien...")

    hasil = linear_search_nama(daftar_pasien, keyword)
    _tampilkan_hasil(hasil, keyword)


def cari_pasien_nik():
    """
    Entry point untuk pencarian pasien by NIK via CLI.
    Menggunakan Binary Search.
    Dipanggil dari main.py saat pengguna memilih menu cari pasien by NIK.
    """
    print("\n" + "=" * 44)
    print("      CARI PASIEN BERDASARKAN NIK")
    print("     Algoritma: Binary Search O(log n)")
    print("=" * 44)

    nik = input("  Masukkan NIK (16 digit): ").strip()
    if not nik:
        print("  [ERROR] NIK tidak boleh kosong.")
        return

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  [INFO] Belum ada data pasien.")
        return

    print(f"\n  Mencari NIK '{nik}'...")

    hasil = binary_search_nik(daftar_pasien, nik)

    if hasil:
        _tampilkan_hasil([hasil])
    else:
        print(f"\n  [INFO] Pasien dengan NIK '{nik}' tidak ditemukan.")


def cari_pasien_layanan():
    """
    Entry point untuk filter pasien berdasarkan jenis layanan via CLI.
    Menggunakan Linear Search (filter).
    Dipanggil dari main.py.
    """
    # Tuple kategori layanan — sesuai dengan implementasi di proyek
    KATEGORI_LAYANAN = ("UGD", "Rawat Inap", "Rawat Jalan")

    print("\n" + "=" * 44)
    print("    FILTER PASIEN BERDASARKAN LAYANAN")
    print("=" * 44)
    print("  Pilih kategori layanan:")
    for i, kat in enumerate(KATEGORI_LAYANAN, 1):
        print(f"    [{i}] {kat}")

    while True:
        try:
            pilih = int(input("  Pilih [1/2/3]: ").strip())
            if 1 <= pilih <= len(KATEGORI_LAYANAN):
                layanan = KATEGORI_LAYANAN[pilih - 1]
                break
            print("  [ERROR] Pilih angka 1, 2, atau 3.")
        except ValueError:
            print("  [ERROR] Input harus berupa angka.")

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  [INFO] Belum ada data pasien.")
        return

    print(f"\n  Menampilkan pasien dengan layanan '{layanan}'...")

    hasil = filter_layanan(daftar_pasien, layanan)
    _tampilkan_hasil(hasil, layanan)


# ── TEST MANDIRI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  TEST MANDIRI — modules/searching.py")
    print("=" * 55)

    # Data dummy untuk test (tidak bergantung file JSON)
    data_dummy = [
        {"nik": "3201010101010006", "nama": "John Doe",        "umur": 40, "layanan": "UGD",        "status": "terdaftar", "danger_score": 10, "nomor_kamar": None, "rekam_medis": []},
        {"nik": "3201010101010001", "nama": "Albert Edison",   "umur": 35, "layanan": "UGD",        "status": "terdaftar", "danger_score": 0,  "nomor_kamar": None, "rekam_medis": []},
        {"nik": "3201010101010002", "nama": "Olivia Rodriguez","umur": 28, "layanan": "Rawat Jalan","status": "terdaftar", "danger_score": 0,  "nomor_kamar": None, "rekam_medis": []},
        {"nik": "3201010101010003", "nama": "Sabrina Carpenter","umur":45, "layanan": "Rawat Inap", "status": "terdaftar", "danger_score": 0,  "nomor_kamar": "K102","rekam_medis": []},
        {"nik": "3201010101010004", "nama": "Michael Johnson", "umur": 35, "layanan": "UGD",        "status": "terdaftar", "danger_score": 5,  "nomor_kamar": None, "rekam_medis": []},
        {"nik": "3201010101010005", "nama": "Emily Davis",     "umur": 22, "layanan": "Rawat Jalan","status": "terdaftar", "danger_score": 0,  "nomor_kamar": None, "rekam_medis": []},
        {"nik": "3201010101010007", "nama": "Jhonccena",       "umur": 45, "layanan": "Rawat Jalan","status": "terdaftar", "danger_score": 0,  "nomor_kamar": None, "rekam_medis": []},
    ]

    daftar = []
    for d in data_dummy:
        p = Pasien("", "", 0, "")
        p.dict_ke_objek(d)
        daftar.append(p)

    # ── Test 1: Linear Search — keyword ada ──────────────────────────────
    print("\n[TEST 1] Linear Search — keyword 'john' (harus cocok 2 pasien)")
    print("─" * 55)
    hasil = linear_search_nama(daftar, "john")
    print(f"  Ditemukan: {len(hasil)} pasien")
    for p in hasil:
        print(f"    → {p.nama} (NIK: {p.nik})")
    assert len(hasil) == 2, f"GAGAL: Harusnya 2, dapat {len(hasil)}"
    print("  ✅ Linear Search menemukan 2 pasien yang mengandung 'john'")

    # ── Test 2: Linear Search — case-insensitive ──────────────────────────
    print("\n[TEST 2] Linear Search — keyword 'ALBERT' (huruf kapital)")
    print("─" * 55)
    hasil2 = linear_search_nama(daftar, "ALBERT")
    print(f"  Ditemukan: {len(hasil2)} pasien")
    for p in hasil2:
        print(f"    → {p.nama}")
    assert len(hasil2) == 1
    assert hasil2[0].nama == "Albert Edison"
    print("  ✅ Case-insensitive berfungsi dengan benar")

    # ── Test 3: Linear Search — keyword tidak ada ─────────────────────────
    print("\n[TEST 3] Linear Search — keyword 'Budi' (tidak ada)")
    print("─" * 55)
    hasil3 = linear_search_nama(daftar, "Budi")
    print(f"  Ditemukan: {len(hasil3)} pasien")
    assert len(hasil3) == 0
    print("  ✅ Mengembalikan list kosong jika tidak ditemukan")

    # ── Test 4: Binary Search — NIK ada ──────────────────────────────────
    print("\n[TEST 4] Binary Search — NIK '3201010101010004' (ada)")
    print("─" * 55)
    target = "3201010101010004"
    hasil4 = binary_search_nik(daftar, target)
    print(f"  Hasil: {hasil4.nama if hasil4 else 'Tidak ditemukan'}")
    assert hasil4 is not None
    assert hasil4.nik == target
    assert hasil4.nama == "Michael Johnson"
    print("  ✅ Binary Search menemukan pasien yang benar")

    # ── Test 5: Binary Search — NIK tidak ada ────────────────────────────
    print("\n[TEST 5] Binary Search — NIK '9999999999999999' (tidak ada)")
    print("─" * 55)
    hasil5 = binary_search_nik(daftar, "9999999999999999")
    print(f"  Hasil: {hasil5}")
    assert hasil5 is None
    print("  ✅ Mengembalikan None jika NIK tidak ditemukan")

    # ── Test 6: Binary Search — NIK pertama dan terakhir ─────────────────
    print("\n[TEST 6] Binary Search — edge case: NIK terkecil dan terbesar")
    print("─" * 55)
    hasil6a = binary_search_nik(daftar, "3201010101010001")  # terkecil
    hasil6b = binary_search_nik(daftar, "3201010101010007")  # terbesar
    assert hasil6a is not None and hasil6a.nama == "Albert Edison"
    assert hasil6b is not None and hasil6b.nama == "Jhonccena"
    print(f"  NIK terkecil → {hasil6a.nama} ✅")
    print(f"  NIK terbesar → {hasil6b.nama} ✅")

    # ── Test 7: Filter layanan — UGD ─────────────────────────────────────
    print("\n[TEST 7] Filter layanan 'UGD'")
    print("─" * 55)
    hasil7 = filter_layanan(daftar, "UGD")
    print(f"  Ditemukan: {len(hasil7)} pasien UGD")
    for p in hasil7:
        print(f"    → {p.nama}")
    assert len(hasil7) == 3
    print("  ✅ Filter UGD mengembalikan 3 pasien yang benar")

    # ── Test 8: Filter layanan — case-insensitive ─────────────────────────
    print("\n[TEST 8] Filter layanan 'rawat jalan' (huruf kecil semua)")
    print("─" * 55)
    hasil8 = filter_layanan(daftar, "rawat jalan")
    print(f"  Ditemukan: {len(hasil8)} pasien")
    assert len(hasil8) == 3
    print("  ✅ Filter case-insensitive berfungsi")

    # ── Test 9: Data nyata dari JSON ──────────────────────────────────────
    print("\n[TEST 9] Cari nama 'johnson' dari data nyata pasien.json")
    print("─" * 55)
    daftar_nyata = _load_daftar_pasien()
    hasil9 = linear_search_nama(daftar_nyata, "johnson")
    print(f"  Ditemukan: {len(hasil9)} pasien")
    for p in hasil9:
        print(f"    → {p.nama} (NIK: {p.nik})")
    _tampilkan_hasil(hasil9, "johnson")

    print("\n" + "=" * 55)
    print("  SEMUA TEST SELESAI ✅")
    print("=" * 55)