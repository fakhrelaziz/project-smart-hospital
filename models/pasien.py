"""
Mendefinisikan class Pasien sebagai representasi objek data pasien
dalam sistem Smart Hospital. Menyimpan semua atribut dan method
untuk manipulasi data pasien.
- Rekam medis disimpan sebagai list dict dan dikelola oleh sll_rekammedis.py.
- Method objek_ke_dict() digunakan untuk serialisasi ke JSON.
- Method dict_ke_objek() digunakan untuk deserialisasi dari JSON.
"""

class Pasien:
    def __init__(self, nik="", nama="", umur=0, layanan=""):
        self.nik = nik
        self.nama = nama
        self.umur = umur
        self.jenis_layanan = layanan
        self.status = "antri"
        self.rekam_medis = []
        self.danger_score = 0
        self.kamar = None
        
    
    def objek_ke_dict(self):
        """Mengubah objek Pasien menjadi dictionary agar bisa si simpan ke JSON."""
        return {
            "nik"         : self.nik,
            "nama"        : self.nama,
            "umur"        : self.umur,
            "layanan"     : self.jenis_layanan,
            "status"      : self.status,
            "danger_score": self.danger_score,
            "nomor_kamar" : self.kamar if hasattr(self, 'kamar') else None,
            "rekam_medis" : self.rekam_medis
        }
    

    def dict_ke_objek(self, data):
        """mengubah dictionary yg di json tu ke dalam bentuk atribut objek Pasien."""
        self.nik = data.get("nik")
        self.nama = data.get("nama")
        self.umur = data.get("umur")
        self.jenis_layanan = data.get("layanan")
        self.status = data.get("status")
        self.danger_score = data.get("danger_score")
        self.kamar = data.get("nomor_kamar")
        self.rekam_medis = data.get("rekam_medis", [])

    def data_pasien(self):
        """ini untuk tampilkan atau ngeprint data pasien """
        return (f"NIK          : {self.nik}\n"
                f"Nama         : {self.nama}\n"
                f"Umur         : {self.umur}\n"
                f"Jenis Layanan: {self.jenis_layanan}\n"
                f"Status       : {self.status}\n"
                f"Kamar        : {self.kamar if self.kamar else '-'}")

    def cek_danger_score(self):
        """Mengembalikan nilai danger_score pasien."""
        return self.danger_score

    def update_danger_score(self, danger_score):
        """Memperbarui nilai danger_score pasien setelah pemeriksaan atau perawatan."""
        self.danger_score = danger_score

    def update_status(self, status):
        """Memperbarui status pasien, misalnya dari 'antri' ketika mendaftar lalu 'selesai' ketika dilayani."""
        self.status = status

    def update_layanan(self, layanan):
        """Memperbarui jenis layanan pasien, misalnya dari rawat jalan ke rawat inap."""
        self.jenis_layanan = layanan

    def set_kamar(self, nomor_kamar):
        """Menyimpan nomor kamar yang ditempati pasien."""
        self.kamar = nomor_kamar

    def tambah_rekam_medis(self, tanggal, diagnosis, resep):
        """tambah rekam medis pasien """
        rekam_medis = {
            "tanggal": tanggal,
            "diagnosis": diagnosis,
            "resep": resep
        }
        self.rekam_medis.append(rekam_medis)