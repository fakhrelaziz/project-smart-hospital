"""
File    : modules/queue_pendaftaran.py
Materi  : Queue — Antrian FIFO (First In First Out)
Deskripsi:
    Mengimplementasikan struktur data Queue secara manual untuk mengelola
    antrian pendaftaran pasien. Pasien yang datang lebih dulu dilayani
    lebih dulu (FIFO).
Catatan :
    - Queue diimplementasikan menggunakan list Python dengan:
        enqueue() = append ke belakang list
        dequeue()  = pop(0) dari depan list
    - Tidak menggunakan collections.deque agar implementasi terlihat eksplisit.
Relasi  :
    - Digunakan oleh modules/manage_pasien.py sebagai antrian loket pendaftaran.
"""


class QueuePendaftaran:
    def __init__(self):
        self._items: list = []

    def enqueue(self, pasien: dict):
        """Menambahkan pasien ke bagian belakang antrian (FIFO).

        Melakukan validasi bahwa data yang masuk adalah dict dan memiliki key 'nik'.

        Returns:
            bool: True jika berhasil, False jika data tidak valid.
        """
        if not isinstance(pasien, dict):
            print("[SISTEM] ERROR: pasien harus berupa dictionary.")
            return False

        if not pasien.get("nik"):
            print("[SISTEM] ERROR: data pasien harus memiliki key 'nik'.")
            return False

        self._items.append(pasien)
        print(f"[SISTEM] '{pasien.get('nama', pasien['nik'])}' "
              f"masuk antrean. Posisi: {len(self._items)}")
        return True

    def dequeue(self):
        """Mengambil dan menghapus pasien paling depan antrian (FIFO).

        Returns:
            dict | None: Dict pasien yang dilayani, atau None jika antrian kosong.
        """
        if self.cek_antrian_kosong():
            print("[SISTEM] Antrean kosong. Tidak ada pasien untuk diproses.")
            return None

        pasien = self._items.pop(0)
        print(f"[SISTEM] '{pasien.get('nama', pasien['nik'])}' "
              f"keluar dari antrean untuk dilayani.")
        return pasien

    def lihat_pasien(self):
        """Mengembalikan pasien paling depan tanpa menghapusnya dari antrian (Peek).

        Returns:
            dict | None: Dict pasien terdepan, atau None jika antrian kosong.
        """
        if self.cek_antrian_kosong():
            return None
        return self._items[0]

    def cek_antrian_kosong(self):
        """Mengecek apakah antrian sedang kosong."""
        return len(self._items) == 0

    def jmlh_antrian_pasien(self):
        """Mengembalikan jumlah pasien yang sedang dalam antrian."""
        return len(self._items)

    def tampilkan_antrian(self):
        """Menampilkan seluruh isi antrian ke terminal secara terurut dari depan."""
        if self.cek_antrian_kosong():
            print("[SISTEM] Antrean saat ini kosong.")
            return
        print(f"[SISTEM] Isi antrean ({self.jmlh_antrian_pasien()} pasien) — urutan dari depan:")

        for i, p in enumerate(self._items, start=1):
            print(f"  {i}. NIK: {p.get('nik')} | "
                  f"Nama: {p.get('nama', '-')} | "
                  f"Layanan: {p.get('layanan', '-')}")

    def to_list(self) -> list:
        """Mengekspor isi antrian sebagai list biasa untuk disimpan ke JSON."""
        return list(self._items)

    def from_list(self, data: list):
        """Mengisi ulang antrian dari list yang dimuat dari JSON."""
        self._items = [item for item in data if isinstance(item, dict)]
