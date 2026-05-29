"""
File    : modules/stack_ugd.py
Materi  : Stack — Tumpukan LIFO (Last In First Out)
Deskripsi:
    Mengimplementasikan struktur data Stack secara manual untuk menyimpan
    riwayat aksi (triase & pendaftaran) demi keperluan fitur Undo.
    Aksi yang terakhir dilakukan adalah yang pertama kali dibatalkan (LIFO).
Catatan :
    - tambah_aksi()       [Push] — menyimpan aksi ke atas tumpukan.
    - batalkan_aksi()     [Pop]  — mengambil dan menghapus aksi teratas untuk Undo.
    - intip_aksi_terakhir() [Peek] — melihat aksi teratas tanpa menghapus.
    - Mendukung dua tipe aksi: 'triase' dan 'pendaftaran'.
Relasi  :
    - Digunakan oleh modules/manage_pasien.py dan modules/sorting_triase.py.
"""


class Stack_UGD:

    def __init__(self):
        #kita buat list kosong untuk menyimpan riwayat aksi/perubahan skor bahaya
        self._riwayat_aksi: list = []

    def tambah_aksi(self, aksi: dict) -> bool:
        '''
        menyimpan aksi/perubahan skor terakhir ke dalam stack (Push).
        mengembalikan True jika berhasil, False jika data tidak valid.
        '''
        #validasi 1: memastikan data riwayat berbentuk Dictionary {}
        if not isinstance(aksi, dict):
            print("[STACK-UGD] ERROR: Data aksi harus berupa dictionary.")
            return False

        #validasi 2: memastikan kunci-kunci penting sesuai dengan tipe aksinya
        tipe = aksi.get("tipe_aksi", "triase")
        if tipe == "triase":
            kunci_wajib = ["nik", "skor_lama", "skor_baru"]
        elif tipe == "pendaftaran":
            kunci_wajib = ["nik"]
        else:
            kunci_wajib = ["nik"]

        for kunci in kunci_wajib:
            if kunci not in aksi:
                print(f"[SISTEM] ERROR: Data aksi tidak lengkap! Kurang key '{kunci}'.")
                return False

        #memasukkan data aksi ke urutan paling akhir (paling atas di dalam tumpukan)
        self._riwayat_aksi.append(aksi)
        print(f"[SISTEM] BERHASIL: Aksi '{tipe}' untuk NIK {aksi['nik']} disimpan ke tumpukan.")
        return True


    def batalkan_aksi(self) -> dict:
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
        tipe = aksi_terakhir.get("tipe_aksi", "triase")
        if tipe == "triase":
            print(f"[SISTEM] UNDO: Membatalkan perubahan skor NIK {aksi_terakhir['nik']}. "
                  f"Mengembalikan skor ke {aksi_terakhir['skor_lama']}.")
        elif tipe == "pendaftaran":
            print(f"[SISTEM] UNDO: Membatalkan pendaftaran NIK {aksi_terakhir['nik']}.")
        return aksi_terakhir


    def intip_aksi_terakhir(self) -> dict:
        '''
        melihat catatan aksi teratas TANPA menghapusnya dari tumpukan (Peek).
        '''
        if self.apakah_kosong():
            return None

        #menggunakan indeks [-1] untuk melihat elemen terakhir/teratas di Python
        return self._riwayat_aksi[-1]


    def apakah_kosong(self) -> bool:
        '''
        memeriksa apakah tumpukan riwayat sedang kosong atau tidak.
        '''
        return len(self._riwayat_aksi) == 0


    def total_riwayat(self) -> int:
        '''
        Mmenghitung jumlah total aksi yang tersimpan di dalam tumpukan.
        '''
        return len(self._riwayat_aksi)


    def tampilkan_tumpukan(self):
        '''
        menampilkan seluruh isi tumpukan riwayat dari yang terbaru/teratas (untuk keperluan demo).
        '''
        if self.apakah_kosong():
            print("[SISTEM] Tumpukan riwayat undo saat ini kosong.")
            return
        

        print(f"[SISTEM] Daftar Riwayat Perubahan (Total: {self.total_riwayat()} aksi) - Urutan Atas ke Bawah:")
        #reversed() digunakan agar kita membaca list dari belakang (data paling baru dulu)
        for nomor, aksi in enumerate(reversed(self._riwayat_aksi), start=1):
            tipe = aksi.get('tipe_aksi', 'triase')
            if tipe == 'triase':
                info = f"Skor: {aksi.get('skor_lama')} -> {aksi.get('skor_baru')}"
            else:
                info = f"Aksi: {tipe}"
            print(f"  {nomor}. NIK: {aksi['nik']} | {info} | Ket: {aksi.get('keterangan', '-')}")


#Coba Demo mandiri — jalankan: python modules/stack_ugd.py
if __name__ == "__main__":
    print("=== Demo modules/stack_ugd.py ===\n")

    #buat objek stack untuk fitur undo UGD
    fitur_undo = Stack_UGD()

    #1. Simulasi Admin UGD melakukan input salah dan melakukan perubahan skor (Push)
    print("--- 1. PROSES INPUT & PERUBAHAN SKOR (PUSH) ---")

   
    #aksi 1: Input awal pasien pertama
    aksi1 = {
        "nik": "1234567890",
        "skor_lama": 0,
        "skor_baru": 3,
        "keterangan": "Input awal skor triase Budi"
    }
    fitur_undo.tambah_aksi(aksi1)


    #aksi 2: Admin salah input skor untuk pasien pertama (Budi), harusnya 5 tapi terketik 8
    aksi2 = {
        "nik": "1234567890",
        "skor_lama": 3,
        "skor_baru": 8,
        "keterangan": "Salah input skor bahaya UGD"
    }
    fitur_undo.tambah_aksi(aksi2)

    #aksi 3: Input skor untuk pasien kedua (Siti)
    aksi3 = {
        "nik": "9876543210",
        "skor_lama": 0,
        "skor_baru": 5,
        "keterangan": "Input triase Siti"
    }
    fitur_undo.tambah_aksi(aksi3)
    print()

    #tampilkan isi tumpukan saat ini
    fitur_undo.tampilkan_tumpukan()
    print()

    #2. Simulasi Admin menekan tombol UNDO (Pop) karena sadar ada yang salah
    print("--- 2. PROSES UNDO PERTAMA (Membatalkan Aksi Terakhir) ---")

    #aksi terakhir yang masuk adalah milik Siti (Aksi 3), maka ini yang keluar duluan
    data_pulih1 = fitur_undo.batalkan_aksi()
    if data_pulih1:
        print(f"  -> LOG: Sistem harus memulihkan NIK {data_pulih1['nik']} ke skor lama: {data_pulih1['skor_lama']}")
    print()

    print("--- 3. PROSES UNDO KEDUA (Membatalkan Salah Input Budi) ---")
    #sekarang posisi teratas adalah Aksi 2 (Salah input Budi). Ini yang di-undo
    data_pulih2 = fitur_undo.batalkan_aksi()
    if data_pulih2:
        print(f"  -> LOG: Sistem sukses memulihkan NIK {data_pulih2['nik']} ke skor lama: {data_pulih2['skor_lama']}")
    print()

    #tampilkan sisa tumpukan setelah 2 kali di-undo
    print("--- 4. SISA TUMPUKAN SEKARANG ---")
    fitur_undo.tampilkan_tumpukan()