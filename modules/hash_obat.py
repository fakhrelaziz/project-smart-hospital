'''
Cara kerja Hash Table:
1. Kode obat (string) dimasukkan ke fungsi hash -> menghasilkan angka indeks (0 s.d. ukuran_tabel - 1).
2. Data obat disimpan secara instan di dalam slot indeks tersebut menggunakan Key.
3. Pencarian: hash(kode) -> langsung tembak Key di dalam slot -> O(1) mutlak tanpa looping.

Collision Handling — Dictionary Chaining:
   Jika dua kode menghasilkan indeks yang sama (tabrakan), keduanya otomatis 
   mengelompok di dalam satu Dictionary yang sama pada slot tersebut.

Struktur slot setelah insert: 
    self._tabel[5] = {
       "OBT001": {"nama": "Paracetamol", "stok": 50, ...},
       "OBT011": {"nama": "Amoxicillin",  "stok": 30, ...}   <- collision tetap O(1)
   }
'''


class HashObat:
    def __init__(self, ukuran = 20): #disini ukuran default kita buat 20, bisa diubah sesuai kebutuhan
        #1. Menentukan ukuran slot lemari apotek
        self._ukuran = ukuran
        
        #2. Setiap slot diisi Dictionary kosong {} untuk wadah obat yang tabrakan (Chaining)
        self._tabel = [{} for _ in range(ukuran)]

        #3. Pengingat jumlah total seluruh obat yang sukses tersimpan di dalam lemari
        self._total_obat = 0


    '''
    _fungsi_hash_manual — Fungsi hash manual
    Menjumlahkan nilai ASCII setiap karakter kode, lalu modulo ukuran.
    Contoh: "OBT001"
      O=79, B=66, T=84, 0=48, 0=48, 1=49
      total = 374  →  374 % 20 = 14  →  slot 14
    '''

    def hash_function(self, kode_obat):
        #4. Rumus standar: jumlah ASCII huruf di-modulo ukuran lemari
        total_ascii = 0
        #itung nilai huruf dari kode obatnya satu-satu
        for karakter in kode_obat:
            total_ascii += ord(karakter)  #mengubah huruf jadi angka angka satu-satu
        return total_ascii % self._ukuran  #sisa bagi biar hasilnya pas dengan nomor slot lemari

    '''
    insert — Menambah atau memperbarui obat
    Menyimpan detail obat.
        Jika kode sudah ada → data diperbarui (update).
        Jika belum ada → data baru ditambahkan.
        detail_obat minimal berisi: nama, kategori, stok, harga
    '''
    def insert(self, kode_obat, detail_obat):
        #5. Memasukkan atau memperbarui data obat lama langsung ke slot yang ditentukan oleh fungsi hash
        index = self.hash_function(kode_obat)  #kita cari lokasi slotnya dulu
        
        #cek dulu, kalau kodenya belum pernah ada di slot ini, berarti statusnya obat baru
        if kode_obat not in self._tabel[index]:
            self._total_obat += 1
            
        #langsung simpan/timpa ke dalam dictionary slot tujuan secara diam-diam
        self._tabel[index][kode_obat] = detail_obat


    '''
    get — Mencari detail obat berdasarkan kode
    Mencari detail obat berdasarkan kode.
    Langsung menuju slot yang ditentukan oleh fungsi hash.
    Mengembalikan detail obat jika ditemukan, atau None jika tidak ada.
    '''
    def get(self, kode_obat):
        #6. Mencari detail obat secara cepat dengan langsung menuju slot yang ditentukan oleh fungsi hash
        index = self.hash_function(kode_obat)  #cari langsung lokasi slotnya
        
        #bbuka pintu slotnya, langsung panggil kodenya (kalau gak ada, komputer ngasih None)
        return self._tabel[index].get(kode_obat, None)
    

    '''
    sebenarnya fungsi get() di atas sudah cukup buat cari detail obat, 
    tapi kami buat fungsi tambahan yang lebih user-friendly buat 
    cetak detail obatnya dengan format yang rapi dan mudah dibaca.
    jadi untuk get() itu tetap fokus ke proses pencarian data, 
    sementara cetak_obat() fokus ke proses menampilkan data obatnya.
    '''
    def cetak_obat(self, detail):
        if detail is None :
            print("Obat tidak ditemukan.")
        else:
            print(f"\n  • Nama     : {detail.get('nama')}")
            print(f"  • Kategori : {detail.get('kategori')}")
            print(f"  • Stok     : {detail.get('stok')}")
            print(f"  • Harga    : Rp{detail.get('harga')}")