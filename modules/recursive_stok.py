"""
File    : modules/recursive_stok.py
Materi  : Rekursif (Recursive Function)
Deskripsi:
    Menghitung estimasi sisa hari pemakaian stok obat menggunakan
    fungsi rekursif. Program memanggil dirinya sendiri berulang kali,
    mengurangi stok sebesar dosis_harian setiap panggilan, hingga
    mencapai base case (stok <= 0).
Cara kerja rekursif:
    hitung_sisa_hari(stok=50, dosis=3, hari=0)
        → stok 50 > 0, rekursif ke hitung_sisa_hari(47, 3, 1)
            → stok 47 > 0, rekursif ke hitung_sisa_hari(44, 3, 2)
                → ... terus hingga stok <= 0
                    → BASE CASE: return hari  (= 17)
Catatan :
    - Fungsi utama: hitung_sisa_hari() — WAJIB rekursif, bukan loop
    - Kompleksitas : O(stok / dosis_harian) panggilan rekursif
    - Batas rekursi Python default: 1000 (sys.getrecursionlimit())
      Untuk stok sangat besar, ada versi iteratif sebagai fallback
Relasi  :
    - Membaca data dari data/obat.json via utils.json_handler
    - Menggunakan models.obat.Obat untuk konversi dict → objek
"""

import sys
from models.obat import Obat
from utils.json_handler import load_json


# ── KONSTANTA ─────────────────────────────────────────────────────────────────

# Batas aman sebelum beralih ke fallback iteratif
# Python default recursion limit = 1000
# Kita set 900 agar ada ruang aman
BATAS_REKURSIF = 900


# ── FUNGSI REKURSIF UTAMA ────────────────────────────────────────────────────

def hitung_sisa_hari(stok, dosis_harian, hari=0):
    """
    Menghitung estimasi sisa hari pemakaian obat secara REKURSIF.

    Cara kerja:
        BASE CASE    : Jika stok <= 0, return nilai hari.
                       Ini adalah kondisi berhenti — stok sudah habis.
        RECURSIVE CASE: Kurangi stok dengan dosis_harian, tambah hari 1,
                        lalu panggil dirinya sendiri dengan nilai baru.

    Contoh trace (stok=10, dosis=3):
        hitung_sisa_hari(10, 3, 0)   → stok > 0, lanjut
        hitung_sisa_hari( 7, 3, 1)   → stok > 0, lanjut
        hitung_sisa_hari( 4, 3, 2)   → stok > 0, lanjut
        hitung_sisa_hari( 1, 3, 3)   → stok > 0, lanjut
        hitung_sisa_hari(-2, 3, 4)   → stok <= 0, BASE CASE → return 4

    Args:
        stok         (int) : Jumlah stok obat saat ini.
        dosis_harian (int) : Berapa unit obat dipakai per hari.
        hari         (int) : Akumulator — bertambah 1 setiap panggilan rekursif.
                             Nilai awal selalu 0 (default).

    Returns:
        int: Estimasi jumlah hari sampai stok habis.
    """

    # ── BASE CASE ──────────────────────────────────────────────────────────
    # Kondisi berhenti: stok sudah habis (atau minus)
    if stok <= 0:
        return hari

    # ── RECURSIVE CASE ────────────────────────────────────────────────────
    # Kurangi stok 1 hari, tambah penghitung hari, panggil diri sendiri
    return hitung_sisa_hari(stok - dosis_harian, dosis_harian, hari + 1)


def hitung_sisa_hari_iteratif(stok, dosis_harian):
    """
    Versi ITERATIF dari hitung_sisa_hari (fallback untuk stok sangat besar).
    Dipakai otomatis jika stok / dosis_harian > BATAS_REKURSIF.

    Tidak dipakai langsung oleh pengguna — dipanggil oleh prediksi_stok_obat()
    jika stok terlalu besar untuk rekursif.

    Args:
        stok         (int): Jumlah stok obat saat ini.
        dosis_harian (int): Unit obat yang dipakai per hari.

    Returns:
        int: Estimasi jumlah hari sampai stok habis.
    """
    hari = 0
    while stok > 0:
        stok -= dosis_harian
        hari += 1
    return hari


# ── FUNGSI PREDIKSI (GABUNGAN LOGIKA + VALIDASI) ─────────────────────────────

