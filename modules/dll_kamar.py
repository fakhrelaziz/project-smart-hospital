"""
Mengimplementasikan Double Linked List untuk navigasi kamar rawat inap.
Setiap node merepresentasikan satu kamar dengan pointer ke kamar
berikutnya (next) dan sebelumnya (prev).
"""

class NodeKamar:
    def __init__(self, data_kamar):
        self.data = data_kamar
        self.next = None
        self.prev = None

class NavigasiKamar:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, data_kamar):
        """fungsi lihat_kamar_tersedia di file manage_kamar melooping data kamar dan dimasukkan ke fungsi insert"""
        node_baru = NodeKamar(data_kamar)
        
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
            return
            
        self.tail.next = node_baru
        node_baru.prev = self.tail
        self.tail = node_baru

    def traversal(self):
        """Menyusuri DLL dan mengembalikan daftar kamar yang Kosong."""
        kamar_tersedia = []
        saat_ini = self.head
        while saat_ini is not None:
            # Pengecekan matematis lebih aman daripada string teks
            if len(saat_ini.data.pasien_terisi) < saat_ini.data.kapasitas_kasur:
                kamar_tersedia.append(saat_ini.data)
            saat_ini = saat_ini.next
        return kamar_tersedia

