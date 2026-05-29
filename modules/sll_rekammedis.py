"""
File    : modules/sll_rekammedis.py
Materi  : Single Linked List (SLL)
Deskripsi:
    Mengimplementasikan Single Linked List untuk menyimpan riwayat rekam
    medis pasien secara kronologis. Setiap kali pasien berobat, catatan
    baru ditambahkan (append) ke ujung list sebagai node baru.
Catatan :
    - Setiap node menyimpan satu catatan rekam medis (dict: tanggal, diagnosis, resep).
    - to_list() dan from_list() digunakan untuk serialisasi/deserialisasi JSON.
Relasi  :
    - Digunakan oleh modules/manage_pasien.py untuk lihat dan tambah rekam medis.
"""


class NodeRiwayat:
    def __init__(self, data):
        self.data = data  
        self.next = None  

class SingleLinkedListRekamMedis:
    def __init__(self):
        self.head = None  

    def tambah_riwayat(self, catatan):
        node_baru = NodeRiwayat(catatan)
        if self.head is None:
            self.head = node_baru
            return
        saat_ini = self.head
        while saat_ini.next is not None:
            saat_ini = saat_ini.next
        saat_ini.next = node_baru

    def lihat_riwayat(self):
        if self.head is None:
            print("Belum ada riwayat rekam medis.")
            return
        print("=== BUKU REKAM MEDIS ===")
        saat_ini = self.head
        nomor = 1
        while saat_ini is not None:
            print(f"{nomor}. {saat_ini.data}")
            saat_ini = saat_ini.next
            nomor += 1

    def to_list(self):
        """Membongkar SLL menjadi list biasa agar bisa masuk JSON"""
        hasil = []
        saat_ini = self.head
        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    def from_list(self, data_list):
        """Merakit ulang SLL dari data list JSON"""
        for catatan in data_list:
            self.tambah_riwayat(catatan)