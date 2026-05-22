from models.kamar import Kamar
from utils.json_handler import load_json, save_json

def lihat_kamar():

     data_kamar = load_json("data/kamar.json")

     for kamar in data_kamar:
          print("-" * 40)
          print("Nomor         :", kamar["nomor"])
          print("Tipe          :", kamar["tipe"])
          print("Status        :", kamar["status"])
          print("Pasien Terisi :", kamar["pasien_terisi"])


def tambah_kamar():

     data_kamar = load_json("data/kamar.json")

     nomor = input("Masukkan nomor kamar: ")
     tipe = input("Masukkan tipe: ")

     kamar_baru = Kamar(nomor, tipe)

     data_kamar.append(kamar_baru)

     save_json("data/kamar.json", data_kamar)
     print("Kamar berhasil ditambahkan")
     