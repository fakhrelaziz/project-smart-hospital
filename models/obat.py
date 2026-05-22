class Obat:
    def __init__(self, kode, nama, kategori, stok, harga):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga

    #untuk menampilkan data ringkas obat
    def dataObat(self):
        return f"Kode: {self.kode}\nNama obat: {self.nama}\nKategori: {self.kategori}\nStok: {self.stok}\nHarga: {self.harga}"

    #nambahin stok
    def tambahStok(self, tambah):
        self.stok += tambah
        return f"Stok ditambahkan\n Stok {self.nama} sekarang: {self.stok}"

    #kurangin stok jika ada yang beli atau berobat
    def kurangStok(self, kurang):
        if self.stok >= kurang:
            self.stok -= kurang
            return f"Stok dikurangi\n Stok {self.nama} sekarang: {self.stok}"
        else:
            return f"Stok obat kurang"

    #naik turunin harga
    def ubahHarga(self, hargaBaru):
        self.harga = hargaBaru
        return f"harga {self.nama} sekarang adalah {self.harga}"