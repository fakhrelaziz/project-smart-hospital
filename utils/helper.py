"""
File    : utils/helper.py
Deskripsi: Kumpulan fungsi utilitas umum yang dipakai berulang di banyak modul.
Tujuan  : Mengurangi duplikasi kode untuk operasi-operasi non-bisnis yang sering muncul,
           seperti mencetak garis pemisah, memvalidasi input angka, dan memformat nilai.
Catatan :
    - File ini TIDAK mengandung business logic apapun.
    - Semua fungsi bersifat pure utility dan dapat diimpor dari modul manapun.
    - Tidak bergantung pada modul lain di dalam proyek ini.
Relasi  :
    - Dapat diimpor oleh semua modul di modules/ maupun models/.
"""


# ── TAMPILAN / SEPARATOR ──────────────────────────────────────────────────────

def cetak_garis(karakter="─", panjang=44):
    """Mencetak garis pemisah horizontal ke terminal."""
    print(karakter * panjang)


def cetak_header(judul: str, karakter="=", panjang=44):
    """
    Mencetak header berformat ke terminal.

    Contoh output (judul='DAFTAR PASIEN'):
        ============================================
          DAFTAR PASIEN
        ============================================
    """
    print(karakter * panjang)
    print(f"  {judul.upper()}")
    print(karakter * panjang)


def cetak_subheader(judul: str, panjang=44):
    """Mencetak sub-header berformat ringan menggunakan garis tipis."""
    print(f"\n{'─' * panjang}")
    print(f"  {judul}")
    print("─" * panjang)


# ── VALIDASI INPUT ────────────────────────────────────────────────────────────

def input_angka(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Meminta input angka bulat dari pengguna dengan validasi otomatis.
    Akan terus meminta ulang sampai input valid.

    Args:
        prompt  (str) : Teks yang ditampilkan sebelum input.
        min_val (int) : Nilai minimum yang diizinkan (opsional).
        max_val (int) : Nilai maksimum yang diizinkan (opsional).

    Returns:
        int: Angka bulat yang valid dari pengguna.
    """
    while True:
        try:
            nilai = int(input(prompt).strip())
            if min_val is not None and nilai < min_val:
                print(f"[ERROR] Nilai minimal adalah {min_val}.")
                continue
            if max_val is not None and nilai > max_val:
                print(f"[ERROR] Nilai maksimal adalah {max_val}.")
                continue
            return nilai
        except ValueError:
            print("[ERROR] Input harus berupa angka bulat.")


def input_tidak_kosong(prompt: str) -> str:
    """
    Meminta input string dari pengguna dan memastikan tidak kosong.
    Akan terus meminta ulang sampai ada isi.

    Returns:
        str: String non-kosong dari pengguna.
    """
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("[ERROR] Input tidak boleh kosong.")


def konfirmasi(prompt: str = "Yakin? (y/n): ") -> bool:
    """
    Meminta konfirmasi ya/tidak dari pengguna.

    Returns:
        bool: True jika pengguna menjawab 'y' atau 'Y', False jika lainnya.
    """
    jawaban = input(prompt).strip().lower()
    return jawaban == "y"


# ── FORMAT NILAI ──────────────────────────────────────────────────────────────

def format_rupiah(angka: int) -> str:
    """
    Memformat angka integer menjadi format mata uang Rupiah.

    Contoh: format_rupiah(15000) → 'Rp 15.000'

    Args:
        angka (int): Nilai dalam Rupiah.

    Returns:
        str: String terformat, contoh 'Rp 15.000'.
    """
    return f"Rp {angka:,.0f}".replace(",", ".")


def format_tanggal_hari_ini() -> str:
    """
    Mengembalikan tanggal hari ini dalam format DD-MM-YYYY.

    Returns:
        str: Tanggal hari ini, contoh '29-05-2026'.
    """
    from datetime import date
    hari_ini = date.today()
    return hari_ini.strftime("%d-%m-%Y")