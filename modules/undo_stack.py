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
        """Mengambil dan menghapus data terakhir (Pop)."""
        if self.is_empty():
            return None
        return self.data.pop()

    def intip_aksi_terakhir(self):
        """Melihat data teratas tanpa menghapusnya (Peek)."""
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        """Memeriksa apakah tumpukan sedang kosong."""
        return len(self.data) == 0