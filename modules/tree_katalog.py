"""
File    : modules/tree_katalog.py
Materi  : Tree (Materi Tambahan)
Deskripsi:
    Mengimplementasikan struktur Tree untuk hierarki katalog farmasi.
    Tree bersifat STATIS (hardcoded) — kategori tidak bertambah/berkurang
    saat program berjalan. Obat-obat dari obat.json diletakkan di node
    daun sesuai kategorinya.
Struktur Tree:
    Farmasi (root)
    ├── Obat Dalam
    │   ├── Paracetamol 500mg  [OBT001]
    │   └── Antasida           [OBT003]
    ├── Antibiotik
    │   └── Amoxicillin 500mg  [OBT002]
    ├── Analgesik
    │   └── Ibuprofen 400mg    [OBT004]
    └── Antasida (kategori)
        └── Ranitidin 150mg    [OBT005]
Catatan :
    - Node kategori : kode_obat = None
    - Node obat (daun): kode_obat diisi kode obat
    - Fungsi tampilkan() menggunakan rekursif
    - Tidak ada fitur tambah/hapus node dinamis
Relasi  :
    - Membaca data dari data/obat.json via utils.json_handler
    - Kategori node dicocokkan dengan field "kategori" di obat.json
"""

from utils.json_handler import load_json


# ══════════════════════════════════════════════════════════════════════════════
# CLASS NODE TREE
# ══════════════════════════════════════════════════════════════════════════════

class NodeTree:
    """
    Merepresentasikan satu node di dalam Tree katalog farmasi.

    Setiap node bisa berupa:
        - Node kategori : nama = nama kategori, kode_obat = None
        - Node obat (daun): nama = nama obat, kode_obat = kode obat

    Atribut:
        nama      (str)        : Nama node (kategori atau nama obat).
        kode_obat (str | None) : Kode obat jika ini node daun, None jika kategori.
        children  (list)       : List NodeTree anak dari node ini.
    """

    def __init__(self, nama, kode_obat=None):
        self.nama      = nama
        self.kode_obat = kode_obat   # None jika node kategori
        self.children  = []          # list of NodeTree

    def tambah_anak(self, node_anak):
        """Menambahkan node anak ke daftar children."""
        self.children.append(node_anak)
        return node_anak             # return agar bisa chaining


# ══════════════════════════════════════════════════════════════════════════════
# CLASS KATALOG OBAT (TREE)
# ══════════════════════════════════════════════════════════════════════════════

