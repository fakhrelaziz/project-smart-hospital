"""
File    : models/sistem_rs.py
Materi  : OOP (Application State)
Deskripsi:
    Class utama untuk menyimpan state global/in-memory (Application State)
    agar terhindar dari penggunaan variabel tingkat modul.
    Ini memastikan enkapsulasi yang baik saat instance dilempar via Dependency Injection.
"""

from modules.undo_stack import UndoStack

class SistemRS:
    """Menyimpan state global aplikasi agar tidak menggunakan variabel ditingkat modul."""
    def __init__(self):
        # Menyimpan tumpukan riwayat Undo untuk pendaftaran pasien
        self.stack_pendaftaran = UndoStack()
        
        # Menyimpan tumpukan riwayat Undo untuk triase UGD
        self.stack_triase = UndoStack()
