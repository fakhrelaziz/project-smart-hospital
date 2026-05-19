from utils.json_handler import load_json, save_json # memanggil fungsi load_json dan save_json dari path utils/json_handler.py

while True:
     print("\n=== SMART HOSPITAL ===")
     print("1. Lihat Pasien")
     print("2. Tambah Pasien")
     print("3. Keluar")

     pilihan = input("Pilih menu: ")

     if pilihan == "1":

          data_pasien = load_json("data/pasien.json")

          for pasien in data_pasien:
               print("-" * 40)
               print("NIK          :", pasien["nik"])
               print("Nama         :", pasien["nama"])
               print("Umur         :", pasien["umur"])
               print("Layanan      :", pasien["layanan"])
               print("Status       :", pasien["status"])
               print("Danger Score :", pasien["danger_score"])
     
     elif pilihan == "2":

          data_pasien = load_json("data/pasien.json")

          nik = input("Masukkan NIK: ")
          nama = input("Masukkan Nama: ")
          umur = int(input("Masukkan Umur: "))
          layanan = input("Masukkan Layanan: ")

          pasien_baru = {
               "nik": nik,
               "nama": nama,
               "umur": umur,
               "layanan": layanan,
               "status": "terdaftar",
               "danger_score": 0
          }

          data_pasien.append(pasien_baru)

          save_json("data/pasien.json", data_pasien)

          print("Pasien berhasil ditambahkan")
     
     elif pilihan == "3":
          print("Program selesai")
          break

     else:
          print("Pilihan tidak valid")