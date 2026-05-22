from utils.json_handler import load_json, save_json

def lihat_obat():

     data_obat = load_json("data/obat.json")

     for obat in data_obat:
          print("-" * 40)
          print("Kode     :", obat["kode"])
          print("Nama     :", obat["nama"])
          print("Kategori :", obat["kategori"])
          print("Stok     :", obat["stok"])
          print("Harga    :", obat["harga"])

def tambah_obat():

     data_obat = load_json("data/obat.json")

     kode = input("Masukkan kode obat: ")
     nama = input("Masukkan nama: ")
     kategori = input("Masukkan kategori: ")
     stok = int(input("Berapa stok?:  "))
     harga = int(input("Harga: "))
     
     obat_baru = {
          "kode": kode,
          "nama": nama,
          "kategori": kategori,
          "stok": stok,
          "harga": harga
     }

     data_obat.append(obat_baru)

     save_json("data/obat.json", data_obat)

     print("Obat berhasil ditambahkan")