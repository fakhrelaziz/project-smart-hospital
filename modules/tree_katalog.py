"""
File    : modules/tree_katalog.py
Materi  : Tree (Materi Tambahan)
Deskripsi:
    Mengimplementasikan struktur Tree untuk hierarki katalog farmasi.
    Tree bersifat STATIS (hardcoded) — kategori tidak bertambah/berkurang
    saat program berjalan. Obat-obat dari obat.json diletakkan di node
    daun sesuai kategorinya.
Struktur Tree (4-Level):
    Farmasi (root)
    ├── Obat Dalam (kategori)
    │   ├── Tablet (bentuk)
    │   │   └── Paracetamol 500mg  [OBT001]
    │   └── Sirup (bentuk)
    │       └── Paracetamol Sirup  [OBT006]
    └── Obat Luar (kategori)
        └── Salep (bentuk)
            └── Ketoconazole Krim  [OBT008]
Catatan :
    - Node kategori & bentuk : kode_obat = None
    - Node obat (daun): kode_obat diisi kode obat
    - Fungsi tampilkan() menggunakan rekursif
    - Tidak ada fitur tambah/hapus node dinamis
Relasi  :
    - Membaca data dari data/obat.json via utils.json_handler
    - Kategori node dicocokkan dengan field "kategori" dan "bentuk" di obat.json
"""

from utils.json_handler import load_json


# ══════════════════════════════════════════════════════════════════════════════
# CLASS NODE TREE
# ══════════════════════════════════════════════════════════════════════════════

class NodeTree:
    """
    Merepresentasikan satu node di dalam Tree katalog farmasi.

    Setiap node bisa berupa:
        - Node kategori/bentuk : nama = nama node, kode_obat = None
        - Node obat (daun)     : nama = nama obat, kode_obat = kode obat

    Atribut:
        nama      (str)        : Nama node.
        kode_obat (str | None) : Kode obat jika ini node daun, None jika kategori/bentuk.
        children  (list)       : List NodeTree anak dari node ini.
    """

    def __init__(self, nama, kode_obat=None):
        self.nama      = nama
        self.kode_obat = kode_obat   # None jika node kategori/bentuk
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
    Tree hierarki katalog farmasi (4-Level).

    Struktur tree dibangun STATIS di __init__ berdasarkan
    data obat.json.
    Hierarki: Farmasi -> Kategori -> Bentuk -> Nama Obat
    """

    def __init__(self):
        # Root node — puncak hierarki
        self.root = NodeTree("Farmasi")

        # Dict untuk tracking node yang sudah dibuat
        self._node_kategori = {}
        self._node_bentuk = {}

        self._bangun_tree()

    def _bangun_tree(self):
        """
        Membaca obat.json dan membangun hierarki tree secara otomatis
        berdasarkan field "kategori" dan "bentuk" tiap obat.
        """
        data_obat = load_json("data/obat.json")

        for obat in data_obat:
            nama_kategori = obat.get("kategori", "Lainnya")
            bentuk        = obat.get("bentuk", "Lainnya")
            kode          = obat.get("kode", "")
            nama_obat     = obat.get("nama", "")

            # 1. Level 2: Kategori
            if nama_kategori not in self._node_kategori:
                node_kat = NodeTree(nama_kategori)
                self.root.tambah_anak(node_kat)
                self._node_kategori[nama_kategori] = node_kat

            # 2. Level 3: Bentuk (di bawah Kategori)
            key_bentuk = f"{nama_kategori}_{bentuk}"
            if key_bentuk not in self._node_bentuk:
                node_bentuk = NodeTree(bentuk)
                self._node_kategori[nama_kategori].tambah_anak(node_bentuk)
                self._node_bentuk[key_bentuk] = node_bentuk

            # 3. Level 4: Nama Obat (Daun, di bawah Bentuk)
            node_obat = NodeTree(nama_obat, kode_obat=kode)
            self._node_bentuk[key_bentuk].tambah_anak(node_obat)

    # TAMPILKAN TREE (REKURSIF)

    def tampilkan(self, node=None, level=0):
        """
        Menampilkan seluruh hierarki tree ke terminal secara REKURSIF.

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
            # Node kategori/bentuk — tampilkan dengan simbol folder
            print(f"{indent}├─ {node.nama}")

        # RECURSIVE CASE
        # Panggil tampilkan() untuk setiap node anak
        for anak in node.children:
            self.tampilkan(anak, level + 1)


# FUNGSI CLI — DIPANGGIL DARI main.py

def tampilkan_katalog():
    """Entry point CLI: tampilkan seluruh hierarki katalog obat."""
    print("\n" + "=" * 48)
    print("         KATALOG FARMASI — HIERARKI OBAT")
    print("         Struktur Data: Tree (4-Level)")
    print("=" * 48)
    katalog = KatalogObat()
    katalog.tampilkan()
    print("=" * 48)