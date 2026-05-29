"""
File    : main.py
Deskripsi: Entry point utama program Smart Hospital CLI.
Tujuan  : Menampilkan menu utama dan menghubungkan semua modul handler ke antarmuka CLI.
Catatan :
    - Semua logika bisnis berada di dalam modules/. main.py hanya sebagai router menu.
    - Data disimpan per-operasi (tidak perlu save eksplisit saat keluar).
Relasi  :
    - modules.manage_pasien
    - modules.manage_kamar
    - modules.manage_obat
    - modules.sorting_triase
    - modules.graph_rujukan
    - modules.searching
"""

from modules.manage_kamar import (
    assign_pasien_ke_kamar,
    lihat_kamar,
    lihat_kamar_tersedia,
    pasien_keluar_kamar,
    lihat_kamar_maju,
    lihat_kamar_mundur,
    cari_kamar_kosong_terdekat,
    lihat_jadwal_obat_pasien
)
from modules.manage_obat import (
    lihat_obat,
    tambah_obat,
    ubah_harga_obat,
    ubah_stok_obat,
    cari_obat_kode,
    prediksi_stok_habis,
    tampilkan_katalog_obat
)
from modules.manage_pasien import (
    lihat_semua_pasien,
    daftar_pasien_baru,
    lihat_antrian_pendaftaran,
    proses_antrian_pendaftaran,
    undo_pendaftaran_terakhir,
    lihat_rekam_medis_pasien,
    tambah_catatan_rekam_medis
)
from modules.sorting_triase import (
    tampilkan_antrian_ugd,
    lihat_antrian_ugd,
    update_danger_score,
    undo_skor_triase_terakhir
)
from modules.graph_rujukan import (
    lihat_peta_rujukan,
    cari_rs_rujukan,
    ubah_status_rs
)
from modules.searching import (
    cari_pasien_nama,
    cari_pasien_nik,
    cari_pasien_layanan
)

#MENU UTAMA

