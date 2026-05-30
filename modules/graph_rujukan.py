"""
File    : modules/graph_rujukan.py
Materi  : Graph + BFS (Materi Tambahan)
Deskripsi:
    Mengimplementasikan jaringan rumah sakit rujukan menggunakan Graph
    dan algoritma BFS (Breadth-First Search) untuk menemukan RS rujukan
    terdekat yang masih tersedia.
Struktur Graph:
    - Node  : Rumah sakit (Smart Hospital + 5 RS lainnya)
    - Edge  : Koneksi antar RS (jalan/jalur rujukan)
    - Representasi: Adjacency List (dictionary)
Cara kerja BFS:
    Mulai dari Smart Hospital, telusuri RS tetangga (1 hop) terlebih dahulu,
    baru kemudian RS yang lebih jauh (2 hop, 3 hop, dst).
    Ini MENJAMIN RS yang ditemukan adalah yang TERDEKAT dari Smart Hospital.
Peta Jaringan:
    Smart Hospital ── RS Medika ── RS Harapan
          │                           │
          ├── RS Bunda ── RS Sejahtera─┘
          │
          └── RS Kasih ──────────────────
Catatan :
    - Graph bersifat STATIS (hardcoded) — tidak ada tambah/hapus node
    - Status RS (Tersedia/Penuh) bisa diubah saat runtime
    - BFS diimplementasikan MANUAL menggunakan collections.deque
"""

from collections import deque


# ══════════════════════════════════════════════════════════════════════════════
# DATA GRAPH — HARDCODED (STATIS)
# ══════════════════════════════════════════════════════════════════════════════

# Adjacency List: setiap RS memetakan ke daftar RS tetangganya
JARINGAN_RS = {
    "Smart Hospital" : ["RS Medika", "RS Bunda", "RS Kasih"],
    "RS Medika"      : ["Smart Hospital", "RS Harapan"],
    "RS Bunda"       : ["Smart Hospital", "RS Sejahtera"],
    "RS Kasih"       : ["Smart Hospital", "RS Harapan", "RS Sejahtera"],
    "RS Harapan"     : ["RS Medika", "RS Kasih"],
    "RS Sejahtera"   : ["RS Bunda", "RS Kasih"],
}

# Status awal semua RS — bisa diubah saat runtime
STATUS_AWAL = {
    "Smart Hospital" : "Penuh",       # RS utama — selalu penuh saat cari rujukan
    "RS Medika"      : "Tersedia",
    "RS Bunda"       : "Tersedia",
    "RS Kasih"       : "Tersedia",
    "RS Harapan"     : "Tersedia",
    "RS Sejahtera"   : "Tersedia",
}


# ══════════════════════════════════════════════════════════════════════════════
# CLASS GRAPH RUJUKAN
# ══════════════════════════════════════════════════════════════════════════════

