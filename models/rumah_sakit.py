class RumahSakit:
    def __init__(self, nama, kapasitas_ugd):
        self.nama = nama
        self.daftar_kamar = []
        self.kapasitas_ugd = kapasitas_ugd
        self.status_penuh = False

    def objek_ke_dict(self):
        return {
            'nama': self.nama,
            'daftar_kamar': self.daftar_kamar,
            'kapasitas_ugd': self.kapasitas_ugd,
            'status_penuh': self.status_penuh
        }
    
    def dict_ke_objek(self, data):
        self.nama = data.get('namma')
        self.daftar_kamar = data.get('daftar_kamar', [])
        self.kapasitas_ugd = data.get('kapasitas_ugd')
        self.status_penuh = data.get('status_penuh', False)