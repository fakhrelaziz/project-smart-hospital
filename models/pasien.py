class Pasien:
    def __init__(self, nik, nama, umur, jenisLayanan):
        self.nik = nik
        self.nama = nama
        self.umur = umur
        self.jenisLayanan = jenisLayanan
        self.riwayat = None
        self.danger_score = 0
        self.status = "Terdaftar"

    def dataPasien(self):
        return (f"NIK: {self.nik}\nNama: {self.nama}\nUmur:{self.umur}")

    def cekDangerScore(self):
        return self.danger_score

    def updateDangerScore(self, dangerScoreBaru):
        self.danger_score = dangerScoreBaru

    def updateStatus(self, statusBaru):
        self.status = statusBaru

    def updateLayanan(self, layananBaru):
        self.jenisLayanan = layananBaru

    def setKamar(self, nomorKamarBaru):
        self.kamar = nomorKamarBaru