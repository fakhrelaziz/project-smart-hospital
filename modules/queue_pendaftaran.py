class QueuePendaftaran:
    def __init__(self):  
        self._items: list = []  #kita buat list kosong untuk menyimpan data pasien yang masuk antrean


    def enqueue(self, pasien: dict):
        #validasi 1: memastikan data yang dikirim wajib berbentuk Dictionary {}
        if not isinstance(pasien, dict):
            print("[SISTEM] ERROR: pasien harus berupa dictionary.")
            return False
        
        #validasi 2: memastikan di dalam dictionary wajib ada kunci (key) 'nik'
        if not pasien.get("nik"):
            print("[SISTEM] ERROR: data pasien harus memiliki key 'nik'.")
            return False

        #masukkan pasien ke antrean (append ke akhir list)
        self._items.append(pasien)

        #print notifikasi masuk antrean dengan nama pasien (jika ada) atau NIK sebagai fallback
        print(f"[SISTEM] '{pasien.get('nama', pasien['nik'])}' "
              f"masuk antrean. Posisi: {len(self._items)}")
        return True


    def dequeue(self):
        '''
        mengambil dan menghapus pasien paling depan.
        mengembalikan dict pasien, atau None jika antrean kosong.
        '''

        #cek dulu apakah antrean kosong sebelum melakukan penghapusan
        if self.cek_antrian_kosong():
            print("[SISTEM] Antrean kosong. Tidak ada pasien untuk diproses.")
            return None

        # .pop(0) ini untuk mengambil sekaligus menghapus elemen di indeks ke-0 (paling depan)
        pasien = self._items.pop(0)

        print(f"[SISTEM] '{pasien.get('nama', pasien['nik'])}' "
              f"keluar dari antrean untuk dilayani.")
        return pasien


    def lihat_pasien(self):
        '''
        mengintip siapa pasien yang ada di urutan paling depan TANPA menghapus data dari antrean (Peek).
    
        '''
        if self.cek_antrian_kosong():
            return None
        return self._items[0]


    #cek_antrian_kosong — kita mengecek apakah antrean kosong
    def cek_antrian_kosong(self):
        return len(self._items) == 0  #klau panjang list sama dengan 0, berarti bernilai True (kosong)

    
    #jmlh_antrian_pasien — jumlah pasien dalam antrean
    def jmlh_antrian_pasien(self):
        return len(self._items)   #pakai len() untuk menghitung total elemen di dalam list

    
    #tampilkan_antrian — menampilkan seluruh isi antrean (untuk debug/demo)
    def tampilkan_antrian(self):
        if self.cek_antrian_kosong():
            print("[SISTEM] Antrean saat ini kosong.")
            return
        print(f"[SISTEM] Isi antrean ({self.jmlh_antrian_pasien()} pasien) — urutan dari depan:")

        for i, p in enumerate(self._items, start=1): 
            #enumerate() untuk dapatkan indeks(i) dan data pasien(p) secara bersamaan, mulai dari 1
            print(f"  {i}. NIK: {p.get('nik')} | "
                  f"Nama: {p.get('nama', '-')} | "
                  f"Layanan: {p.get('layanan', '-')}")

    
    #to_list — mengekspor isi antrean sebagai list (untuk save ke JSON)
    def to_list(self) -> list:
        return list(self._items)

    
    #from_list — mengisi ulang antrean dari list (untuk load dari JSON)
    def from_list(self, data: list):
        self._items = [item for item in data if isinstance(item, dict)] #hanya ambil item yang valid (dictionary)



