"""
Deskripsi:
    Mengimplementasikan struktur data Stack secara untuk menyimpan
    riwayat aksi pendaftaran dan triase medis demi keperluan fitur Undo.
"""

class UndoStack:
    def __init__(self):
        self.data = []

    def push(self, aksi):
        """Menyimpan data ke atas tumpukan (Push)."""
        self.data.append(aksi)
        return True

    def pop(self):
        """Mengambil dan menghapus data teratas dari tumpukan (Pop)."""
        if self.is_empty():
            return None
        return self.data.pop()

    def intip_aksi_terakhir(self):
        """Melihat data aksi teratas tanpa menghapusnya (Peek)."""
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        """Memeriksa apakah tumpukan sedang kosong."""
        return len(self.data) == 0

    def total_data(self):
        """Mengembalikan jumlah total data yang tersimpan di dalam tumpukan."""
        return len(self.data)