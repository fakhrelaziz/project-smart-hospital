from models.kamar import NavigasiKamar

class SistemRS:
    def __init__(self, objek_rumah_sakit):
        self.rumah_sakit = objek_rumah_sakit
        self.sistem_kamar = NavigasiKamar()

    def daftarkan_pasien_ke_kamar(self, objek_pasien, objek_kamar):
        objek_pasien.kamar = objek_kamar.nomor
        objek_kamar.pasien_terisi.append(objek_pasien.nama)
        print(f"{objek_pasien.nama} masuk ke Kamar {objek_kamar.nomor}")

    def pasien_tebus_obat(self, objek_pasien, objek_obat, jumlah):
        sukses = objek_obat.kurangStok(jumlah)
        if sukses:
            objek_pasien.rekam_medis.append(f"Menebus {jumlah} {objek_obat.nama}")
            print(f"{objek_pasien.nama} berhasil menebus {jumlah} {objek_obat.nama}")
        else:
            print(f"Stok {objek_obat.nama} tidak cukup")