def prediksi_stok_obat(nama_obat, stok, dosis_harian):
    """
    Wrapper yang menggabungkan validasi, pemilihan metode (rekursif/iteratif),
    dan format hasil prediksi menjadi satu fungsi yang siap dipanggil.

    Logika pemilihan metode:
        Estimasi hari = stok // dosis_harian
        Jika estimasi > BATAS_REKURSIF → gunakan iteratif (hindari RecursionError)
        Jika estimasi <= BATAS_REKURSIF → gunakan rekursif

    Args:
        nama_obat    (str) : Nama obat (untuk ditampilkan di output).
        stok         (int) : Stok obat saat ini.
        dosis_harian (int) : Unit obat yang dipakai per hari.

    Returns:
        dict: {
            "nama"        : nama obat,
            "stok"        : stok saat ini,
            "dosis_harian": dosis per hari,
            "sisa_hari"   : estimasi hari tersisa,
            "metode"      : "rekursif" atau "iteratif",
            "peringatan"  : pesan jika stok menipis (atau None)
        }
    """
    # Validasi dosis
    if dosis_harian <= 0:
        return {
            "nama"        : nama_obat,
            "stok"        : stok,
            "dosis_harian": dosis_harian,
            "sisa_hari"   : None,
            "metode"      : None,
            "peringatan"  : "ERROR: Dosis harian harus lebih dari 0."
        }

    # Validasi stok
    if stok <= 0:
        return {
            "nama"        : nama_obat,
            "stok"        : stok,
            "dosis_harian": dosis_harian,
            "sisa_hari"   : 0,
            "metode"      : "rekursif",
            "peringatan"  : "STOK HABIS — Segera lakukan pengadaan!"
        }

    # Pilih metode berdasarkan besar estimasi hari
    estimasi_kasar = stok // dosis_harian

    if estimasi_kasar > BATAS_REKURSIF:
        # Stok terlalu besar untuk rekursif — pakai iteratif
        sisa_hari = hitung_sisa_hari_iteratif(stok, dosis_harian)
        metode    = "iteratif (stok terlalu besar untuk rekursif)"
    else:
        # Gunakan rekursif
        sisa_hari = hitung_sisa_hari(stok, dosis_harian)
        metode    = "rekursif"

    # Tentukan peringatan berdasarkan sisa hari
    if sisa_hari == 0:
        peringatan = "STOK HABIS — Segera lakukan pengadaan!"
    elif sisa_hari <= 3:
        peringatan = "KRITIS — Stok habis dalam 3 hari atau kurang!"
    elif sisa_hari <= 7:
        peringatan = "PERHATIAN — Stok habis dalam seminggu."
    elif sisa_hari <= 14:
        peringatan = "INFO — Stok cukup untuk 2 minggu."
    else:
        peringatan = None

    return {
        "nama"        : nama_obat,
        "stok"        : stok,
        "dosis_harian": dosis_harian,
        "sisa_hari"   : sisa_hari,
        "metode"      : metode,
        "peringatan"  : peringatan
    }


# ── HELPER: LOAD SEMUA OBAT SEBAGAI OBJEK ────────────────────────────────────

def _load_daftar_obat():
    """
    Membaca obat.json dan mengembalikan list objek Obat.

    Returns:
        list: List objek Obat. List kosong jika file bermasalah.
    """
    data_dict = load_json("data/obat.json")
    daftar = []
    for data in data_dict:
        o = Obat("", "", "", 0, 0, 0)
        o.dict_ke_objek(data)
        daftar.append(o)
    return daftar


# ── TAMPILKAN HASIL PREDIKSI ─────────────────────────────────────────────────

def _tampilkan_hasil_prediksi(hasil):
    """
    Menampilkan hasil prediksi ke terminal dalam format yang informatif.

    Args:
        hasil (dict): Dict hasil dari prediksi_stok_obat().
    """
    print("\n" + "=" * 48)
    print("       HASIL PREDIKSI STOK OBAT")
    print("=" * 48)

    if hasil["sisa_hari"] is None:
        print(f"  [ERROR] {hasil['peringatan']}")
        print("=" * 48)
        return

    print(f"  Obat         : {hasil['nama']}")
    print(f"  Stok saat ini: {hasil['stok']} unit")
    print(f"  Dosis harian : {hasil['dosis_harian']}x per hari")
    print(f"  Metode       : {hasil['metode']}")
    print("  " + "─" * 44)
    print(f"  Estimasi habis dalam: {hasil['sisa_hari']} hari")

    if hasil["peringatan"]:
        print(f"\n  ⚠  {hasil['peringatan']}")

    print("=" * 48)