class KatalogObat:
    """
    Tree hierarki katalog farmasi.

    Struktur tree dibangun STATIS di __init__ berdasarkan
    kategori yang ada di obat.json. Node kategori di-root di
    bawah node "Farmasi".

    Cara kerja:
        1. Load obat.json saat inisialisasi
        2. Buat root node "Farmasi"
        3. Untuk setiap obat, cari node kategorinya
           (buat baru jika belum ada)
        4. Tambahkan node obat sebagai daun di bawah kategorinya
    """

    def __init__(self):
        # Root node — puncak hierarki
        self.root = NodeTree("Farmasi")

        # Dict untuk tracking node kategori yang sudah dibuat
        # Key: nama kategori, Value: NodeTree kategori
        self._node_kategori = {}

        # Load dan bangun tree dari data JSON
        self._bangun_tree()

    # BANGUN TREE DARI DATA JSON

    def _bangun_tree(self):
        """
        Membaca obat.json dan membangun hierarki tree secara otomatis
        berdasarkan field "kategori" tiap obat.

        Alur:
            Untuk setiap obat di JSON:
            1. Ambil nama kategorinya
            2. Jika node kategori belum ada → buat dan sambungkan ke root
            3. Buat node obat (daun) → sambungkan ke node kategori
        """
        data_obat = load_json("data/obat.json")

        for obat in data_obat:
            nama_kategori = obat.get("kategori", "Lainnya")
            kode          = obat.get("kode", "")
            nama_obat     = obat.get("nama", "")

            # Cek apakah node kategori sudah ada
            if nama_kategori not in self._node_kategori:
                # Buat node kategori baru dan sambungkan ke root
                node_kat = NodeTree(nama_kategori)
                self.root.tambah_anak(node_kat)
                self._node_kategori[nama_kategori] = node_kat

            # Buat node obat (daun) dan sambungkan ke kategorinya
            node_obat = NodeTree(nama_obat, kode_obat=kode)
            self._node_kategori[nama_kategori].tambah_anak(node_obat)

    # TAMPILKAN TREE (REKURSIF)

    def tampilkan(self, node=None, level=0):
        """
        Menampilkan seluruh hierarki tree ke terminal secara REKURSIF.

        Cara kerja rekursif:
            tampilkan(root, 0)
                → cetak "Farmasi"
                → untuk setiap anak root: tampilkan(anak, 1)
                    → cetak "  Obat Dalam"
                    → untuk setiap anak: tampilkan(anak, 2)
                        → cetak "    Paracetamol [OBT001]"
                        → tidak ada anak lagi → kembali (base case)

        BASE CASE    : Node tidak punya anak (node daun) → tidak rekursif lagi.
        RECURSIVE CASE: Node punya anak → panggil tampilkan() untuk setiap anak.

        Args:
            node  (NodeTree | None): Node yang sedang ditampilkan.
                                     Default None → mulai dari root.
            level (int)            : Kedalaman node, menentukan indentasi.
        """
        # Jika dipanggil tanpa argumen, mulai dari root
        if node is None:
            node = self.root

        # Tentukan indentasi dan simbol berdasarkan level
        indent = "  " * level

        if level == 0:
            # Root — tanpa simbol
            print(f"{indent}{node.nama}")

        elif node.kode_obat:
            # Node daun (obat) — tampilkan dengan kode
            print(f"{indent}└─ {node.nama}  [{node.kode_obat}]")

        else:
            # Node kategori — tampilkan dengan simbol folder
            print(f"{indent}├─ {node.nama}")

        # RECURSIVE CASE
        # Panggil tampilkan() untuk setiap node anak
        for anak in node.children:
            self.tampilkan(anak, level + 1)

    # CARI OBAT BY NAMA (REKURSIF)

    def cari_obat(self, keyword, node=None, hasil=None):
        """
        Mencari obat di tree berdasarkan nama menggunakan rekursif.

        BASE CASE    : Node tidak punya anak → tidak ada yang perlu dicari lagi.
        RECURSIVE CASE: Periksa node ini, lalu cari ke semua anak.

        Args:
            keyword (str)             : Kata kunci nama obat (case-insensitive).
            node    (NodeTree | None) : Node saat ini. Default → root.
            hasil   (list | None)     : Akumulator hasil. Default → list baru.

        Returns:
            list: List of dict obat yang cocok:
                  [{"nama": ..., "kode_obat": ..., "kategori": ...}, ...]
        """
        if node is None:
            node = self.root
        if hasil is None:
            hasil = []

        # Periksa node saat ini (hanya node daun / obat yang punya kode_obat)
        if node.kode_obat and keyword.lower() in node.nama.lower():
            # Cari nama kategori (parent node)
            kategori = self._cari_kategori_obat(node.kode_obat)
            hasil.append({
                "nama"     : node.nama,
                "kode_obat": node.kode_obat,
                "kategori" : kategori
            })

        # RECURSIVE CASE
        for anak in node.children:
            self.cari_obat(keyword, anak, hasil)

        return hasil

    def _cari_kategori_obat(self, kode_obat):
        """
        Mencari nama kategori dari sebuah kode obat.
        Menggunakan dict _node_kategori yang sudah dibangun saat init.

        Args:
            kode_obat (str): Kode obat yang dicari kategorinya.

        Returns:
            str: Nama kategori, atau "Tidak diketahui" jika tidak ditemukan.
        """
        for nama_kat, node_kat in self._node_kategori.items():
            for anak in node_kat.children:
                if anak.kode_obat == kode_obat:
                    return nama_kat
        return "Tidak diketahui"

    # AMBIL SEMUA OBAT DI KATEGORI TERTENTU

    def obat_by_kategori(self, nama_kategori):
        """
        Mengembalikan semua kode obat di bawah kategori tertentu.

        Args:
            nama_kategori (str): Nama kategori yang dicari (case-insensitive).

        Returns:
            list: List of dict obat di kategori tersebut.
                  List kosong jika kategori tidak ditemukan.
        """
        nama_lower = nama_kategori.lower()
        for nama_kat, node_kat in self._node_kategori.items():
            if nama_kat.lower() == nama_lower:
                return [
                    {"nama": anak.nama, "kode_obat": anak.kode_obat}
                    for anak in node_kat.children
                ]
        return []

    # DAFTAR SEMUA KATEGORI

    def daftar_kategori(self):
        """
        Mengembalikan semua nama kategori yang ada di tree.

        Returns:
            list: List nama kategori (string).
        """
        return list(self._node_kategori.keys())


# FUNGSI CLI — DIPANGGIL DARI main.py

def tampilkan_katalog():
    """Entry point CLI: tampilkan seluruh hierarki katalog obat."""
    print("\n" + "=" * 48)
    print("         KATALOG FARMASI — HIERARKI OBAT")
    print("         Struktur Data: Tree")
    print("=" * 48)
    katalog = KatalogObat()
    katalog.tampilkan()
    print("=" * 48)


def cari_obat_di_katalog():
    """Entry point CLI: cari obat berdasarkan nama di dalam tree."""
    print("\n" + "=" * 48)
    print("           CARI OBAT DI KATALOG")
    print("=" * 48)
    keyword = input("  Masukkan nama obat: ").strip()
    if not keyword:
        print("  [ERROR] Keyword tidak boleh kosong.")
        return

    katalog = KatalogObat()
    hasil   = katalog.cari_obat(keyword)

    if not hasil:
        print(f"  [INFO] Obat '{keyword}' tidak ditemukan di katalog.")
        return

    print(f"\n  Ditemukan {len(hasil)} obat:\n")
    for obat in hasil:
        print(f"  ├─ {obat['nama']}  [{obat['kode_obat']}]")
        print(f"  │  Kategori: {obat['kategori']}")


def lihat_obat_per_kategori():
    """Entry point CLI: tampilkan semua obat dalam kategori tertentu."""
    print("\n" + "=" * 48)
    print("          LIHAT OBAT PER KATEGORI")
    print("=" * 48)

    katalog    = KatalogObat()
    kategori   = katalog.daftar_kategori()

    print("  Kategori tersedia:")
    for i, kat in enumerate(kategori, 1):
        print(f"    [{i}] {kat}")

    while True:
        try:
            pilih = int(input("  Pilih nomor kategori: ").strip())
            if 1 <= pilih <= len(kategori):
                nama_kat = kategori[pilih - 1]
                break
            print(f"  [ERROR] Pilih angka 1 sampai {len(kategori)}.")
        except ValueError:
            print("  [ERROR] Input harus berupa angka.")

    daftar = katalog.obat_by_kategori(nama_kat)
    print(f"\n  Obat dalam kategori '{nama_kat}':\n")
    for obat in daftar:
        print(f"  └─ {obat['nama']}  [{obat['kode_obat']}]")