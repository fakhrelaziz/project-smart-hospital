"""
Mengimplementasikan Circular Linked List untuk mengelola siklus jadwal
minum obat pasien rawat inap. Node terakhir (Malam) menunjuk kembali
ke node pertama (Pagi) sehingga siklus berjalan tanpa batas.
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
        
        # Kalau masih kosong, dia jadi head sekaligus ekor, dan menunjuk ke dirinya sendiri
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
            node_baru.next = self.head
            return
            
        # Sambungkan ekor lama ke node baru
        self.tail.next = node_baru
        self.tail = node_baru
        
        # Sisi unik CLL: Ekor yang baru wajib nunjuk balik ke head
        self.tail.next = self.head

    def lihat_jadwal(self, jumlah_putaran=1, interaktif=False):
        if self.head is None:
            print("[-] Belum ada jadwal.")
            return
            
        saat_ini = self.head
        putaran_sekarang = 0
        
        print("=== JADWAL SIKLUS ===")
        
        if interaktif:
            while True:
                pilihan = input(f"- {saat_ini.data}   (Tekan ENTER untuk lanjut, ketik 'q' untuk berhenti): ").strip().lower()
                if pilihan == 'q':
                    break
                
                saat_ini = saat_ini.next
                if saat_ini == self.head:
                    print("--- (Siklus Berulang) ---")
        else:
            # Karena muter terus gak ada ujungnya, kita kasih batas putaran biar gak infinity loop
            while putaran_sekarang < jumlah_putaran:
                print(f"- {saat_ini.data}")
                saat_ini = saat_ini.next
                
                # Kalau udah balik ke head, berarti satu putaran selesai
                if saat_ini == self.head:
                    putaran_sekarang += 1
                    print("--- (Siklus Berulang) ---")

    def to_list(self):
        if self.head is None:
            return []
            
        hasil = []
        saat_ini = self.head
        
        while True:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
            if saat_ini == self.head:  
                break
                
        return hasil