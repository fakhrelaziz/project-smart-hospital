'''
file helper.py ini adalah untuk menyimpan struktur data dan fungsi-fungsi 
yang berhubungan dengan manajemen data pasien, seperti validasi NIK, penyimpanan profil 
pasien, dan lain-lain. 
tujuannya adalah membuat modul manajemen data pasien awal sebelum nanti dihubungkan 
ke sistem antrean.
'''

'''
TUPLE: Daftar layanan tetap
Tuple dipilih karena isi layanan TIDAK akan berubah saat program
berjalan. Berbeda dengan list, tuple bersifat immutable (tidak bisa
ditambah, dihapus, atau diubah nilainya).
'''

LAYANAN_TETAP = ("UGD", "Rawat Jalan", "Spesialis", "Rawat Inap", "Farmasi")



'''
SET: Kumolkan NIK pasien yang sudah terdaftar
Set dipilih karena kita hanya perlu menyimpan NIK secara unik tanpa urutan tertentu.
Set secara otomatis mencegah duplikasi, jadi kalau ada NIK yang sama dimasukkan
lagi, set tidak akan menambahnya dan kita bisa langsung tahu kalau NIK itu sudah terdaftar.
'''

nik_terdaftar = set()



'''
DICTIONARY: Menyimpan data profil pasien 
Dictionary dipilih karena kita ingin menyimpan data pasien dalam format yang terstruktur dan mudah diakses.
Kita bisa menggunakan NIK sebagai kunci utama untuk mengakses data profil pasien,
dan setiap profil pasien bisa berisi informasi seperti nama, umur, layanan yang dipilih, 
dan status pendaftaran.
 '''

profil_pasien = {}


#sekarang kita buat fungsi fungsinya

'''
FUNGSI: validasi_nik
Memeriksa apakah NIK sah sebelum pasien didaftarkan.
Aturan validasi:
  1. NIK tidak boleh kosong atau hanya spasi
  2. Panjang NIK minimal 5 karakter 
  3. NIK tidak boleh sudah ada di set nik_terdaftar
'''

def validasi_nik(nik: str):
    #menghapus spasi di awal/akhir inputan admin
    nik_baru = nik.strip() 

    #cek dulu apakah NIK kosong
    if not nik_baru:
        return False, "[SISTEM] ERROR: NIK tidak boleh kosong!"
        
    #cek apakah NIK terlalu pendek 
    #(Standar KTP Indonesia umumnya 16 digit, tapi kita buat batas minimal misal 5 digit aja)
    if len(nik_baru) < 5:
        return False, "[SISTEM] ERROR: NIK '{nik_baru}' terlalu pendek. Minimal 5 karakter."

    #cek apakah NIK sudah pernah terdaftar di dalam SET
    if nik_baru in nik_terdaftar:
        return False, "[SISTEM] ERROR: NIK '{nik_baru}' sudah terdaftar. Tidak boleh duplikat."
        
    #jika lolos semua pengecekan
    return True, "NIK Valid"



'''
FUNGSI: tambah_profil_pasien
Fungsi untuk menambah data pasien ke dalam SET dan DICTIONARY secara bersamaan.
Prosesnya:
  1. Jalankan fungsi validasi NIK terlebih dahulu
  2. Validasi tambahan: Pastikan pilihan layanan ada di dalam TUPLE LAYANAN_TETAP
  3. Masukkan NIK ke dalam SET nik_terdaftar
  4. Masukkan data profil ringkas ke dalam DICTIONARY profil_pasien dengan struktur:
     {
       "nama": nama,
       "umur": umur,
       "layanan": layanan,
       "status": "terdaftar"
     }
'''
'''
FUNGSI: tambah_profil_pasien
Fungsi buat masukin data pasien baru ke dalam set dan dictionary.
Sebelum disimpan, data NIK dan layanannya harus lolos validasi dulu.
'''
def tambah_profil_pasien(data_pasien: dict):
    #ambil NIK dari dictionary pasien secara manual
    if "nik" in data_pasien:
        nik_baru = data_pasien["nik"].strip() #hapus spasi di awal/akhir inputan NIK
    else:
        nik_baru = ""
    
    #kita validasi NIK nya dulu lewat fungsi validasi_nik
    is_valid, pesan = validasi_nik(nik_baru)
    if not is_valid:
        print(pesan)
        return False
        
    #ambil data layanan dan cek apakah ada di TUPLE LAYANAN_TETAP
    if "layanan" in data_pasien:
        layanan = data_pasien["layanan"]
    else:
        layanan = "" 
        #kalau layanan gak diisi, kita set jadi string kosong biar nanti validasi layanan nya gagal

    #validasi layanannya
    if layanan not in LAYANAN_TETAP:
        print(f"[SISTEM] ERROR: Layanan '{layanan}' tidak tersedia di rumah sakit ini!")
        return False
        
    #kalau lolos validasi, baru kita simpan ke SET dan DICTIONARY
    nik_terdaftar.add(nik_baru)
    
    #ambil nama dan umur buat dimasukin ke profil_pasien
    nama_pasien = data_pasien["nama"] if "nama" in data_pasien else "Tanpa Nama"
    umur_pasien = data_pasien["umur"] if "umur" in data_pasien else 0
    
    #kita buat struktur data profil pasien yang rapi di dalam DICTIONARY
    profil_pasien[nik_baru] = {
        "nama"    : nama_pasien,
        "umur"    : umur_pasien,
        "layanan" : layanan,
        "status"  : "terdaftar"
    }
    
    print(f"[Sistem] Berhasil mendaftarkan profil pasien: {nama_pasien} ({nik_baru}).")
    return True


