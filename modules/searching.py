"""
Menyediakan fungsi pencarian data pasien menggunakan dua algoritma:
1. Linear Search  — mencari pasien berdasarkan nama (tidak harus terurut)
2. Binary Search  — mencari pasien berdasarkan NIK (data harus terurut dulu)
Serta fungsi filter pasien berdasarkan kategori layanan.
"""

from models.pasien import Pasien
from utils.json_handler import load_json

#fungsi yang sering dipanggil 
def _load_daftar_pasien():
    """
    Membaca pasien.json dan mengembalikan list objek Pasien.
    Fungsi internal — diawali _ karena hanya dipakai di dalam file ini.
    """
    data_dict = load_json("data/pasien.json")
    daftar = []
    for data in data_dict:
        p = Pasien()
        p.dict_ke_objek(data)
        daftar.append(p)
    return daftar

def _tampilkan_hasil(daftar_hasil, keyword=""):
    """Menampilkan list objek Pasien hasil pencarian."""
    if not daftar_hasil:
        if keyword:
            print(f"\n  Tidak ada pasien yang cocok dengan '{keyword}'.")
        else:
            print("\n  Tidak ada data yang ditemukan.")
        return

    print(f"\n  Pasien Ditemukan")
    print("  " + "─" * 30)
    for pasien in daftar_hasil:
        print(f"  NIK          : {pasien.nik}")
        print(f"  Nama         : {pasien.nama}")
        print(f"  Umur         : {pasien.umur} tahun")
        print(f"  Layanan      : {pasien.jenis_layanan}")
        print(f"  Status       : {pasien.status}")
        print(f"  Danger Score : {pasien.danger_score}")
        print(f"  Kamar        : {pasien.kamar if pasien.kamar else '-'}")
        print("  " + "─" * 30)


def linear_search_nama(daftar_pasien, keyword):
    hasil = []
    # ubah ke huruf kecil untuk perbandingan
    keyword_lower = keyword.lower() 

    # Loop dari index 0 sampai akhir 
    for pasien in daftar_pasien:
        # Proteksi nilai None
        nama_pasien = str(pasien.nama).lower() if pasien.nama else ""
        if keyword_lower in nama_pasien:
            hasil.append(pasien)

    return hasil


def _urutkan_by_nik(daftar_pasien):
    """Mengurutkan list pasien berdasarkan NIK secara ascending (A→Z) untuk implementasi Bubble Sort"""
    n = len(daftar_pasien)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            nik1 = str(daftar_pasien[j].nik) if daftar_pasien[j].nik else ""
            nik2 = str(daftar_pasien[j + 1].nik) if daftar_pasien[j + 1].nik else ""
            if nik1 > nik2:
                daftar_pasien[j], daftar_pasien[j + 1] = \
                    daftar_pasien[j + 1], daftar_pasien[j]
    return daftar_pasien


def binary_search_nik(daftar_pasien, target_nik):

    # Urutkan dulu berdasarkan NIK 
    # copy agar list asli tidak berubah, karena Binary Search butuh data terurut
    daftar_terurut = _urutkan_by_nik(daftar_pasien[:])

    low  = 0
    high = len(daftar_terurut) - 1

    # Loop selama area pencarian masih valid
    while low <= high:

        # Hitung index tengah
        mid = (low + high) // 2

        nik_mid = str(daftar_terurut[mid].nik) if daftar_terurut[mid].nik else ""

        if nik_mid == target_nik:
            return daftar_terurut[mid]

        elif nik_mid < target_nik:
            # NIK target ada di KANAN — buang separuh kiri
            low = mid + 1

        else:
            # NIK target ada di KIRI — buang separuh kanan
            high = mid - 1

    return None


def filter_layanan(daftar_pasien, layanan):
    """Memfilter pasien berdasarkan jenis layanan menggunakan Linear Search."""
    hasil = []
    layanan_lower = layanan.lower()

    for pasien in daftar_pasien:
        layanan_pasien = str(pasien.jenis_layanan).lower() if pasien.jenis_layanan else ""
        if layanan_pasien == layanan_lower:
            hasil.append(pasien)

    return hasil


def cari_pasien_nama():
    """untuk pencarian pasien by nama. Menggunakan Linear Search."""
    print("\n" + "=" * 44)
    print("     CARI PASIEN BERDASARKAN NAMA")
    print("=" * 44)

    keyword = input("  Masukkan nama (atau sebagian): ").strip()
    if not keyword:
        print("  Keyword tidak boleh kosong.")
        return

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  Belum ada data pasien.")
        return

    print(f"\n  Mencari '{keyword}' dari {len(daftar_pasien)} data pasien...")

    hasil = linear_search_nama(daftar_pasien, keyword)
    _tampilkan_hasil(hasil, keyword)


def cari_pasien_nik():
    """mencarian pasien by nik menggunakan Binary Search."""
    print("\n" + "=" * 44)
    print("      CARI PASIEN BERDASARKAN NIK")
    print("=" * 44)

    nik = input("  Masukkan NIK (6 digit): ").strip()
    if not nik:
        print("  ERROR: NIK tidak boleh kosong.")
        return

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  Belum ada data pasien.")
        return

    print(f"\n  Mencari NIK '{nik}'...")

    hasil = binary_search_nik(daftar_pasien, nik)

    if hasil:
        _tampilkan_hasil([hasil])
    else:
        print(f"\n  Pasien dengan NIK '{nik}' tidak ditemukan.")


def cari_pasien_layanan():
    """Entry point untuk filter pasien berdasarkan jenis layanan. Menggunakan Linear Search (filter)."""
    KATEGORI_LAYANAN = ("UGD", "Rawat Inap", "Rawat Jalan")

    print("\n" + "=" * 44)
    print("    FILTER PASIEN BERDASARKAN LAYANAN")
    print("=" * 44)
    print("  Pilih kategori layanan:")
    for i in range(len(KATEGORI_LAYANAN)):
        print(f"    [{i+1}] {KATEGORI_LAYANAN[i]}")

    while True:
        try:
            pilih = int(input("  Pilih [1/2/3]: ").strip())
            if 1 <= pilih <= len(KATEGORI_LAYANAN):
                layanan = KATEGORI_LAYANAN[pilih - 1]
                break
            print("  ERROR: Pilih angka 1, 2, atau 3.")
        except ValueError:
            print("  ERROR: Input harus berupa angka.")

    daftar_pasien = _load_daftar_pasien()

    if not daftar_pasien:
        print("  Belum ada data pasien.")
        return

    print(f"\n  Menampilkan pasien dengan layanan '{layanan}'...")

    hasil = filter_layanan(daftar_pasien, layanan)
    _tampilkan_hasil(hasil, layanan)