while True:
    print("\n" + "=" * 50)
    print("     SELAMAT DATANG DI SMART HOSPITAL SYSTEM")
    print("=" * 50)

    print("\n" + "=" * 15 + " MENU UTAMA " + "=" * 15)
    print("  [1] Pendaftaran Pasien")
    print("  [2] Layanan UGD")
    print("  [3] Rawat Inap & Navigasi Kamar")
    print("  [4] Sistem Farmasi & Apotek")
    print("  [5] Sistem Rujukan Lintas RS")
    print("  [6] Pencarian Data")
    print("  [7] Keluar")
    print("=" * 42)

    pilihan = input("Pilih menu: ").strip()

    # ── [1] PENDAFTARAN PASIEN 
    if pilihan == "1":
        while True:
            print("\n=== MANAJEMEN PASIEN ===")
            print("  [1] Lihat Keseluruhan Pasien")
            print("  [2] Daftar Pasien Baru (Antri)")
            print("  [3] Lihat Antrean Pendaftaran")
            print("  [4] Proses Antrean (Layani Pasien)")
            print("  [5] Undo Pendaftaran Terakhir")
            print("  [6] Lihat Rekam Medis Pasien (SLL)")
            print("  [7] Tambah Catatan Rekam Medis")
            print("  [8] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                lihat_semua_pasien()
            elif pilihan == "2":
                daftar_pasien_baru()
            elif pilihan == "3":
                lihat_antrian_pendaftaran()
            elif pilihan == "4":
                proses_antrian_pendaftaran()
            elif pilihan == "5":
                undo_pendaftaran_terakhir()
            elif pilihan == "6":
                lihat_rekam_medis_pasien()
            elif pilihan == "7":
                tambah_catatan_rekam_medis()
            elif pilihan == "8":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [2] LAYANAN UGD ───────────────────────────────────────────────────────
    elif pilihan == "2":
        while True:
            print("\n=== LAYANAN UGD ===")
            print("  [1] Lihat Antrean UGD (Sorted by Danger Score)")
            print("  [2] Update Skor Triase Pasien")
            print("  [3] Undo Update Skor Triase Terakhir")
            print("  [4] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                lihat_antrian_ugd()
            elif pilihan == "2":
                update_danger_score()
            elif pilihan == "3":
                undo_skor_triase_terakhir()
            elif pilihan == "4":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [3] RAWAT INAP & NAVIGASI KAMAR ──────────────────────────────────────
    elif pilihan == "3":
        while True:
            print("\n=== RAWAT INAP & NAVIGASI KAMAR  ===")
            print("  [1] Lihat Semua Kamar")
            print("  [2] Lihat Kamar Tersedia")
            print("  [3] Assign Pasien ke Kamar")
            print("  [4] Pasien Keluar Kamar")
            print("  [5] Lihat Lorong Kamar (Maju — DLL)")
            print("  [6] Lihat Lorong Kamar (Mundur — DLL)")
            print("  [7] Cari Kamar Kosong Terdekat (DLL)")
            print("  [8] Lihat Jadwal Minum Obat Pasien (CLL)")
            print("  [9] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                lihat_kamar()
            elif pilihan == "2":
                lihat_kamar_tersedia()
            elif pilihan == "3":
                assign_pasien_ke_kamar()
            elif pilihan == "4":
                pasien_keluar_kamar()
            elif pilihan == "5":
                lihat_kamar_maju()
            elif pilihan == "6":
                lihat_kamar_mundur()
            elif pilihan == "7":
                cari_kamar_kosong_terdekat()
            elif pilihan == "8":
                lihat_jadwal_obat_pasien()
            elif pilihan == "9":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [4] SISTEM FARMASI & APOTEK ───────────────────────────────────────────
    elif pilihan == "4":
        while True:
            print("\n=== INFO OBAT ===")
            print("  [1] Lihat Daftar Obat")
            print("  [2] Tambah Obat")
            print("  [3] Ubah Stok Obat")
            print("  [4] Ubah Harga Obat")
            print("  [5] Cari Obat via Kode (Hash Table O(1))")
            print("  [6] Prediksi Sisa Hari Stok Obat (Rekursif)")
            print("  [7] Lihat Direktori Katalog Obat (Tree)")
            print("  [8] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                lihat_obat()
            elif pilihan == "2":
                tambah_obat()
            elif pilihan == "3":
                ubah_stok_obat()
            elif pilihan == "4":
                ubah_harga_obat()
            elif pilihan == "5":
                cari_obat_kode()
            elif pilihan == "6":
                prediksi_stok_habis()
            elif pilihan == "7":
                tampilkan_katalog_obat()
            elif pilihan == "8":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [5] SISTEM RUJUKAN LINTAS RS ──────────────────────────────────────────
    elif pilihan == "5":
        while True:
            print("\n=== HUB JARINGAN RUJUKAN RS (GRAPH) ===")
            print("  [1] Lihat Peta Visual Jaringan RS")
            print("  [2] Cari RS Rujukan Terdekat (BFS)")
            print("  [3] Ubah Ketersediaan / Status RS")
            print("  [4] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                lihat_peta_rujukan()
            elif pilihan == "2":
                cari_rs_rujukan()
            elif pilihan == "3":
                ubah_status_rs()
            elif pilihan == "4":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [6] PENCARIAN DATA ────────────────────────────────────────────────────
    elif pilihan == "6":
        while True:
            print("\n=== PENCARIAN DATA ===")
            print("  [1] Cari Pasien by Nama  (Linear Search)")
            print("  [2] Cari Pasien by NIK   (Binary Search)")
            print("  [3] Filter Pasien by Layanan")
            print("  [4] Kembali")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                cari_pasien_nama()
            elif pilihan == "2":
                cari_pasien_nik()
            elif pilihan == "3":
                cari_pasien_layanan()
            elif pilihan == "4":
                break
            else:
                print("[INFO] Pilihan tidak valid.")

    # ── [7] KELUAR ────────────────────────────────────────────────────────────
    elif pilihan == "7":
        print("\n[INFO] Data sudah tersimpan secara otomatis setiap operasi.")
        print("Terima kasih telah menggunakan Smart Hospital System. Sampai jumpa!")
        break

    else:
        print("[INFO] Pilihan tidak valid. Masukkan angka 1-7.")
