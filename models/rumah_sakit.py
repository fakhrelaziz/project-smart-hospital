"""
Menyimpan data statis Graph Jaringan Rumah Sakit Rujukan sebagai adjacency list.
"""

# Adjacency List: setiap RS memetakan ke daftar RS tetangganya
JARINGAN_RS = {
    "Smart Hospital" : ["RS Medika", "RS Bunda", "RS Kasih"],
    "RS Medika"      : ["Smart Hospital", "RS Harapan"],
    "RS Bunda"       : ["Smart Hospital", "RS Sejahtera"],
    "RS Kasih"       : ["Smart Hospital", "RS Harapan", "RS Sejahtera"],
    "RS Harapan"     : ["RS Medika", "RS Kasih"],
    "RS Sejahtera"   : ["RS Bunda", "RS Kasih"],
}