class GraphRujukan:
    """
    Merepresentasikan jaringan RS rujukan sebagai Graph dengan
    adjacency list, dilengkapi algoritma BFS untuk menemukan
    RS terdekat yang tersedia.
    """

    def __init__(self):
        # Adjacency list — struktur utama graph
        self.graph  = JARINGAN_RS

        # Status setiap RS — bisa berubah saat runtime
        self.status = STATUS_AWAL.copy()

    # ── SET STATUS RS ─────────────────────────────────────────────────────────

    def set_status(self, nama_rs, status):
        """
        Mengubah status sebuah RS.

        Args:
            nama_rs (str): Nama RS yang ingin diubah statusnya.
            status  (str): "Tersedia" atau "Penuh".

        Returns:
            bool: True jika berhasil, False jika nama RS tidak ada.
        """
        if nama_rs not in self.graph:
            print(f"  [ERROR] RS '{nama_rs}' tidak ada di jaringan.")
            return False

        if status not in ("Tersedia", "Penuh"):
            print(f"  [ERROR] Status harus 'Tersedia' atau 'Penuh'.")
            return False

        self.status[nama_rs] = status
        return True

    # ── BFS — CARI RS RUJUKAN TERDEKAT ───────────────────────────────────────

    def bfs_cari_rujukan(self, rs_asal="Smart Hospital"):
        """
        Mencari RS rujukan terdekat yang statusnya "Tersedia"
        menggunakan algoritma Breadth-First Search (BFS).

        Cara kerja BFS:
            1. Masukkan rs_asal ke dalam queue dan set visited
            2. Loop selama queue tidak kosong:
               a. Pop RS dari DEPAN queue (FIFO — ini yang membuat BFS berbeda dari DFS)
               b. Jika RS ini bukan rs_asal dan statusnya "Tersedia" → DITEMUKAN!
               c. Jika "Penuh", masukkan semua tetangganya yang belum dikunjungi
                  ke dalam queue
            3. Jika queue habis tanpa hasil → tidak ada RS yang tersedia

        Mengapa BFS menjamin RS terdekat:
            BFS menelusuri level demi level (1 hop dulu, baru 2 hop, baru 3 hop).
            RS pertama yang ditemukan pasti yang paling sedikit hop-nya dari rs_asal.

        Args:
            rs_asal (str): Nama RS yang membutuhkan rujukan.
                           Default: "Smart Hospital".

        Returns:
            dict: {
                "rs_tujuan" : nama RS rujukan yang ditemukan (atau None),
                "rute"      : list nama RS yang dilalui dari rs_asal ke rs_tujuan,
                "hop"       : jumlah langkah dari rs_asal ke rs_tujuan
            }
        """
        # Validasi rs_asal
        if rs_asal not in self.graph:
            return {"rs_tujuan": None, "rute": [], "hop": 0}

        # Queue BFS — gunakan deque untuk operasi popleft() O(1)
        # Setiap elemen di queue: (nama_rs, rute_yang_dilalui)
        queue   = deque()
        visited = set()

        # Inisialisasi BFS dari rs_asal
        queue.append((rs_asal, [rs_asal]))
        visited.add(rs_asal)

        # ── LOOP BFS ──────────────────────────────────────────────────────
        while queue:

            # Ambil RS dari DEPAN queue (FIFO)
            rs_sekarang, rute = queue.popleft()

            # Cek apakah RS ini (bukan rs_asal) statusnya Tersedia
            if rs_sekarang != rs_asal and self.status.get(rs_sekarang) == "Tersedia":
                # ✅ DITEMUKAN — ini RS terdekat yang tersedia
                return {
                    "rs_tujuan": rs_sekarang,
                    "rute"     : rute,
                    "hop"      : len(rute) - 1    # jumlah edge yang dilalui
                }

            # RS ini Penuh → tambahkan tetangganya ke queue
            for tetangga in self.graph.get(rs_sekarang, []):
                if tetangga not in visited:
                    visited.add(tetangga)
                    rute_baru = rute + [tetangga]
                    queue.append((tetangga, rute_baru))

        # Queue habis — tidak ada RS yang tersedia
        return {"rs_tujuan": None, "rute": [], "hop": 0}

    # ── TAMPILKAN PETA JARINGAN ───────────────────────────────────────────────

    def tampilkan_peta(self):
        """
        Menampilkan seluruh jaringan RS dalam format adjacency list
        beserta status masing-masing RS saat ini.
        """
        print("\n" + "=" * 52)
        print("       PETA JARINGAN RUMAH SAKIT RUJUKAN")
        print("       Struktur Data: Graph (Adjacency List)")
        print("=" * 52)

        for rs, tetangga in self.graph.items():
            status   = self.status.get(rs, "?")
            ikon     = "🔴" if status == "Penuh" else "🟢"
            koneksi  = " → ".join(tetangga)
            print(f"  {ikon} {rs:<18} : {koneksi}")

        print("=" * 52)
        print("\n  Keterangan Status:")
        print("  🟢 Tersedia  →  Bisa menerima pasien rujukan")
        print("  🔴 Penuh     →  Tidak bisa menerima pasien")

    # ── TAMPILKAN STATUS SEMUA RS ─────────────────────────────────────────────

    def tampilkan_status(self):
        """Menampilkan status (Tersedia/Penuh) semua RS."""
        print("\n  Status Rumah Sakit Saat Ini:")
        print("  " + "─" * 40)
        for rs, status in self.status.items():
            ikon = "🟢" if status == "Tersedia" else "🔴"
            print(f"  {ikon} {rs:<20} : {status}")

    # ── TAMPILKAN LANGKAH BFS ─────────────────────────────────────────────────

    def bfs_dengan_langkah(self, rs_asal="Smart Hospital"):
        """
        Versi BFS yang menampilkan proses pencariannya step by step.
        Berguna untuk demo/presentasi agar penguji bisa melihat
        algoritma BFS bekerja secara transparan.

        Args:
            rs_asal (str): RS asal pencarian.

        Returns:
            dict: Sama seperti return value bfs_cari_rujukan().
        """
        print(f"\n  [BFS] Mulai dari: {rs_asal}")
        print(f"  [BFS] Menelusuri RS tetangga level demi level...\n")

        if rs_asal not in self.graph:
            print(f"  [ERROR] RS '{rs_asal}' tidak ditemukan.")
            return {"rs_tujuan": None, "rute": [], "hop": 0}

        queue   = deque()
        visited = set()

        queue.append((rs_asal, [rs_asal]))
        visited.add(rs_asal)

        langkah = 0

        while queue:
            rs_sekarang, rute = queue.popleft()
            langkah += 1

            status_rs = self.status.get(rs_sekarang, "?")

            if rs_sekarang != rs_asal:
                print(f"  Langkah {langkah}: Memeriksa {rs_sekarang:<18} → {status_rs}")

            if rs_sekarang != rs_asal and status_rs == "Tersedia":
                rute_str = " → ".join(rute)
                print(f"\n  ✅ DITEMUKAN: {rs_sekarang}")
                print(f"  Rute  : {rute_str}")
                print(f"  Jarak : {len(rute)-1} hop")
                return {
                    "rs_tujuan": rs_sekarang,
                    "rute"     : rute,
                    "hop"      : len(rute) - 1
                }

            for tetangga in self.graph.get(rs_sekarang, []):
                if tetangga not in visited:
                    visited.add(tetangga)
                    queue.append((tetangga, rute + [tetangga]))

        print("\n  ❌ Semua RS penuh. Tidak ada rujukan tersedia.")
        return {"rs_tujuan": None, "rute": [], "hop": 0}


