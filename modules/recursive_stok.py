"""
Menghitung estimasi sisa hari pemakaian stok obat menggunakan
fungsi rekursif. Program memanggil dirinya sendiri berulang kali,
mengurangi stok sebesar pemakaian_harian setiap panggilan, hingga
mencapai base case (stok <= 0).
"""

from models.obat import Obat
from utils.json_handler import load_json


def hitung_sisa_hari(stok, pemakaian_harian, hari=0):

    # base case
    if stok <= 0:
        return hari

    # recursive case
    return hitung_sisa_hari(stok - pemakaian_harian, pemakaian_harian, hari + 1)


def prediksi_stok_obat(nama_obat, stok, pemakaian_harian):
    """
    Memanggil fungsi hitung_sisa_hari untuk menghitung prediksi sisa hari stok obat berdasarkan 
    rata rata rumah sakit memakai obat dari farmasi per harinya.
    """
    sisa_hari = None
    
    if pemakaian_harian <= 0:
        peringatan = "Pemakaian harian harus lebih dari 0."
    else:
        sisa_hari = hitung_sisa_hari(stok, pemakaian_harian)

        # peringatan berdasarkan sisa hari
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
        "pemakaian_harian": pemakaian_harian,
        "sisa_hari"   : sisa_hari,
        "peringatan"  : peringatan
    }


def tampilkan_hasil_prediksi(hasil):
    """fungsi di pakai pada fitur cari obat"""
    print("\n" + "=" * 48)
    print("       HASIL PREDIKSI STOK OBAT")
    print("=" * 48)

    if hasil["sisa_hari"] is None:
        print(f"  ERROR: {hasil['peringatan']}")
        print("=" * 48)
        return

    print(f"  Obat         : {hasil['nama']}")
    print(f"  Stok saat ini: {hasil['stok']} unit")
    print(f"  Pemakaian harian : {hasil['pemakaian_harian']} stok per hari")
    print("  " + "─" * 44)
    print(f"  Estimasi habis dalam: {hasil['sisa_hari']} hari")

    if hasil["peringatan"]:
        print(f"\n  {hasil['peringatan']}")

    print("=" * 48)


def prediksi_semua_obat():
    print("\n  " + "=" * 72)
    print("  " + "PREDIKSI STOK SEMUA OBAT".center(72))
    print("  " + "=" * 72)

    data_dict = load_json("data/obat.json")

    if not data_dict:
        print("  Belum ada data obat.")
        return

    # Hitung prediksi untuk setiap obat
    semua_hasil = []
    for data in data_dict:
        obat = Obat("", "", "", 0, 0, 0)
        obat.dict_ke_objek(data)
        hasil = prediksi_stok_obat(obat.nama, obat.stok, obat.pemakaian_harian)
        semua_hasil.append(hasil)

    # Tampilkan ringkasan tabel
    print(f"\n  {'Nama Obat':<24} | {'Stok':>6} | {'Pemakaian/hr':>12} | {'Sisa Hari':>9} | {'Status'}")
    print("  " + "─" * 72)

    for h in semua_hasil:

        if h["sisa_hari"] is not None:
            sisa = str(h["sisa_hari"])
        else:
            "ERR"

        if h["sisa_hari"] is None:
            status = "ERROR DOSIS"
        elif h["sisa_hari"] == 0:
            status = "HABIS"
        elif h["sisa_hari"] <= 3:
            status = "KRITIS"
        elif h["sisa_hari"] <= 7:
            status = "PERHATIAN"
        elif h["sisa_hari"] <= 14:
            status = "CUKUP"
        else:
            status = "AMAN"

        nama = h["nama"][:23] if len(h["nama"]) > 23 else h["nama"]
        print(f"  {nama:<24} | {h['stok']:>6} | {h['pemakaian_harian']:>12} | {sisa:>9} | {status}")

    print("  " + "─" * 72)
    print(f"  Total: {len(semua_hasil)} jenis obat")