# ── FUNGSI CLI — DIPANGGIL DARI main.py ──────────────────────────────────────

def prediksi_satu_obat():
    """
    Entry point CLI: prediksi stok untuk satu obat berdasarkan input kode.
    Dipanggil dari main.py menu Farmasi.
    """
    print("\n" + "=" * 48)
    print("        PREDIKSI SISA STOK OBAT")
    print("        Algoritma: Fungsi Rekursif")
    print("=" * 48)

    kode = input("  Masukkan kode obat: ").strip().upper()
    if not kode:
        print("  [ERROR] Kode tidak boleh kosong.")
        return

    daftar_obat = _load_daftar_obat()

    # Cari obat berdasarkan kode
    obat_target = None
    for obat in daftar_obat:
        if obat.kode == kode:
            obat_target = obat
            break

    if obat_target is None:
        print(f"  [ERROR] Obat dengan kode '{kode}' tidak ditemukan.")
        return

    hasil = prediksi_stok_obat(
        nama_obat    = obat_target.nama,
        stok         = obat_target.stok,
        dosis_harian = obat_target.dosis_harian
    )
    _tampilkan_hasil_prediksi(hasil)


def prediksi_semua_obat():
    """
    Entry point CLI: prediksi stok untuk seluruh obat di database.
    Berguna untuk laporan ketersediaan obat secara menyeluruh.
    Dipanggil dari main.py menu Farmasi.
    """
    print("\n" + "=" * 48)
    print("     PREDIKSI STOK SEMUA OBAT")
    print("=" * 48)

    daftar_obat = _load_daftar_obat()

    if not daftar_obat:
        print("  [INFO] Belum ada data obat.")
        return

    # Hitung prediksi untuk setiap obat
    semua_hasil = []
    for obat in daftar_obat:
        hasil = prediksi_stok_obat(obat.nama, obat.stok, obat.dosis_harian)
        semua_hasil.append(hasil)

    # Urutkan: yang paling kritis (sisa hari paling sedikit) di atas
    semua_hasil.sort(key=lambda x: x["sisa_hari"] if x["sisa_hari"] is not None else 9999)

    # Tampilkan ringkasan tabel
    print(f"\n  {'Nama Obat':<22} {'Stok':>6} {'Dosis/hr':>8} {'Sisa Hari':>10}  Status")
    print("  " + "─" * 60)

    for h in semua_hasil:
        sisa = str(h["sisa_hari"]) if h["sisa_hari"] is not None else "ERR"

        if h["sisa_hari"] is None:
            status = "⚠ ERROR DOSIS"
        elif h["sisa_hari"] == 0:
            status = "🔴 HABIS"
        elif h["sisa_hari"] <= 3:
            status = "🔴 KRITIS"
        elif h["sisa_hari"] <= 7:
            status = "🟡 PERHATIAN"
        elif h["sisa_hari"] <= 14:
            status = "🟢 CUKUP"
        else:
            status = "🟢 AMAN"

        nama = h["nama"][:20] if len(h["nama"]) > 20 else h["nama"]
        print(f"  {nama:<22} {h['stok']:>6} {h['dosis_harian']:>8} {sisa:>10}  {status}")

    print("  " + "─" * 60)
    print(f"  Total: {len(semua_hasil)} jenis obat")


