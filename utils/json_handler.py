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
    try:
        with open(path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"  File '{path}' tidak ditemukan. Mengembalikan list kosong.")
        return []
    except json.JSONDecodeError:
        print(f"  ERROR: Format JSON pada '{path}' rusak atau tidak valid. Mengembalikan list kosong.")
        return []
    except Exception as e:
        print(f"  ERROR: Terjadi kesalahan saat membaca '{path}': {e}")
        return []


def save_json(path, data):
    """Menyimpan data ke file JSON pada path yang diberikan."""
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"  ERROR: Gagal menyimpan data ke '{path}': {e}")
        return False