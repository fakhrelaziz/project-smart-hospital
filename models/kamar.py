"""
Materi  : OOP — Class Model Kamar
Deskripsi:
    Mendefinisikan class Kamar sebagai representasi data kamar rawat inap, jadi ini tempat manipulasi data kamar.
    Mendukung kamar dengan kapasitas tunggal maupun multi-kasur.
Catatan :
    - Konversi dict → objek menggunakan dict_ke_objek(), ini untuk mengubah dictionary pada json 
    menjadi objek python agar lebih enak di manipulasi karena sudah berbentuk objek, jadi setiap data kamar.json
    di panggil dengan menggunakan looping untuk membuat objek nya dengan Blueprint Kamwr atau class Kamar
    
    - Konversi objek → dict menggunakan objek_ke_dict() untuk serialisasi ke JSON. 
    setelah data diubah ke objek dan saat menjalankan program misal ingin memasukkan pasien ke kamar 
    setelah dimasukkan sebelum data terbaru disimpan ke .json dari objek iti diubah dulu ke format dictionary, kemudian 
    disimpan dengan memanggil fungsi save_json pada file json_handler.py
    - Kapasitas kasur otomatis ditentukan berdasarkan tipe kamar saat dict_ke_objek().
Relasi  :
    - Digunakan oleh modules/manage_kamar.py dan modules/dll_kamar.py.
"""


class Kamar:
    def __init__(self, nomor, tipe, pasien_terisi=None, kapasitas_kasur=1):
        self.nomor = nomor
        self.tipe = tipe
        self.kapasitas_kasur = kapasitas_kasur 
        
        if pasien_terisi is False or pasien_terisi is None:
            self.pasien_terisi = []
        elif isinstance(pasien_terisi, list):
            self.pasien_terisi = pasien_terisi
        else:
            # Jika isinya berupa 1 string NIK, konversikan ke dalam list
            self.pasien_terisi = [pasien_terisi]

    def data_kamar(self):        
        """Mengembalikan string representasi data kamar untuk ditampilkan di CLI."""
        if not self.pasien_terisi:
            daftar_pasien = "-"
        else:
            daftar_pasien = ""
            for p in self.pasien_terisi:
                if daftar_pasien == "":
                    daftar_pasien += p
                else:
                    daftar_pasien += ", " + p
                    
        return f"[Kamar {self.nomor}]\n | Tipe     : {self.tipe}\n | Status   : {self.status_kamar()}\n | Kapasitas: {len(self.pasien_terisi)}/{self.kapasitas_kasur} terisi\n | Pasien   : {daftar_pasien}"

    def objek_ke_dict(self):
        """Mengubah objek Kamar menjadi dictionary untuk serialisasi ke JSON."""
        return {
            "nomor": self.nomor,
            "tipe": self.tipe,
            "status": self.status_kamar(),
            "kapasitas_kasur": self.kapasitas_kasur,
            "pasien_terisi": self.pasien_terisi
        }

    def dict_ke_objek(self, data):
        """Memuat atribut objek Kamar dari dictionary hasil baca JSON."""
        self.nomor = data.get('nomor')
        self.tipe = data.get('tipe')
        self.kapasitas_kasur = data.get('kapasitas_kasur', 1)
        
        pasien_terisi = data.get('pasien_terisi', [])
        # Fallback jaga-jaga apabila ada data lama
        if not pasien_terisi:
            self.pasien_terisi = []
        elif isinstance(pasien_terisi, list):
            self.pasien_terisi = pasien_terisi
        else:
            self.pasien_terisi = [pasien_terisi]

    def status_kamar(self):
        jumlah_pasien = len(self.pasien_terisi)

        if jumlah_pasien == 0:
            return "Kosong"
        elif jumlah_pasien < self.kapasitas_kasur:
            return "Terisi"
        else:
            return "Penuh"

    def pasien_masuk(self, pasien):
        """Memasukkan pasien ke kamar jika masih ada kapasitas yang tersedia."""
        if len(self.pasien_terisi) < self.kapasitas_kasur:
            self.pasien_terisi.append(pasien)
            return True
        else:
            print(f"Kamar {self.nomor} sudah penuh!")
            return False

    def pasien_keluar(self, pasien):
        """Mengeluarkan pasien dari kamar dan memperbarui status ketersediaan."""
        if pasien in self.pasien_terisi:
            self.pasien_terisi.remove(pasien)
            print(f"Pasien keluar dari Kamar {self.nomor}")
        else:
            print("Pasien tidak ditemukan di kamar ini.")