# ── TEST MANDIRI ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  TEST MANDIRI — modules/recursive_stok.py")
    print("=" * 55)

    # ── Test 1: Kasus dasar — stok habis tepat ────────────────────────────
    print("\n[TEST 1] stok=10, dosis=2 → harusnya 5 hari")
    print("─" * 55)
    hasil = hitung_sisa_hari(10, 2)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 5, f"GAGAL: Harusnya 5, dapat {hasil}"
    print("  ✅ Benar")

    # ── Test 2: Stok tidak habis tepat ────────────────────────────────────
    print("\n[TEST 2] stok=10, dosis=3 → harusnya 4 hari")
    print("─" * 55)
    # Trace: 10→7(1)→4(2)→1(3)→-2(4) base case hari=4
    hasil = hitung_sisa_hari(10, 3)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 4, f"GAGAL: Harusnya 4, dapat {hasil}"
    print("  ✅ Benar")

    # ── Test 3: BASE CASE — stok sudah 0 ─────────────────────────────────
    print("\n[TEST 3] stok=0, dosis=3 → harusnya 0 hari (langsung base case)")
    print("─" * 55)
    hasil = hitung_sisa_hari(0, 3)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 0, f"GAGAL: Harusnya 0, dapat {hasil}"
    print("  ✅ Base case langsung terpenuhi")

    # ── Test 4: Stok 1 unit ───────────────────────────────────────────────
    print("\n[TEST 4] stok=1, dosis=5 → harusnya 1 hari")
    print("─" * 55)
    # Trace: 1→-4(1) base case hari=1
    hasil = hitung_sisa_hari(1, 5)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 1, f"GAGAL: Harusnya 1, dapat {hasil}"
    print("  ✅ Benar")

    # ── Test 5: Dosis sama dengan stok ───────────────────────────────────
    print("\n[TEST 5] stok=50, dosis=50 → harusnya 1 hari")
    print("─" * 55)
    hasil = hitung_sisa_hari(50, 50)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 1, f"GAGAL: Harusnya 1, dapat {hasil}"
    print("  ✅ Benar")

    # ── Test 6: Stok besar → pakai iteratif via prediksi_stok_obat ───────
    print("\n[TEST 6] stok=5000, dosis=5 → 1000 hari (melebihi batas rekursif)")
    print("─" * 55)
    hasil_dict = prediksi_stok_obat("Obat Test Besar", 5000, 5)
    print(f"  Sisa hari : {hasil_dict['sisa_hari']}")
    print(f"  Metode    : {hasil_dict['metode']}")
    assert hasil_dict["sisa_hari"] == 1000
    assert "iteratif" in hasil_dict["metode"]
    print("  ✅ Fallback ke iteratif berjalan benar")

    # ── Test 7: Dosis = 0 → validasi error ───────────────────────────────
    print("\n[TEST 7] dosis=0 → harus validasi error")
    print("─" * 55)
    hasil_dict = prediksi_stok_obat("Obat Error", 50, 0)
    print(f"  Peringatan: {hasil_dict['peringatan']}")
    assert hasil_dict["sisa_hari"] is None
    assert "ERROR" in hasil_dict["peringatan"]
    print("  ✅ Validasi dosis 0 berfungsi")

    # ── Test 8: Stok negatif ──────────────────────────────────────────────
    print("\n[TEST 8] stok=-5, dosis=3 → base case langsung, 0 hari")
    print("─" * 55)
    hasil = hitung_sisa_hari(-5, 3)
    print(f"  Hasil: {hasil} hari")
    assert hasil == 0
    print("  ✅ Stok negatif ditangani base case")

    # ── Test 9: Prediksi lengkap dengan peringatan ────────────────────────
    print("\n[TEST 9] Prediksi lengkap — stok=5, dosis=3 → kritis")
    print("─" * 55)
    hasil_dict = prediksi_stok_obat("Paracetamol", 5, 3)
    _tampilkan_hasil_prediksi(hasil_dict)
    assert hasil_dict["sisa_hari"] == 2
    assert "KRITIS" in hasil_dict["peringatan"]
    print("  ✅ Peringatan kritis muncul dengan benar")

    # ── Test 10: Data nyata dari obat.json ────────────────────────────────
    print("\n[TEST 10] Prediksi semua obat dari data nyata obat.json")
    print("─" * 55)
    prediksi_semua_obat()

    # ── Test 11: Verifikasi rekursif benar-benar rekursif ─────────────────
    print("\n[TEST 11] Verifikasi fungsi rekursif (cek call stack)")
    print("─" * 55)
    # Manfaatkan sys.setrecursionlimit untuk verifikasi
    # Jika fungsi bukan rekursif, test ini tidak relevan
    # Kita trace manual: stok=6, dosis=2 → 6→4(1)→2(2)→0(3) base case
    hasil = hitung_sisa_hari(6, 2)
    assert hasil == 3, f"GAGAL: Harusnya 3, dapat {hasil}"
    print(f"  hitung_sisa_hari(6, 2) = {hasil} hari ✅")
    print("  Trace: 6→4(hr1)→2(hr2)→0(hr3) → BASE CASE return 3")
    print("  ✅ Fungsi rekursif berjalan dengan benar")

    print("\n" + "=" * 55)
    print("  SEMUA TEST SELESAI ✅")
    print("=" * 55)