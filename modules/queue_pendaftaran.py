"""
Mengimplementasikan struktur data Queue untuk mengelola
antrian pendaftaran pasien. Pasien yang datang lebih dulu dilayani
lebih dulu (FIFO).
"""

class QueuePendaftaran:
    def __init__(self, data=None):
        self.items = list(data) if data else []

    def enqueue(self, pasien):
        """method untuk memasukkan data pasien yang baru didaftarkan ke stuktur data queue."""
        #validasi apakah data yang masuk beupa dict dan ada key 'nik
        if not pasien.get("nik"):
            print("ERROR: data pasien harus memiliki key 'nik'.")
            return False

        self.items.append(pasien)
        print(f" '{pasien.get('nama', pasien['nik'])}' "
              f"masuk antrean. Posisi: {len(self.items)}")
        return True

    def dequeue(self):
        """Mengambil dan menghapus pasien pertama antri."""
        #manggil method cek_antrian_kosong untuk cek antrian jika kosong
        if self.cek_antrian_kosong():
            print(" Antrean kosong. Tidak ada pasien untuk diproses.")
            return None

        pasien = self.items.pop(0)
        print(f" '{pasien.get('nama', pasien['nik'])}' "
              f"keluar dari antrean untuk dilayani.")
        return pasien


    def cek_antrian_kosong(self):
        """Mengecek apakah antrian sedang kosong."""
        return len(self.items) == 0

    def jmlh_antrian_pasien(self):
        """Mengembalikan jumlah pasien yang sedang dalam antrian."""
        return len(self.items)

    def tampilkan_antrian(self):
        """Menampilkan seluruh isi antrean secara terurut dari depan."""
        if self.cek_antrian_kosong():
            print("Antrean saat ini kosong.")
            return
        print(f"Jumlah Antrean ({self.jmlh_antrian_pasien()} pasien)")

        # Menampilkan NIK, nama, dan layanan pasien dalam antrian
        nomor_urut = 1
        for p in self.items:
            nik_pasien = p["nik"] if "nik" in p else "-"
            nama_pasien = p["nama"] if "nama" in p and p["nama"] else "-"
            layanan_pasien = p["layanan"] if "layanan" in p and p["layanan"] else "-"
            
            print(f"  {nomor_urut}. NIK: {nik_pasien} | "
                  f"Nama: {nama_pasien} | "
                  f"Layanan: {layanan_pasien}")
            nomor_urut += 1

