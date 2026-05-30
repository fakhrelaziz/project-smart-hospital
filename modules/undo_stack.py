"""
File    : modules/undo_stack.py
Materi  : Stack — Tumpukan LIFO (Last In First Out)
Deskripsi:
    Mengimplementasikan struktur data Stack secara manual untuk menyimpan
    riwayat aksi pendaftaran dan triase medis demi keperluan fitur Undo.
Catatan :
    - Bersifat umum (Generic) dan tidak terikat pada logika bisnis spesifik.
    - Menyediakan antarmuka standar: append (Push) dan pop (Pop).
    - Mempertahankan alias Stack dan Stack_UGD untuk kompatibilitas ke belakang.
Relasi  :
    - Digunakan oleh modules/manage_pasien.py dan modules/sorting_triase.py.
"""


class UndoStack:
    """Implementasi struktur data Stack manual yang murni dan umum (Generic)."""

    def __init__(self):
        self.data = []

    def append(self, aksi):
        """Menyimpan data aksi ke atas tumpukan (Push).

        Args:
            aksi: Data riwayat perubahan.

        Returns:
            True jika berhasil disimpan.
        """
        self.data.append(aksi)
        return True

    def pop(self):
        """Mengambil dan menghapus data aksi teratas dari tumpukan (Pop).

        Returns:
            Data aksi teratas, atau None jika tumpukan kosong.
        """
        if self.is_empty():
            return None
        return self.data.pop()

    def intip_aksi_terakhir(self):
        """Melihat data aksi teratas tanpa menghapusnya (Peek).

        Returns:
            Data aksi teratas, atau None jika tumpukan kosong.
        """
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        """Memeriksa apakah tumpukan sedang kosong.

        Returns:
            True jika kosong, False jika ada isinya.
        """
        return len(self.data) == 0

    def total_data(self):
        """Mengembalikan jumlah total data yang tersimpan di dalam tumpukan.

        Returns:
            Jumlah data aksi.
        """
        return len(self.data)