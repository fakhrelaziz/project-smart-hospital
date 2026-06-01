"""
File    : models/rumah_sakit.py
Materi  : Graph (Data)
Deskripsi:
    Menyimpan data statis Graph Jaringan Rumah Sakit dan statusnya.
Catatan :
    - Data ini diakses oleh class GraphRujukan.
"""

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
