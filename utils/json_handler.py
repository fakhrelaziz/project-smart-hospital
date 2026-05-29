"""
File    : utils/json_handler.py
Deskripsi: Utilitas baca dan tulis file JSON untuk sistem Smart Hospital.
Tujuan  : Menyediakan fungsi terpusat untuk membaca dan menyimpan data
           ke file JSON agar tidak ada duplikasi kode I/O di seluruh modul.
Catatan :
    - Selalu menggunakan encoding UTF-8 agar karakter khusus tersimpan dengan benar.
    - Semua data disimpan dengan indentasi 4 spasi untuk kemudahan debugging.
Relasi  :
    - Digunakan oleh hampir semua modul di modules/ yang membutuhkan persistensi data.
"""

import json


def load_json(path):
    """Membaca file JSON dari path yang diberikan dan mengembalikan datanya.

    Args:
        path (str): Path relatif atau absolut ke file JSON.

    Returns:
        list | dict: Data yang terbaca dari file JSON.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json(path, data):
    """Menyimpan data ke file JSON pada path yang diberikan.

    Args:
        path (str): Path relatif atau absolut ke file JSON tujuan.
        data (list | dict): Data yang akan disimpan ke file.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)