'''
fungsi untuk menampilkan profil pasien berdasarkan NIK yang dimasukkan.
prosesnya:
  1. Bersihkan input NIK dari spasi
  2. Cek apakah NIK ada di dalam DICTIONARY profil_pasien
  3. Jika ada, tampilkan detail profil pasien dengan format yang rapi
  4. Jika tidak ada, tampilkan pesan error bahwa profil pasien tidak ditemukan
'''
def tampilkan_profil_pasien(nik: str):
    nik_baru = nik.strip()
    
    if nik_baru in profil_pasien:
        profil = profil_pasien[nik_baru]
        print(f"Profil Pasien NIK: {nik_baru}")
        print(f"Nama: {profil['nama']}")
        print(f"Umur: {profil['umur']} tahun")
        print(f"Layanan: {profil['layanan']}") 
        print(f"Status: {profil['status'].upper()}\n") #.upper() biar statusnya tampil dalam huruf kapital
    else:
        print(f"[Sistem] ERROR: Profil pasien dengan NIK '{nik_baru}' tidak ditemukan!")




#Demo penggunaan fungsi fungsi di atas
if __name__ == "__main__":
    print("=== Demo modules/helper.py ===\n")

    #1. Tes Pendaftaran Pasien
    print("--- 1. TES PENDAFTARAN PASIEN ---")
    print("1. Mendaftarkan Pasien Pertama...")
    pasien1 = {
        "nik": "123456", 
        "nama": "Jokowi", 
        "umur": 25, 
        "layanan": "UGD"
    }
    #ini kita kiri dictionary 'pasien1' ke fungsi
    tambah_profil_pasien(pasien1)

    print("\n2. Mendaftarkan Pasien Kedua...")
    pasien2 = {
        "nik": "789012", 
        "nama": "Prabowo", 
        "umur": 19, 
        "layanan": "Spesialis"
    }
    tambah_profil_pasien(pasien2)


    #2. Tes Validasi Kalau Input Error 
    print("\n 2. --- Tes Validasi Input Error ---")
    #kita coba mendaftarkan Anies menggunakan NIK milik Jokowi (123456)
    pasien3 = {
        "nik": "123456",  #NIK Duplikat
        "nama": "Anies", 
        "umur": 30, 
        "layanan": "Farmasi"
    }
    tambah_profil_pasien(pasien3)


    #3. Tes Validasi Kalau Layanan Salah
    print("\n3. --- Tes Input Layanan Salah ---")
    #kita coba mendaftarkan Megawati dengan layanan yang tidak ada di LAYANAN_TETAP
    pasien4 = {
        "nik": "555555", 
        "nama": "Megawati", 
        "umur": 40, 
        "layanan": "Dukun Sakti"  #layanan salah
    }
    tambah_profil_pasien(pasien4)


    #4. Menamoilkan Hasil Pendaftaran Pasien
    print("\n4. --- Tampilkan Isi Profil Pasien ---")
    tampilkan_profil_pasien("123456")  #memanggil profil Jokowi
    tampilkan_profil_pasien("789012")  #memanggil profil Prabowo
    tampilkan_profil_pasien("345678")  #memanggil profil tanpa nama


    #5. Tes Cari NIK Yang Tidak Terdaftar
    print("\n5. --- Tes Cari NIK Yang Tidak Terdaftar ---")
    tampilkan_profil_pasien("999999")