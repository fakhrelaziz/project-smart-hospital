'''
Konsep dasar yang digunakan adalah STACK / TUMPUKAN (LIFO - Last In, First Out):
  - Aksi yang terakhir dilakukan -> akan pertama kali dibatalkan (Undo).
  - tambah_aksi() [Push] -> memasukkan riwayat perubahan skor ke atas tumpukan.
  - batalkan_aksi() [Pop] -> mengambil dan menghapus aksi paling atas untuk memulihkan data.
  - intip_aksi_terakhir() [Peek] -> melihat catatan perubahan terakhir tanpa membatalkannya.
'''
'''
disini tu nnanti ada pakai istilah "triase", itu arti proses penentuan tingkat bahaya pasien di UGD 
berdasarkan gejala yang dialami. Skor triase ini penting untuk menentukan prioritas penanganan pasien.
'''

from datetime import datetime
#pakai ini buat catat kapan aksi perubahan skor itu terjadi, jadi kita bisa tahu riwayatnya dengan lebih jelas

class Stack_UGD:
    def __init__(self, batas_undo = 20): #disini ukuran default kita buat 20, bisa diubah sesuai kebutuhan
        '''
        batas_undo : jumlah aksi maksimal yang bisa disimpan di dalam tumpukan.
        jadi, akksi terlama otomatis dihapus saat batas tercapai. biar memori gapenuh dari data yang lama
        '''

        #ini buat memastikan batas tidak diisi angka minus atau nol oleh pengguna
        if batas_undo < 1:
            print("[SISTEM] PERINGATAN: Batas undo tidak valid. Nilai diatur ke default (20).")
            self._batas = 20
        else:
            self._batas = batas_undo

        self._riwayat_aksi = []  #kita buat list kosong untuk menyimpan riwayat aksi/perubahan skor bahaya
        


    def tambah_aksi(self, aksi: dict):
        '''
        menyimpan aksi/perubahan skor terakhir ke dalam stack (Push).
        mengembalikan True jika berhasil, False jika data tidak valid.
        '''
        #validasi 1: memastikan data riwayat berbentuk Dictionary {}
        if not isinstance(aksi, dict):
            print("[SISTEM] ERROR: Data aksi harus berupa dictionary.")
            return False

        #validasi 2: memastikan kunci-kunci penting (nik, skor_lama, skor_baru) ada di dalam data
        kunci_wajib = ["nik", "skor_lama", "skor_baru"]
        for kunci in kunci_wajib:
            if kunci not in aksi:
                print(f"[SISTEM] ERROR: Data aksi tidak lengkap! Kurang key '{kunci}'.")
                return False
            

        #otomatis 1: Isi waktu otomatis jika tidak disertakan oleh admin 
        if "waktu" not in aksi:
            aksi["waktu"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #ini mkanya pakai import datetime di awal, untuk catat kapan aksi itu terjadi

        #otomatis 2: Isi keterangan default jika tidak disertakan oleh admin (
        if "keterangan" not in aksi:
            aksi["keterangan"] = "ubah skor triase"

        #buang aksi terlama (indeks 0) jika sudah menyentuh batas maksimal
        if len(self._riwayat_aksi) >= self._batas:
            dibuang = self._riwayat_aksi.pop(0)
            print(f"[SISTEM] Batas {self._batas} aksi tercapai. "
                  f"Aksi terlama NIK '{dibuang['nik']}' dihapus dari memori.")

        #memasukkan data aksi ke urutan paling akhir (paling atas di dalam tumpukan)
        self._riwayat_aksi.append(aksi)
        print(f"[SISTEM] BERHASIL: Aksi perubahan skor untuk NIK {aksi['nik']} disimpan ke tumpukan.")
        return True


    def batalkan_aksi(self):
        '''
        mengambil dan menghapus aksi terakhir untuk proses UNDO (Pop).
        Mengembalikan dict aksi untuk memulihkan skor lama, atau None jika stack kosong.
        '''
        # kita cwk terlebih dahulu, jika tumpukan kosong, maka tidak ada yang bisa di-undo
        if self.apakah_kosong():
            print("[SISTEM] INFO: Tidak ada aksi yang bisa dibatalkan (Tumpukan kosong).")
            return None

        # .pop() tanpa indeks otomatis mengambil dan menghapus data PALING AKHIR (paling atas)
        aksi_terakhir = self._riwayat_aksi.pop()
        print(f"[SISTEM] UNDO: Membatalkan perubahan skor NIK {aksi_terakhir['nik']}. "
              f"Mengembalikan skor ke {aksi_terakhir['skor_lama']}.")
        return aksi_terakhir


    def intip_aksi_terakhir(self):
        '''
        melihat catatan aksi teratas TANPA menghapusnya dari tumpukan (Peek).
        '''
        if self.apakah_kosong():
            return None
            
        #menggunakan indeks [-1] untuk melihat elemen terakhir/teratas di Python
        return self._riwayat_aksi[-1]


    def apakah_kosong(self):
        '''
        memeriksa apakah tumpukan riwayat sedang kosong atau tidak.
        '''
        return len(self._riwayat_aksi) == 0


    def total_riwayat(self):
        '''
        Mmenghitung jumlah total aksi yang tersimpan di dalam tumpukan.
        '''
        return len(self._riwayat_aksi)


    def tampilkan_tumpukan(self):
        '''
        menampilkan seluruh isi tumpukan riwayat dari yang terbaru/teratas
        '''
        if self.apakah_kosong():
            print("[SISTEM] Tumpukan riwayat undo saat ini kosong.")
            return

        
        #reversed() digunakan agar kita membaca list dari belakang (data paling baru dulu)
        print(f"[SISTEM] Daftar Riwayat Perubahan (Total: {self.total_riwayat()} entri) — Urutan Atas ke Bawah:")
        for nomor, aksi in enumerate(reversed(self._riwayat_aksi), start=1):
            print(f"  {nomor}. NIK: {aksi['nik']} | "
                  f"Skor: {aksi['skor_lama']} → {aksi['skor_baru']} | "
                  f"Ket: {aksi.get('keterangan','-')} | Waktu: {aksi.get('waktu','-')}")
    
    def to_list(self):
        '''
        mengomvers objek tumpukan menjadi list mentah biasa agar bisa disimpan ke format JSON.
        '''
        return list(self._riwayat_aksi)


    def from_list(self, data: list):
        '''
        memuat ulang isi tumpukan dari data list mentah (hasil baca dari file JSON).
        '''
        self._riwayat_aksi = [item for item in data if isinstance(item, dict)]





#Coba Demo mandiri — jalankan: python modules/stack_ugd.py
if __name__ == "__main__":
    print("=== Demo modules/stack_ugd.py ===\n")

    #buat objek stack untuk fitur undo UGD
    fitur_undo = Stack_UGD()

    #cek kondisi awal
    print(f"Apakah tumpukan kosong? {fitur_undo.apakah_kosong()}")
    fitur_undo.tampilkan_tumpukan()
    print()

    #1. Jalankan fungsi penambahan aksi (Push)
    print("--- 1. PROSES INPUT & PERUBAHAN SKOR (PUSH) ---")
    fitur_undo.tambah_aksi({"nik": "3201010101010001", "skor_lama": 0, "skor_baru": 5, "keterangan": "triase awal"})
    fitur_undo.tambah_aksi({"nik": "3201010101010003", "skor_lama": 0, "skor_baru": 9, "keterangan": "kondisi kritis"})
    
    #push ketiga ni coba sengaja ga mengisi waktu dan keterangan (akan diisi otomatis oleh program)
    fitur_undo.tambah_aksi({"nik": "3201010101010005", "skor_lama": 2, "skor_baru": 7})
    print()

    #tampilkan isi tumpukan setelah diisi 
    fitur_undo.tampilkan_tumpukan()
    print()

    #2. Jalankan fungsi intip data teratas (Peek)
    terakhir = fitur_undo.intip_aksi_terakhir()
    if terakhir:
        print(f"Intip Aksi Teratas: NIK {terakhir['nik']} | Skor {terakhir['skor_lama']} -> {terakhir['skor_baru']}")
    print(f"Total ukuran tumpukan saat ini: {fitur_undo.total_riwayat()}")
    print()

    #3. Jalankan fungsi pembatalan aksi (Pop / Undo)
    print("--- 2. PROSES UNDO AKSI TERAKHIR ---")
    dibatalkan = fitur_undo.batalkan_aksi()
    if dibatalkan:
        print(f"  -> LOG: Sistem berhasil memicu pengembalian skor NIK '{dibatalkan['nik']}' ke nilai lama: {dibatalkan['skor_lama']}")
    print()

    #4. Kosongkan sisa tumpukan dan uji kondisi kosong
    print("--- 3. MENGOSONGKAN TUMPUKAN ---")
    fitur_undo.batalkan_aksi()  #hpus data sisa terakhir
    fitur_undo.batalkan_aksi()  #ini akan memicu pesan stack kosong