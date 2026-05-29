class NodeKamar:
    def __init__(self, data_kamar):
        self.data = data_kamar
        self.next = None
        self.prev = None

class NavigasiKamar:
    def __init__(self):
        self.head = None
        self.tail = None

    def tambah_kamar(self, data_kamar):
        node_baru = NodeKamar(data_kamar)
        
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
            return
            
        self.tail.next = node_baru
        node_baru.prev = self.tail
        self.tail = node_baru

    def cari_kamar_kosong(self):
        saat_ini = self.head
        while saat_ini is not None:
            kamar = saat_ini.data
            # Ngecek apakah kasur di kamar ini masih ada yang kosong
            if len(kamar.pasien_terisi) < kamar.kapasitas_kasur:
                return [kamar]
            saat_ini = saat_ini.next
        return None

    def lihat_kamar_maju(self):
        saat_ini = self.head
        while saat_ini is not None:
            print(f"Kamar {saat_ini.data.nomor} - {saat_ini.data.tipe}")
            saat_ini = saat_ini.next

    def lihat_kamar_mundur(self):
        saat_ini = self.tail
        while saat_ini is not None:
            print(f"Kamar {saat_ini.data.nomor} - {saat_ini.data.tipe}")
            saat_ini = saat_ini.prev

    def to_list(self):
        hasil = []
        saat_ini = self.head
        while saat_ini is not None:
            hasil.append(saat_ini.data.to_dict())
            saat_ini = saat_ini.next
        return hasil