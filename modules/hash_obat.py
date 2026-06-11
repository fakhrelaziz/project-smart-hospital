
class HashObat:
    def __init__(self, ukuran = 20): 
        #1. Menentukan ukuran 
        self._ukuran = ukuran
        
        #2. Setiap slot diisi Dictionary kosong {} untuk wadah obat yang tabrakan (Chaining)
        self._tabel = [{} for _ in range(ukuran)]

        #3. Pengingat jumlah total seluruh obat yang sukses tersimpan di dalam lemari
        self._total_obat = 0

    def hash_function(self, kode_obat):

        total_ascii = 0
        #itung nilai huruf dari kode obatnya satu-satu
        for i in kode_obat:
            #mengubah huruf jadi angka angka satu-satu
            total_ascii += ord(i)  
        return total_ascii % self._ukuran 

    def insert(self, kode_obat, detail_obat):
        #Memasukkan atau memperbarui data obat lama langsung ke slot yang ditentukan oleh fungsi hash
        index = self.hash_function(kode_obat) 
        
        #cek dulu, kalau kodenya belum pernah ada di slot ini, berarti statusnya obat baru
        if kode_obat not in self._tabel[index]:
            self._total_obat += 1
            
        #langsung simpan/timpa ke dalam dictionary slot tujuan secara diam-diam
        self._tabel[index][kode_obat] = detail_obat

    def get(self, kode_obat):
        #6. Mencari detail obat secara cepat dengan langsung menuju slot yang ditentukan oleh fungsi hash
        index = self.hash_function(kode_obat)  
        
        #bbuka pintu slotnya, langsung panggil kodenya (kalau gak ada, komputer ngasih None)
        return self._tabel[index].get(kode_obat, None)
    

    def cetak_obat(self, detail):
        if detail is None :
            print("Obat tidak ditemukan.")
        else:
            print(f"\n  • Nama     : {detail.get('nama')}")
            print(f"  • Kategori : {detail.get('kategori')}")
            print(f"  • Stok     : {detail.get('stok')}")
            print(f"  • Harga    : Rp{detail.get('harga')}")