"""
File    : modules/manage_rujukan.py
Materi  : Graph + BFS (Business Logic & CLI)
Deskripsi:
    Mengelola antarmuka pengguna (CLI) dan algoritma pencarian BFS
    untuk fitur jaringan rumah sakit rujukan.
Catatan :
    - Menggunakan struktur data Graph dari modules/graph_rujukan.py.
"""

from collections import deque
from modules.graph_rujukan import GraphRujukan


# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS LOGIC (ALGORITMA BFS DENGAN DEMO)
# ══════════════════════════════════════════════════════════════════════════════


def bfs_dengan_langkah(graph_obj, rs_asal="Smart Hospital"):
    """
    Versi BFS yang menampilkan proses pencariannya step by step
    untuk keperluan demo/presentasi.
    """
    print(f"\n  [BFS] Mulai dari: {rs_asal}")
    print(f"  [BFS] Menelusuri RS tetangga level demi level...\n")

    if rs_asal not in graph_obj.graph:
        print(f"  [ERROR] RS '{rs_asal}' tidak ditemukan.")
        return {"rs_tujuan": None, "rute": [], "hop": 0}

    queue = deque()
    visited = set()

    queue.append((rs_asal, [rs_asal]))
    visited.add(rs_asal)

    langkah = 0

    while queue:
        rs_sekarang, rute = queue.popleft()
        langkah += 1

        status_rs = graph_obj.status.get(rs_sekarang, "?")

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

        for tetangga in graph_obj.graph.get(rs_sekarang, []):
            if tetangga not in visited:
                visited.add(tetangga)
                queue.append((tetangga, rute + [tetangga]))

    print("\n  ❌ Semua RS penuh. Tidak ada rujukan tersedia.")
    return {"rs_tujuan": None, "rute": [], "hop": 0}


# ══════════════════════════════════════════════════════════════════════════════
# FUNGSI CLI & PRESENTATION
# ══════════════════════════════════════════════════════════════════════════════

def tampilkan_peta(graph_obj):
    """Menampilkan seluruh jaringan RS dalam format adjacency list."""
    print("\n" + "=" * 52)
    print("       PETA JARINGAN RUMAH SAKIT RUJUKAN")
    print("       Struktur Data: Graph (Adjacency List)")
    print("=" * 52)

    for rs, tetangga in graph_obj.graph.items():
        status   = graph_obj.status.get(rs, "?")
        koneksi  = " → ".join(tetangga)
        print(f"  - {rs:<18} : {koneksi} ({status})")

    print("=" * 52)
    print("\n  Keterangan Status:")
    print("  Tersedia  →  Bisa menerima pasien rujukan")
    print("  Penuh     →  Tidak bisa menerima pasien")


def tampilkan_status(graph_obj):
    """Menampilkan status (Tersedia/Penuh) semua RS."""
    print("\n  Status Rumah Sakit Saat Ini:")
    print("  " + "─" * 40)
    for rs, status in graph_obj.status.items():
        print(f"  - {rs:<20} : {status}")


# ── ENTRY POINTS UNTUK MAIN.PY ────────────────────────────────────────────────

def lihat_peta_rujukan():
    """Entry point CLI: tampilkan peta jaringan RS."""
    graph_obj = GraphRujukan()
    tampilkan_peta(graph_obj)
    tampilkan_status(graph_obj)


def cari_rs_rujukan():
    """Entry point CLI: jalankan BFS untuk menemukan RS rujukan terdekat."""
    print("\n" + "=" * 52)
    print("       CARI RS RUJUKAN TERDEKAT")
    print("       Algoritma: BFS (Breadth-First Search)")
    print("=" * 52)

    graph_obj = GraphRujukan()
    tampilkan_peta(graph_obj)
    tampilkan_status(graph_obj)

    print("\n" + "─" * 52)
    print("  Mencari RS rujukan dari Smart Hospital...\n")

    hasil = bfs_dengan_langkah(graph_obj, "Smart Hospital")

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
    graph_obj = GraphRujukan()

    print("\n" + "=" * 52)
    print("         UBAH STATUS RUMAH SAKIT")
    print("=" * 52)
    tampilkan_status(graph_obj)

    nama_rs = input("\n  Masukkan nama RS: ").strip()
    if nama_rs not in graph_obj.graph:
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

    if graph_obj.set_status(nama_rs, status):
        print(f"  [OK] Status {nama_rs} diubah menjadi '{status}'.")
