"""
File    : models/kamar.py
Materi  : OOP — Class Model Kamar
Deskripsi:
    Mendefinisikan class Kamar sebagai representasi data kamar rawat inap.
    Mendukung kamar dengan kapasitas tunggal maupun multi-kasur.
Catatan :
    - Konversi dict → objek menggunakan dict_ke_objek(), bukan constructor langsung.
    - Konversi objek → dict menggunakan objek_ke_dict() untuk serialisasi ke JSON.
    - Kapasitas kasur otomatis ditentukan berdasarkan tipe kamar saat dict_ke_objek().
Relasi  :
    - Digunakan oleh modules/manage_kamar.py dan modules/dll_kamar.py.
"""


class Kamar:
    def __init__(self, nomor, tipe, status="tersedia", pasien_terisi=None, kapasitas_kasur=1):
        self.nomor = nomor
        self.tipe = tipe
        self.status = status          
        self.kapasitas_kasur = kapasitas_kasur 
        
        if pasien_terisi is False or pasien_terisi is None:
            self.pasien_terisi = []
        elif isinstance(pasien_terisi, list):
            self.pasien_terisi = pasien_terisi
        else:
            # Jika isinya berupa 1 string NIK, konversikan ke dalam list
            self.pasien_terisi = [pasien_terisi]

    def data_kamar(self):
        daftar_pasien = ", ".join(self.pasien_terisi) if self.pasien_terisi else "Kosong"
        return f"[Kamar {self.nomor}] Tipe: {self.tipe} | Status: {self.status} | Terisi: {daftar_pasien}"

    def objek_ke_dict(self):
        """Mengubah objek Kamar menjadi dictionary untuk serialisasi ke JSON.
        
        Format pasien_terisi disesuaikan dengan skema kamar.json:
        - Kamar kosong → False
        - Kamar kapasitas 1 dengan 1 pasien → string NIK
        - Kamar multi-kasur → list NIK
        """
        pt_export = False
        if len(self.pasien_terisi) > 0:
            if self.kapasitas_kasur == 1:
                pt_export = self.pasien_terisi[0]
            else:
                pt_export = self.pasien_terisi
                
        return {
            "nomor": self.nomor,
            "tipe": self.tipe,
            "status": self.status,
            "pasien_terisi": pt_export
        }

    def dict_ke_objek(self, data):
        """Memuat atribut objek Kamar dari dictionary hasil baca JSON.
        
        Kapasitas kasur ditentukan otomatis berdasarkan tipe kamar
        karena field ini tidak disimpan di kamar.json.
        """
        kapasitas = 1
        if data.get("tipe") == "Umum":
            kapasitas = 2
        elif data.get("tipe") == "UGD":
            kapasitas = 4
        self.nomor = data.get('nomor')
        self.tipe = data.get('tipe')
        self.status = data.get('status', 'Tersedia')
        
        pasien_terisi = data.get('pasien_terisi', False)
        if pasien_terisi is False or pasien_terisi is None:
            self.pasien_terisi = []
        elif isinstance(pasien_terisi, list):
            self.pasien_terisi = pasien_terisi
        else:
            # Jika isinya berupa 1 string NIK, konversikan ke dalam list
            self.pasien_terisi = [pasien_terisi]
            
        self.kapasitas_kasur = kapasitas

    def status_kamar(self):
        jumlah_pasien = len(self.pasien_terisi)

        if jumlah_pasien == 0:
            return "Kosong"
        elif jumlah_pasien < self.kapasitas_kasur:
            kasur_sisa = self.kapasitas_kasur - jumlah_pasien
            return f"Ada {kasur_sisa} kasur kosong"
        else:
            return "Penuh"

    def pasien_masuk(self, pasien):
        """Memasukkan pasien ke kamar jika masih ada kapasitas yang tersedia."""
        if len(self.pasien_terisi) < self.kapasitas_kasur:
            self.pasien_terisi.append(pasien)
            
            # Update status jika setelah pasien masuk, kamar menjadi penuh
            if len(self.pasien_terisi) >= self.kapasitas_kasur:
                self.status = "terisi"
            
            return True
        else:
            print(f"Kamar {self.nomor} sudah penuh!")
            return False

    def pasien_keluar(self, pasien):
        """Mengeluarkan pasien dari kamar dan memperbarui status ketersediaan."""
        if pasien in self.pasien_terisi:
            self.pasien_terisi.remove(pasien)
            print(f"Pasien keluar dari Kamar {self.nomor}")
            
            # Update status kamar jika setelah pasien keluar, kapasitas tidak penuh
            if len(self.pasien_terisi) < self.kapasitas_kasur:
                self.status = "tersedia"
        else:
            print("Pasien tidak ditemukan di kamar ini.")