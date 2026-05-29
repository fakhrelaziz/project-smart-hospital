"""
File    : modules/cll_obat.py
Materi  : Circular Linked List (CLL)
Deskripsi:
    Mengimplementasikan Circular Linked List untuk mengelola siklus jadwal
    minum obat pasien rawat inap. Node terakhir (Malam) menunjuk kembali
    ke node pertama (Pagi) sehingga siklus berjalan tanpa batas.
Catatan :
    - Siklus default: Pagi (07.00) → Siang (13.00) → Malam (19.00) → kembali ke Pagi.
    - lihat_jadwal(jumlah_putaran) membatasi iterasi agar tidak infinite loop.
Relasi  :
    - Digunakan oleh modules/manage_kamar.py melalui lihat_jadwal_obat_pasien().
"""


class NodeJadwal:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def tambah_jadwal(self, data):
        node_baru = NodeJadwal(data)
        
        # Kalau masih kosong, dia jadi kepala sekaligus ekor, dan menunjuk ke dirinya sendiri
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
            node_baru.next = self.head
            return
            
        # Sambungkan ekor lama ke node baru
        self.tail.next = node_baru
        self.tail = node_baru
        
        # Sisi unik CLL: Ekor yang baru wajib nunjuk balik ke kepala
        self.tail.next = self.head

    def lihat_jadwal(self, jumlah_putaran=1):
        if self.head is None:
            print("[-] Belum ada jadwal.")
            return
            
        saat_ini = self.head
        putaran_sekarang = 0
        
        print("=== JADWAL SIKLUS ===")
        # Karena muter terus gak ada ujungnya, kita kasih batas putaran biar gak infinity loop
        while putaran_sekarang < jumlah_putaran:
            print(f"- {saat_ini.data}")
            saat_ini = saat_ini.next
            
            # Kalau udah balik ke kepala, berarti satu putaran selesai
            if saat_ini == self.head:
                putaran_sekarang += 1
                print("--- (Siklus Berulang) ---")

    def to_list(self):
        if self.head is None:
            return []
            
        hasil = []
        saat_ini = self.head
        
        # Pakai do-while ala Python biar gampang
        while True:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
            if saat_ini == self.head:  # Berhenti kalau udah muter balik ke kepala
                break
                
        return hasil