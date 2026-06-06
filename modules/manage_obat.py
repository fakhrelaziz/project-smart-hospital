from models.obat import Obat
from utils.json_handler import load_json, save_json
from modules.hash_obat import HashObat
from modules.recursive_stok import prediksi_stok_obat, tampilkan_hasil_prediksi
from modules.tree_katalog import KatalogObat


def _input_angka(angka):
    """Fungsi yang sering dipakai oleh function lain ketika ingin minta input
     dari pada setiap input harus menginisialisai code input terus, lebih baik di jadikan function 
    input angka dari user dengan Error Handling."""
    while True:
        try:
            nilai = int(input(angka))
            if nilai < 0:
                print("  ERROR: Input tidak boleh negatif. Silakan coba lagi.")
                continue
            return nilai
        except ValueError:
            print("  ERROR: Input harus berupa angka bulat. Silakan coba lagi.")

def lihat_obat():
    """Menampilkan seluruh data obat dari file JSON."""
    data_obat = load_json("data/obat.json")

    # Mengubah data mentah (dict) menjadi barisan Objek Obat
    daftar_objek_obat = []
    for i in data_obat:
        obat_obj = Obat()
        obat_obj.dict_ke_objek(i)
        daftar_objek_obat.append(obat_obj)

    # Menampilkan data menggunakan fungsi dari class Obat
    print("\n--- DAFTAR OBAT RUMAH SAKIT ---")
    for i in daftar_objek_obat:
        print(i.data_obat())
        print("─" * 42)

    print(f"  Total: {len(data_obat)} jenis obat")

def tambah_obat():
    """Menambahkan obat baru ke data JSON."""
    data_obat = load_json("data/obat.json")

    kode = input("Masukkan kode obat: ")

    for i in data_obat:
        if i.get("kode") == kode:
            print(f"\nGAGAL! Kode '{kode}' sudah dipakai oleh obat '{i.get('nama')}'.")
            return

    nama = input("Masukkan nama: ")
    kategori = input("Masukkan kategori: ")
    bentuk = input("Masukkan bentuk (Tablet/Kapsul/Sirup dll): ")
    stok = _input_angka("Berapa stok?:  ")
    harga = _input_angka("Harga: ")
    pemakaian_harian = _input_angka("Rata-rata pemakaian RS per hari: ")
     
    obat_baru = Obat(kode, nama, kategori, bentuk, stok, harga, pemakaian_harian)
    data_obat.append(obat_baru.objek_ke_dict())

    save_json("data/obat.json", data_obat)

    print("Obat berhasil ditambahkan")



def cari_obat_kode():
    """Mencari obat menggunakan kode obat."""
    data_obat = load_json("data/obat.json")
    if not data_obat:
        print("Data obat kosong")
        return

    # 1. Bangun Hash Table O(1)
    hash_tabel = HashObat()
    for i in data_obat:
        hash_tabel.insert(i['kode'], i)

    print("\n--- PENCARIAN OBAT (HASH TABLE) ---")
    kode_cari = input("Masukkan kode obat yang dicari: ").strip()
    hasil = hash_tabel.get(kode_cari)

    if hasil:
        # 3. Tampilkan jika ketemu
        hash_tabel.cetak_obat(hasil)
        
        # 4. Tampilkan Sub-Menu Aksi Lanjutan
        print("\n  [Aksi Lanjutan]")
        print("  [1] Ubah Stok")
        print("  [2] Ubah Harga")
        print("  [3] Lihat Prediksi Sisa Hari Stok")
        print("  [0] Selesai & Kembali")
        pilihan = input("  Pilih aksi: ").strip()

        obat_obj = Obat()
        obat_obj.dict_ke_objek(hasil)

        if pilihan == "1":
            aksi = input("Pilih aksi [1] Tambah [2] Kurang: ").strip()
            jumlah = _input_angka("Jumlah stok: ")
            
            if aksi == "1":
                print(obat_obj.tambah_stok(jumlah))
            elif aksi == "2":
                print(obat_obj.kurang_stok(jumlah))
            
            # Update List JSON & Save
            for i in data_obat:
                if i['kode'] == kode_cari:
                    i['stok'] = obat_obj.stok
                    break

        elif pilihan == "2":
            harga_baru = _input_angka("Harga baru: ")
            print(obat_obj.ubah_harga(harga_baru))
            
            # Update List JSON & Save
            for i in data_obat:
                if i['kode'] == kode_cari:
                    i['harga'] = obat_obj.harga
                    break
                
        elif pilihan == "3":
            hasil_prediksi = prediksi_stok_obat(obat_obj.nama, obat_obj.stok, obat_obj.pemakaian_harian)
            tampilkan_hasil_prediksi(hasil_prediksi)
            
    
    save_json("data/obat.json", data_obat)


def tampilkan_katalog():
    """menampilkan katalog obat dalam bentuk direktori."""
    print("\n" + "=" * 52)
    print("             KATALOG OBAT FARMASI")
    print("          Struktur Data: General Tree")
    print("=" * 52)

    katalog = KatalogObat()
    katalog.tampilkan()
    print("=" * 52)
