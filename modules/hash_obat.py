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

    def _fungsi_hash_manual(self, kode_obat):
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
        index = self._fungsi_hash_manual(kode_obat)  #kita cari lokasi slotnya dulu
        
        #cek dulu, kalau kodenya belum pernah ada di slot ini, berarti statusnya obat baru
        if kode_obat not in self._tabel[index]:
            self._total_obat += 1
            status_aksi = "menambahkan obat baru"
        else:
            status_aksi = "memperbarui data obat"
            
        #langsung simpan/timpa ke dalam dictionary slot tujuan
        self._tabel[index][kode_obat] = detail_obat
        print(f"[SISTEM] Sukses {status_aksi} '{kode_obat}' di slot {index}.")


    '''
    get — Mencari detail obat berdasarkan kode
    Mencari detail obat berdasarkan kode.
    Langsung menuju slot yang ditentukan oleh fungsi hash.
    Mengembalikan detail obat jika ditemukan, atau None jika tidak ada.
    '''
    def get(self, kode_obat):
        #6. Mencari detail obat secara cepat dengan langsung menuju slot yang ditentukan oleh fungsi hash
        index = self._fungsi_hash_manual(kode_obat)  #cari langsung lokasi slotnya
        
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



    '''
    update_stok — Memperbarui stok obat
    Memperbarui jumlah stok obat berdasarkan kode.
    Mengembalikan True jika berhasil, False jika gagal.
    '''
    def update_stok(self, kode_obat, stok_baru):
        #7. Memperbarui angka stok kalau ada transaksi obat terjual atau obat datang
        if stok_baru <= 0:
            print("[Sistem] ERROR: Jumlah stok obat tidak boleh nol atau minus!")
            return False
        
        #kita pakai fungsi get() yang udah kita buat untuk memastikan obatnya emang ada di lemari
        detail_stok = self.get(kode_obat)
        if detail_stok:
            stok_lama = detail_stok["stok"]
            detail_stok["stok"] = stok_baru  #ganti nilai stok lamanya pake angka baru
            print(f"[Sistem] Stok '{kode_obat}' berhasil diubah: {stok_lama} -> {stok_baru}.")
            return True
        
        print(f"[Sistem] Gagal Update Stok: Obat '{kode_obat}' tidak ditemukan!")
        return False
    

    '''
    delete — Menghapus obat berdasarkan kode
    Menghapus data obat dari dalam slot.
    Mengembalikan True jika berhasil dihapus, False jika kode tidak ditemukan.
    '''
    def delete(self, kode_obat):
        #8. Menghapus data obat dari dalam slot lemari berdasarkan kode obatnya
        #cari lokasi slot lemarinya dulu lewat fungsi hash
        index = self._fungsi_hash_manual(kode_obat)
        
        #cek apakah kode obat tersebut emang ada di dalam slot Dictionary itu
        if kode_obat in self._tabel[index]:
            #hapus datanya langsung dari dictionary menggunakan perintah 'del' bawaan Python
            del self._tabel[index][kode_obat]
            self._total_obat -= 1 #kurangi catatan total obat di lemari
            print(f"[SISTEM] Sukses menghapus obat '{kode_obat}' dari slot {index}.")
            return True
            
        print(f"[SISTEM] Gagal menghapus, obat '{kode_obat}' tidak ditemukan!")
        return False
    

    '''
    display — Menampilkan isi hash table (untuk demo / presentasi)
    '''
    def display(self):
        #9. Baru kita cetak visual lemari untuk demo presentasi kelompok 11 mantap
        print(f"\n===== KATALOG APOTEK SMART HOSPITAL (Total Obat: {self._total_obat}) =====")
        

        #kita iterasi SEMUA slot tanpa terkecuali (0 sampai ukuran-1)
        for i in range(self._ukuran):
            slot = self._tabel[i]

            if slot: #kalau slot ada isinya (Dictionary tidak kosong)
                #ini kita buat variabel pembantu untuk menandai apakah nomor slot sudah dicetak atau belum
                slot_sudah_dicetak = False
                
                for kode, detail in slot.items(): #kode obat dan detailnya kita cetak satu-satu
                    if not slot_sudah_dicetak: #kalau nomor slot belum dicetak
                        #cetak obat pertama lengkap dengan nomor slotnya
                        print(f"  Slot [{i}] -> Kode: {kode} | Nama: {detail['nama']} | Stok: {detail['stok']} | Harga: Rp{detail['harga']}")
                        slot_sudah_dicetak = True
                    else:
                        #kalau ada obat kedua dst di slot yang sama (collision/tabrakan), 
                        #nomor slotnya dikosongkan (diganti spasi) biar sejajar rapi ke bawah
                        spasi_sejajar = " " * len(f"  Slot [{i}] -> ")
                        print(f"{spasi_sejajar}Kode: {kode} | Nama: {detail['nama']} | Stok: {detail['stok']} | Harga: Rp{detail['harga']}")
            else: 
                #kalau slot kosong (Dictionary kosong {})
                print(f"  Slot [{i}] -> [Kosong]")

       


    '''
    to_list — Mengonversi Hash Table menjadi List biasa
    berguna buat dikirim ke file JSON biar data obat gak hilang saat aplikasi ditutup.
    '''
    def to_list(self):
        kumpulan_obat = []
        
        #bongkar seluruh slot lemari satu per satu
        for slot in self._tabel:
            if slot: #kalau slotnya ada isinya
                for kode_obat, detail_obat in slot.items():
                    #kita gabungkan kode obat dan detailnya menjadi satu struktur rapi
                    data_obat = {
                        "kode": kode_obat,
                        "nama": detail_obat.get("nama"),
                        "kategori": detail_obat.get("kategori"),
                        "stok": detail_obat.get("stok"),
                        "harga": detail_obat.get("harga")
                    }
                    kumpulan_obat.append(data_obat)
                    
        return kumpulan_obat #mengembalikan list bersih berisi semua obat


    '''
    from_list — Memasukkan kembali kumpulan data List ke dalam Hash Table
    Dipakai saat aplikasi baru dibuka, buat nge-load data lama dari file JSON.
    '''
    def from_list(self, list_data):
        if not list_data:
            return
            
        #ambil data obat dari list satu per satu
        for data in list_data:
            kode_obat = data.get("kode")
            
            #pisahkan detail obatnya ke dalam dictionary tersendiri
            detail_obat = {
                "nama": data.get("nama"),
                "kategori": data.get("kategori"),
                "stok": data.get("stok"),
                "harga": data.get("harga")
            }
            
            #masukkan kembali secara otomatis lewat fungsi insert kita yang super aman
            if kode_obat:
                self.insert(kode_obat, detail_obat)