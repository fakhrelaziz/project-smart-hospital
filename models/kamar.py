class DLL:
    def __init__(self):
        self.head = None
        self.tail = None

    def tambah_kamar(self, kamar_baru):
        if self.head is None:
            self.head = kamar_baru
            self.tail = kamar_baru
        else:
            self.tail.next = kamar_baru
            kamar_baru.prev = self.tail
            self.tail = kamar_baru

    def cari_kamar_kosong(self):
        kamar_tersedia = []
        current = self.head
        while current is not None:
            if current.status == "Kosong":
                kamar_tersedia.append(current)
            current = current.next  
        return kamar_tersedia

class Kamar:
    def __init__(self, nomor, kelas):
        self.nomor = nomor
        self.kelas = kelas
        kasurPerRuangan = {
            "VIP": 1,
            "Kelas 1": 2,
            "Kelas 2": 3,
            "Kelas 3": 5
        }

        self.kapasitasKasur = kasurPerRuangan.get(kelas, 1)

        self.pasienTerisi = []

        self.next = None
        self.prev = None

    def statusKamar(self):
        jumlahPasien = len(self.pasienTerisi)
        
        if jumlahPasien == 0:
            return "Kosong"
        elif jumlahPasien < self.kapasitasKasur:
            kasurSisa = self.kapasitasKasur - jumlahPasien
            return f"Ada {kasurSisa} kasur kosong)"
        else:
            return "Penuh"

    def pasienMasuk(self, pasien):
        if len(self.pasienTerisi) < self.kapasitasKasur:
            self.pasienTerisi.append(pasien)
            return True
        else:
            print(f"Kamar {self.nomor} sudah penuh!")
            return False

    def pasienKeluar(self, pasien):
        if pasien in self.pasienTerisi:
            self.pasienTerisi.remove(pasien)
            print(f"Pasien keluar dari Kamar {self.nomor}")
        else:
            print("Pasien tidak ditemukan di kamar ini.")