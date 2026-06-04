"""
File    : modules/graph_rujukan.py
Materi  : Graph (Data Structure)
Deskripsi:
    Merepresentasikan jaringan rumah sakit rujukan sebagai Struktur Data Graph
    dengan adjacency list.
Catatan :
    - Data diimpor dari models/rumah_sakit.py.
    - Algoritma pencarian dan interaksi CLI dikelola oleh manage_rujukan.py.
"""

from models.rumah_sakit import JARINGAN_RS, STATUS_AWAL

class GraphRujukan:
    """
    Merepresentasikan jaringan RS rujukan sebagai Graph.
    Berperan sebagai Struktur Data (Data Structure).
    """

    def __init__(self):
        # Adjacency list — struktur utama graph
        self.graph  = JARINGAN_RS
        # Status setiap RS (Merujuk ke global dictionary agar perubahan permanen)
        self.status = STATUS_AWAL

    def set_status(self, nama_rs, status):
        """
        Mengubah status sebuah RS.

        Args:
            nama_rs (str): Nama RS yang ingin diubah statusnya.
            status  (str): "Tersedia" atau "Penuh".

        Returns:
            bool: True jika berhasil, False jika nama RS tidak ada atau input salah.
        """
        if nama_rs not in self.graph:
            print(f"  [ERROR] RS '{nama_rs}' tidak ada di jaringan.")
            return False

        if status not in ("Tersedia", "Penuh"):
            print(f"  [ERROR] Status harus 'Tersedia' atau 'Penuh'.")
            return False

        self.status[nama_rs] = status
        return True

    def bfs_cari_rujukan(self, rs_asal="Smart Hospital"):
        """
        Mencari RS rujukan terdekat yang statusnya "Tersedia"
        menggunakan algoritma Breadth-First Search (BFS).
        
        Returns dictionary yang berisi rs_tujuan, rute, hop, dan history pemeriksaan.
        """
        from collections import deque
        if rs_asal not in self.graph:
            return {"rs_tujuan": None, "rute": [], "hop": 0, "history": []}

        queue = deque()
        visited = set()

        queue.append((rs_asal, [rs_asal]))
        visited.add(rs_asal)

        history = []

        while queue:
            rs_sekarang, rute = queue.popleft()
            status_rs = self.status.get(rs_sekarang, "?")

            # Catat riwayat pemeriksaan untuk keperluan UI/Demo (selain RS asal)
            if rs_sekarang != rs_asal:
                history.append((rs_sekarang, status_rs))

            if rs_sekarang != rs_asal and status_rs == "Tersedia":
                return {
                    "rs_tujuan": rs_sekarang,
                    "rute"     : rute,
                    "hop"      : len(rute) - 1,
                    "history"  : history
                }

            for tetangga in self.graph.get(rs_sekarang, []):
                if tetangga not in visited:
                    visited.add(tetangga)
                    queue.append((tetangga, rute + [tetangga]))

        return {"rs_tujuan": None, "rute": [], "hop": 0, "history": history}