# ── FUNGSI CLI — DIPANGGIL DARI main.py ──────────────────────────────────────

def lihat_peta_rujukan():
    """Entry point CLI: tampilkan peta jaringan RS."""
    graph = GraphRujukan()
    graph.tampilkan_peta()
    graph.tampilkan_status()


def cari_rs_rujukan():
    """
    Entry point CLI: jalankan BFS untuk menemukan RS rujukan terdekat.
    Menampilkan proses BFS step by step untuk keperluan demo.
    """
    print("\n" + "=" * 52)
    print("       CARI RS RUJUKAN TERDEKAT")
    print("       Algoritma: BFS (Breadth-First Search)")
    print("=" * 52)

    graph = GraphRujukan()
    graph.tampilkan_peta()
    graph.tampilkan_status()

    print("\n" + "─" * 52)
    print("  Mencari RS rujukan dari Smart Hospital...\n")

    hasil = graph.bfs_dengan_langkah("Smart Hospital")

    if hasil["rs_tujuan"]:
        print("\n" + "=" * 52)
        print(f"  RS Rujukan  : {hasil['rs_tujuan']}")
        print(f"  Rute        : {' → '.join(hasil['rute'])}")
        print(f"  Jarak       : {hasil['hop']} hop dari Smart Hospital")
        print("=" * 52)
    else:
        print("\n" + "=" * 52)
        print("  [INFO] Tidak ada RS rujukan yang tersedia.")
        print("  Semua RS dalam jaringan sedang penuh.")
        print("=" * 52)


def ubah_status_rs():
    """Entry point CLI: ubah status Tersedia/Penuh sebuah RS."""
    graph = GraphRujukan()

    print("\n" + "=" * 52)
    print("         UBAH STATUS RUMAH SAKIT")
    print("=" * 52)
    graph.tampilkan_status()

    nama_rs = input("\n  Masukkan nama RS: ").strip()
    if nama_rs not in graph.graph:
        print(f"  [ERROR] RS '{nama_rs}' tidak ditemukan.")
        return

    print("  Pilih status baru:")
    print("    [1] Tersedia")
    print("    [2] Penuh")

    pilih = input("  Pilih [1/2]: ").strip()
    if pilih == "1":
        status = "Tersedia"
    elif pilih == "2":
        status = "Penuh"
    else:
        print("  [ERROR] Pilihan tidak valid.")
        return

    if graph.set_status(nama_rs, status):
        print(f"  [OK] Status {nama_rs} diubah menjadi '{status}'.")