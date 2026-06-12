from models.kamar import Kamar
from models.pasien import Pasien
from utils.json_handler import load_json, save_json
from modules.dll_kamar import NavigasiKamar
from modules.cll_obat import CircularLinkedList


# fungsi yang sering digunakan atau disebut fungsi helper
def _cari_pasien(data, nik):
    for p in data:
        if p.get("nik") == nik:
            return p
    return None

def _cari_kamar(data, nomor):
    for k in data:
        if k.get("nomor") == nomor:
            return k
    return None

def _dict_ke_objek(data):
    """Mengkonversi dict kamar menjadi objek Kamar."""
    kamar_obj = Kamar()
    kamar_obj.dict_ke_objek(data)
    return kamar_obj

def _bangun_dll():
    """ memuat kamar.json dan membangun DLL NavigasiKamar."""
    data_kamar = load_json("data/kamar.json")
    dll = NavigasiKamar()
    for i in data_kamar:
        kamar_obj = _dict_ke_objek(i)
        dll.insert(kamar_obj)
    return dll



def lihat_kamar_tersedia():
    """Menampilkan daftar kamar yang masih memiliki kapasitas kosong pakai DLL."""
    # Bangun DLL dari data kamar.json
    dll = _bangun_dll()  

    print("\n--- KAMAR TERSEDIA ---")
    daftar_kamar = dll.traversal()
    
    if daftar_kamar:
        for i in daftar_kamar:
            print(i.data_kamar())
    else:
        print("ERROR: Tidak ada kamar tersedia.")

    print("-" * 32)


def assign_pasien_ke_kamar():
    """Menempatkan pasien ke kamar dan memperbarui data JSON."""
    data_kamar = load_json("data/kamar.json")
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK pasien: ").strip()
    nomor_kamar = input("Masukkan nomor kamar: ").strip()

    # Cari data pasien yang mau dimasukkan ke kamar
    pasien_data = _cari_pasien(data_pasien, nik)

    if pasien_data is None:
        print("ERROR: Pasien tidak ditemukan.")
        return

    if pasien_data.get("nomor_kamar"):
        if pasien_data.get("nomor_kamar") == nomor_kamar:
            print("Pasien sudah berada di kamar tersebut.")
        else:
            print(f"Pasien sudah terdaftar di kamar {pasien_data.get('nomor_kamar')}.")
        return

    # Cari data kamar 
    kamar_data = _cari_kamar(data_kamar, nomor_kamar)

    if kamar_data is None:
        print("ERROR: Kamar tidak ditemukan.")
        return

    # mengubah dict ke objek Kamar
    kamar_obj = _dict_ke_objek(kamar_data)
    if nik in kamar_obj.pasien_terisi:
        print("Pasien sudah tercatat di kamar ini.")
        return

    if not kamar_obj.pasien_masuk(nik):
        return

    # Update data pasien menggunakan OOP
    pasien_obj = Pasien()
    pasien_obj.dict_ke_objek(pasien_data)
    pasien_obj.set_kamar(nomor_kamar)
    pasien_obj.update_status("dirawat")
    pasien_obj.update_layanan("Rawat Inap")
    pasien_data.update(pasien_obj.objek_ke_dict())

    kamar_data.update(kamar_obj.objek_ke_dict())
    save_json("data/kamar.json", data_kamar)
    save_json("data/pasien.json", data_pasien)

    print(f"Pasien {nik} berhasil ditempatkan ke kamar {nomor_kamar}.")


def pasien_keluar_kamar():
    """Mengeluarkan pasien dari kamar dan memperbarui data JSON."""
    data_kamar = load_json("data/kamar.json")
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK pasien: ").strip()

    # Cari data pasien
    pasien_data = _cari_pasien(data_pasien, nik)

    if pasien_data is None:
        print("ERROR: Pasien tidak ditemukan.")
        return

    nomor_kamar = pasien_data.get("nomor_kamar")
    if not nomor_kamar:
        print("ERROR: Pasien tidak tercatat di kamar manapun.")
        return

    # Cari data kamar
    kamar_data = _cari_kamar(data_kamar, nomor_kamar)

    if kamar_data is None:
        print("ERROR: Kamar tidak ditemukan.")
        return

    # Konversi dict → objek Kamar
    kamar_obj = _dict_ke_objek(kamar_data)
    if nik not in kamar_obj.pasien_terisi:
        print("ERROR: Pasien tidak ditemukan di kamar ini.")
        return

    kamar_obj.pasien_keluar(nik)

    # Update data pasien menggunakan OOP
    pasien_obj = Pasien()
    pasien_obj.dict_ke_objek(pasien_data)
    pasien_obj.set_kamar(None)
    pasien_obj.update_status("selesai")
    pasien_data.update(pasien_obj.objek_ke_dict())

    kamar_data.update(kamar_obj.objek_ke_dict())
    save_json("data/kamar.json", data_kamar)
    save_json("data/pasien.json", data_pasien)

    print(f"Pasien {nik} berhasil keluar dari kamar {nomor_kamar}.")


def navigasi_kamar():
    """Menavigasi kamar satu per satu secara interaktif (Next/Prev) menggunakan DLL."""
    dll = _bangun_dll()
    
    if dll.head is None:
        print("\nBelum ada data kamar.")
        return

    saat_ini = dll.head

    while True:
        
        print("\n======= NAVIGASI KAMAR RAWAT INAP =======")
        print(saat_ini.data.data_kamar())
        print("\n  [N] Kamar Berikutnya  [P] Kamar Sebelumnya  [0] Kembali")
        pilihan = input("  Pilih navigasi: ").strip().lower()
        
        if pilihan == '0':
            break
        elif pilihan == 'n':
            if saat_ini.next is not None:
                saat_ini = saat_ini.next
            else:
                print("  Anda sudah berada di ujung lorong terakhir.")
        elif pilihan == 'p':
            if saat_ini.prev is not None:
                saat_ini = saat_ini.prev
            else:
                print("  Anda sudah berada di ujung lorong pertama.")
        else:
            print("  ERROR: Pilihan tidak valid.")



def lihat_jadwal_obat_pasien():
    data_pasien = load_json("data/pasien.json")

    nik = input("Masukkan NIK pasien: ").strip()

    # Cari pasien
    pasien_data = _cari_pasien(data_pasien, nik)

    if pasien_data is None:
        print("ERROR: Pasien tidak ditemukan.")
        return

    if not pasien_data.get("nomor_kamar"):
        print(f"Pasien '{pasien_data['nama']}' belum dirawat inap (tidak memiliki kamar).")
        return

    # Bangun CLL jadwal default Pagi → Siang → Malam
    jadwal = CircularLinkedList()
    jadwal.tambah_jadwal("PAGI   — 07.00 WIB")
    jadwal.tambah_jadwal("SIANG  — 13.00 WIB")
    jadwal.tambah_jadwal("MALAM  — 19.00 WIB")

    print(f"\n=== JADWAL MINUM OBAT: {pasien_data['nama']} ===")
    print(f"    Kamar    : {pasien_data['nomor_kamar']}")
    print(f"    Layanan  : {pasien_data.get('layanan', '-')}")
    print()
    print("-" * 44)

    jadwal.lihat_jadwal(interaktif=True)