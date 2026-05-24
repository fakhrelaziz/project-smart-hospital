class Obat:
    def __init__(self, kode, nama, kategori, stok, harga, dosis_harian=0):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga
        self.dosis_harian = dosis_harian

    #untuk menampilkan data ringkas obat
    def data_obat(self):
        return f"Kode: {self.kode}\nNama obat: {self.nama}\nKategori: {self.kategori}\nStok: {self.stok}\nHarga: {self.harga}\nDosis: {self.dosis_harian}"

    def objek_ke_dict(self):
        return {
            "kode": self.kode,
            "nama": self.nama,
            "kategori": self.kategori,
            "stok": self.stok,
            "harga": self.harga,
            "dosis_harian": self.dosis_harian
        }

    def dict_ke_objek(self, data):
        self.kode = data.get("kode")
        self.nama = data.get("nama")
        self.kategori = data.get("kategori")
        self.stok = data.get("stok")
        self.harga = data.get("harga")
        self.dosis_harian = data.get("dosis_harian", 0)

    #nambahin stok
    def tambah_stok(self, tambah):
        self.stok += tambah
        return f"Stok ditambahkan\n Stok {self.nama} sekarang: {self.stok}"

    #kurangin stok jika ada yang beli atau berobat
    def kurang_stok(self, kurang):
        if self.stok >= kurang:
            self.stok -= kurang
            return f"Stok dikurangi\n Stok {self.nama} sekarang: {self.stok}"
        else:
            return f"Stok obat kurang"

    #naik turunin harga
    def ubah_harga(self, harga_baru):
        self.harga = harga_baru
        return f"harga {self.nama} sekarang adalah {self.harga}"