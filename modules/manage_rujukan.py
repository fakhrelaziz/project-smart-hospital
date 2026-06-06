from collections import deque
from modules.graph_rujukan import GraphRujukan


def bfs_dengan_langkah(graph_obj, rs_asal="Smart Hospital"):
    """
    Versi BFS yang menampilkan proses pencariannya step by step,
    dengan mendelegasikan logika pencarian ke class GraphRujukan.
    """
    print(f"\n  Mulai dari: {rs_asal}")
    print(f"  Menelusuri RS tetangga level demi level...\n")

    if rs_asal not in graph_obj.graph:
        print(f"  ERROR: RS '{rs_asal}' tidak ditemukan.")
        return {"rs_tujuan": None, "rute": [], "hop": 0}

    # Panggil logika inti
    hasil = graph_obj.bfs_cari_rujukan(rs_asal)

    # Cetak history langkah yang dikunjungi oleh BFS
    if "history" in hasil:
        for i in range(len(hasil["history"])):
            rs_sekarang, status_rs = hasil["history"][i]
            print(f"  Langkah {i + 1}: Memeriksa {rs_sekarang:<18} → {status_rs}")

    if hasil["rs_tujuan"]:
        rute_str = " → ".join(hasil["rute"])
        print(f"\n   DITEMUKAN: {hasil['rs_tujuan']}")
        print(f"  Rute  : {rute_str}")
        print(f"  Jarak : {hasil['hop']} hop")
    else:
        print("\n   Semua RS penuh. Tidak ada rujukan tersedia.")

    return hasil


def tampilkan_peta(graph_obj):
    """Menampilkan seluruh jaringan RS dalam format adjacency list."""
    print("\n" + "=" * 52)
    print("       PETA JARINGAN RUMAH SAKIT RUJUKAN")
    print("=" * 52)

    for i, tetangga in graph_obj.graph.items():
        status   = graph_obj.status.get(i, "?")
        koneksi  = " → ".join(tetangga)
        print(f"  - {i:<18} : ({status}) {koneksi}")

    print("=" * 52)
    print("\n  Keterangan Status:")
    print("  Tersedia  →  Bisa menerima pasien rujukan")
    print("  Penuh     →  Tidak bisa menerima pasien")


def tampilkan_status(graph_obj):
    """Menampilkan status (Tersedia/Penuh) semua RS."""
    print("\n  Status Rumah Sakit Saat Ini:")
    print("  " + "─" * 40)
    for i, status in graph_obj.status.items():
        print(f"  - {i:<20} : {status}")


def lihat_peta_rujukan():
    """Entry point CLI: tampilkan peta jaringan RS."""
    graph_obj = GraphRujukan()
    tampilkan_peta(graph_obj)
    tampilkan_status(graph_obj)


def cari_rs_rujukan():
    """Entry point CLI: jalankan BFS untuk menemukan RS rujukan terdekat."""
    print("\n" + "=" * 52)
    print("       CARI RS RUJUKAN TERDEKAT")
    print("=" * 52)

    graph_obj = GraphRujukan()
    tampilkan_peta(graph_obj)
    tampilkan_status(graph_obj)

    print("\n" + "─" * 52)
    print("   Mencari RS rujukan dari Smart Hospital...\n")

    hasil = bfs_dengan_langkah(graph_obj, "Smart Hospital")

    if hasil["rs_tujuan"]:
        print("\n" + "=" * 52)
        print(f"   RS Rujukan  : {hasil['rs_tujuan']}")
        print(f"   Rute        : {' → '.join(hasil['rute'])}")
        print(f"   Jarak       : {hasil['hop']} hop dari Smart Hospital")
        print("=" * 52)
    else:
        print("\n" + "=" * 52)
        print("  Tidak ada RS rujukan yang tersedia.")
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
        print(f"  ERROR: RS '{nama_rs}' tidak ditemukan.")
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
        print("  ERROR: Pilihan tidak valid.")
        return

    if graph_obj.set_status(nama_rs, status):
        print(f"  Status {nama_rs} diubah menjadi '{status}'.")
