"""
File    : modules/tree_katalog.py
Materi  : Tree (Data Structure)
Deskripsi:
    Mengimplementasikan struktur Tree murni untuk node hierarki katalog farmasi.
Catatan :
    - Class ini hanya mendefinisikan struktur data.
    - Algoritma pembangunan Tree dan CLI dipindahkan ke manage_obat.py.
"""

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
# CLASS KATALOG OBAT (TREE DATA STRUCTURE & ALGORITHM)
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
        from utils.json_handler import load_json
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
        """
        if node is None:
            node = self.root

        indent = "  " * level

        if level == 0:
            print(f"{indent}{node.nama}")
        elif node.kode_obat:
            print(f"{indent}└─ {node.nama}  [{node.kode_obat}]")
        else:
            print(f"{indent}├─ {node.nama}")

        for anak in node.children:
            self.tampilkan(anak, level + 1)
