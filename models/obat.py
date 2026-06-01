"""
File: models/obat.py
Deskripsi: Model data Obat dan operasi dasar stok serta harga.
Tujuan: Menyimpan data obat dan menyediakan method manipulasi sederhana.
Catatan penting: Validasi input dilakukan di layer handler.
Relasi: Digunakan oleh modules/manage_obat.py dan modul farmasi lainnya.
"""


class Obat:
    def __init__(self, kode, nama, kategori, bentuk, stok, harga, pemakaian_harian=0):
        """Inisialisasi objek obat dengan atribut utama."""
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.bentuk = bentuk
        self.stok = stok
        self.harga = harga
        self.pemakaian_harian = pemakaian_harian

    def data_obat(self):
        """Mengembalikan ringkasan data obat dalam format string."""
        return f"Kode: {self.kode}\nNama obat: {self.nama}\nKategori: {self.kategori}\nBentuk: {self.bentuk}\nStok: {self.stok}\nHarga: {self.harga}\nPemakaian Harian RS: {self.pemakaian_harian}"

    def objek_ke_dict(self):
        """Mengubah objek obat menjadi dictionary untuk penyimpanan JSON."""
        return {
            "kode": self.kode,
            "nama": self.nama,
            "kategori": self.kategori,
            "bentuk": self.bentuk,
            "stok": self.stok,
            "harga": self.harga,
            "pemakaian_harian": self.pemakaian_harian
        }

    def dict_ke_objek(self, data):
        """Memuat data obat dari dictionary ke atribut objek."""
        self.kode = data.get("kode")
        self.nama = data.get("nama")
        self.kategori = data.get("kategori")
        self.bentuk = data.get("bentuk", "Tidak Diketahui")
        self.stok = data.get("stok")
        self.harga = data.get("harga")
        self.pemakaian_harian = data.get("pemakaian_harian", 0)

    def tambah_stok(self, tambah):
        """Menambah stok obat sesuai jumlah yang diberikan."""
        self.stok += tambah
        return f"Stok ditambahkan\nStok {self.nama} sekarang: {self.stok}"

    def kurang_stok(self, kurang):
        """Mengurangi stok obat jika mencukupi."""
        if self.stok >= kurang:
            self.stok -= kurang
            return f"Stok dikurangi\nStok {self.nama} sekarang: {self.stok}"
        else:
            return f"Stok obat kurang"

    def ubah_harga(self, harga_baru):
        """Mengubah harga obat ke nilai baru."""
        self.harga = harga_baru
        return f"harga {self.nama} sekarang adalah {self.harga}"

