from modules.manage_kamar import (
    assign_pasien_ke_kamar,
    lihat_kamar,
    lihat_kamar_tersedia,
    pasien_keluar_kamar,
)
from modules.manage_obat import (
    lihat_obat,
    tambah_obat,
    ubah_harga_obat,
    ubah_stok_obat,
)
from modules.manage_pasien import (
    lihat_semua_pasien, 
    daftar_pasien_baru,
    lihat_antrian_pendaftaran,
    proses_antrian_pendaftaran,
    undo_pendaftaran_terakhir
)

while True:
    print("\n=== SMART HOSPITAL ===")
    print("1. Pasien")
    print("2. Kamar")
    print("3. Obat")
    print("4. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        while True:
            print("\n=== MANAJEMEN PASIEN ===")
            print("1. Lihat Keseluruhan Pasien")
            print("2. Daftar Pasien Baru (Antri)")
            print("3. Lihat Antrean Pendaftaran")
            print("4. Proses Antrean (Layani Pasien)")
            print("5. Undo Pendaftaran Terakhir")
            print("6. Kembali")

            pilihan = input("Pilih menu: ")

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
                break
            else:
                print("Pilihan invalid.")

    elif pilihan == "2":
        while True:
            print("\n=== INFO KAMAR ===")
            print("1. Lihat Kamar")
            print("2. Lihat Kamar Tersedia")
            print("3. Assign Pasien ke Kamar")
            print("4. Pasien Keluar Kamar")
            print("5. Kembali")

            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                lihat_kamar()
            elif pilihan == "2":
                lihat_kamar_tersedia()
            elif pilihan == "3":
                assign_pasien_ke_kamar()
            elif pilihan == "4":
                pasien_keluar_kamar()
            elif pilihan == "5":
                break
            else:
                print("Pilihan invalid.")


    elif pilihan == "3":
        while True:
            print("\n=== INFO OBAT ===")
            print("1. Lihat Obat")
            print("2. Tambah Obat")
            print("3. Ubah Stok Obat")
            print("4. Ubah Harga Obat")
            print("5. Kembali")

            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                lihat_obat()
            elif pilihan == "2":
                tambah_obat()
            elif pilihan == "3":
                ubah_stok_obat()
            elif pilihan == "4":
                ubah_harga_obat()
            elif pilihan == "5":
                break
            else:
                print("Pilihan invalid.")

    elif pilihan == "4":
        print("Program selesai")
        break
    else:
        print("Pilihan tidak valid")
