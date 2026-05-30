"""
File    : utils/json_handler.py
Deskripsi: Utilitas baca dan tulis file JSON untuk sistem Smart Hospital.
Tujuan  : Menyediakan fungsi terpusat untuk membaca dan menyimpan data
           ke file JSON agar tidak ada duplikasi kode I/O di seluruh modul.
Catatan :
    - Semua data disimpan dengan indentasi 4 spasi untuk kemudahan debugging.
Relasi  :
    - Digunakan oleh hampir semua modul di modules/ yang membutuhkan persistensi data.
"""

import json


def load_json(path):
    """Membaca file JSON dari path yang diberikan dan mengembalikan datanya."""
    with open(path, "r") as file:
        data = json.load(file)
    return data


def save_json(path, data):
    """Menyimpan data ke file JSON pada path yang diberikan."""
    with open(path, "w") as file:
        json.dump(data, file, indent=4)