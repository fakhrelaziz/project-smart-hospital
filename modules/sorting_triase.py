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
from modules.undo_stack import UndoStack

# variabel untuk menampung undo khusus update danger score
stack_triase = UndoStack()


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
    # Tampilkan antrian dulu agar tahu siapa saja yang ada
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
    stack_triase.append({
        "nik": nik,
        "skor_lama": score_lama
    })

    print(f"[OK] Danger score {pasien_data['nama']} diperbarui: {score_lama} → {score_baru}")
    print(f"     Status kegawatan: {label_kegawatan(score_baru)}")


def undo_danger_score():
    if stack_triase.is_empty():
        print("[INFO] Tidak ada riwayat triase yang bisa dibatalkan.")
        return

    """Membatalkan (Undo) proses update skor triase menggunakan Stack LIFO."""
    aksi_terakhir = stack_triase.pop()
    
    nik_batal = aksi_terakhir["nik"]
    skor_lama = aksi_terakhir["skor_lama"]
    data_semua = load_json("data/pasien.json")
    
    # Cari dan pulihkan
    pasien_ditemukan = False
    for data in data_semua:
        if data.get("nik") == nik_batal:
            data["danger_score"] = skor_lama
            pasien_ditemukan = True
            break
            
    if pasien_ditemukan:
        save_json("data/pasien.json", data_semua)
        print(f"[SUCCESS] Danger score NIK {nik_batal} berhasil di-restore ke nilai awal: {skor_lama}.")
    else:
        print(f"[ERROR] Data pasien NIK {nik_batal} tidak ditemukan, gagal undo.")


def lihat_antrian_ugd():
    """
    Fungsi utama yang dipanggil dari main.py.
    Mengambil pasien UGD, mengurutkan dengan Bubble Sort,
    lalu menampilkan hasilnya.
    """
    daftar_ugd = ambil_pasien_ugd()
    daftar_terurut = bubble_sort_ugd(daftar_ugd)
    tampilkan_antrian_ugd(daftar_terurut)
