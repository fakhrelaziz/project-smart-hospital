"""
File: models/obat.py
Deskripsi: Model data Obat dan operasi dasar stok serta harga.
Tujuan: Menyimpan data obat dan menyediakan method manipulasi sederhana.
Catatan penting: Validasi input dilakukan di layer handler.
Relasi: Digunakan oleh modules/manage_obat.py dan modul farmasi lainnya.
"""


class Obat:
    def __init__(self, kode, nama, kategori, stok, harga, dosis_harian=0):
        """Inisialisasi objek obat dengan atribut utama."""
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga
        self.dosis_harian = dosis_harian

    def data_obat(self):
        """Mengembalikan ringkasan data obat dalam format string."""
        return f"Kode: {self.kode}\nNama obat: {self.nama}\nKategori: {self.kategori}\nStok: {self.stok}\nHarga: {self.harga}\nDosis: {self.dosis_harian}"

    def objek_ke_dict(self):
        """Mengubah objek obat menjadi dictionary untuk penyimpanan JSON."""
        return {
            "kode": self.kode,
            "nama": self.nama,
            "kategori": self.kategori,
            "stok": self.stok,
            "harga": self.harga,
            "dosis_harian": self.dosis_harian
        }

    def dict_ke_objek(self, data):
        """Memuat data obat dari dictionary ke atribut objek."""
        self.kode = data.get("kode")
        self.nama = data.get("nama")
        self.kategori = data.get("kategori")
        self.stok = data.get("stok")
        self.harga = data.get("harga")
        self.dosis_harian = data.get("dosis_harian", 0)
        

    def tambah_stok(self, tambah):
        """Menambah stok obat sesuai jumlah yang diberikan."""
        self.stok += tambah
        return f"Stok ditambahkan\n Stok {self.nama} sekarang: {self.stok}"

    def kurang_stok(self, kurang):
        """Mengurangi stok obat jika mencukupi."""
        if self.stok >= kurang:
            self.stok -= kurang
            return f"Stok dikurangi\n Stok {self.nama} sekarang: {self.stok}"
        else:
            return f"Stok obat kurang"

    def ubah_harga(self, harga_baru):
        """Mengubah harga obat ke nilai baru."""
        self.harga = harga_baru
        return f"harga {self.nama} sekarang adalah {self.harga}"
