"""
Mengimplementasikan struktur Tree untuk node hierarki katalog farmasi.
"""
class NodeTree:
    def __init__(self, nama, kode_obat=None):
        self.nama      = nama
        self.kode_obat = kode_obat   
        self.children  = []         

    def tambah_anak(self, node_anak):
        """Menambahkan node anak ke daftar children."""
        self.children.append(node_anak)
        return node_anak         

class KatalogObat:
    """
    Tree hierarki katalog farmasi (4-Level).
    Struktur tree dibangun STATIS di __init__ berdasarkan
    data obat.json.
    Hierarki: Farmasi -> Kategori -> Bentuk -> Nama Obat
    """
    def __init__(self):
        # Root node 
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
        Menampilkan seluruh hierarki tree ke terminal secara rekursif.
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
