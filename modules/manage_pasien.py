from utils.json_handler import load_json, save_json

def lihat_pasien():

    data_pasien = load_json("data/pasien.json")

    for pasien in data_pasien:

        print("-" * 40)
        print("NIK          :", pasien["nik"])
        print("Nama         :", pasien["nama"])
        print("Umur         :", pasien["umur"])
        print("Layanan      :", pasien["layanan"])
        print("Status       :", pasien["status"])
        print("Danger Score :", pasien["danger_score"])


def tambah_pasien():

    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK: ")

    for pasien in data_pasien:
        if pasien["nik"] == nik:
            print("NIK sudah terdaftar")
            return

    nama = input("Masukkan Nama: ")
    while True:

    try:
        umur = int(input("Masukkan umur: "))
        break

    except ValueError:
        print("Umur harus angka!")
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