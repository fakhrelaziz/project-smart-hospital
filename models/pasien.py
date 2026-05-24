class Pasien:
    def __init__(self, nik, nama, umur, layanan):
        self.nik = nik
        self.nama = nama
        self.umur = umur
        self.jenis_layanan = layanan
        self.status = "terdaftar"
        self.rekam_medis = []
        self.danger_score = 0
        self.kamar = None
        
    
    def objek_ke_dict(self):
        return {
            "nik"         : self.nik,
            "nama"        : self.nama,
            "umur"        : self.umur,
            "layanan"     : self.jenis_layanan,  # sesuaikan key-nya
            "status"      : self.status,
            "danger_score": self.danger_score,
            "nomor_kamar" : self.kamar if hasattr(self, 'kamar') else None,
            "rekam_medis" : []
        }
    
    def dict_ke_objek(self, data):
        self.nik = data.get("nik")
        self.nama = data.get("nama")
        self.umur = data.get("umur")
        self.jenis_layanan = data.get("layanan")
        self.status = data.get("status")
        self.danger_score = data.get("danger_score")
        self.kamar = data.get("nomor_kamar")
        self.rekam_medis = data.get("rekam_medis", [])
        
    def data_pasien(self):
        return (f"NIK          : {self.nik}\n"
                f"Nama         : {self.nama}\n"
                f"Umur         : {self.umur}\n"
                f"Layanan      : {self.jenis_layanan}\n"
                f"Status       : {self.status}\n"
                f"Danger Score : {self.danger_score}")

    def cek_danger_score(self):
        return self.danger_score

    def update_danger_score(self, danger_score_baru):
        self.danger_score = danger_score_baru

    def update_status(self, status_baru):
        self.status = status_baru

    def update_layanan(self, layanan_baru):
        self.jenis_layanan = layanan_baru

    def set_kamar(self, nomor_kamar_baru):
        self.kamar = nomor_kamar_baru