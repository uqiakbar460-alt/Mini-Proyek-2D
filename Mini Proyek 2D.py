import os

header_batua = ["User_ID", "Product_ID", "Category", "Price (Rs.)", "Discount (%)", "Final_Price(Rs.)", "Payment_Method", "Purchase_Date"]

def file_ada(nama_file):
    return os.path.exists(nama_file)

def angka_valid(teks):
    teks=teks.strip()
    if teks == "":
        return False
    bagian = teks.split(".")
    if len (bagian) > 2:
        return False
    for b in bagian:
        if not b.isdigit():
            return False

    return True

def tanggal_valid(teks):
    bagian =teks.strip().split("-")
    if len(bagian) != 3:
        return False
    hari,bulan,tahun=bagian
    if not(hari.isdigit() and bulan.isdigit() and tahun.isdigit()):
        return False
    if len(hari) !=2 or len(bulan) !=2 or len(tahun) !=4:
        return False
    if int(hari)<1 or int(hari)>31:
        return False
    if int(bulan)<1 or int(bulan)>12:
        return False
    if int(tahun)<2000 or int(tahun)>2100:
        return False

    batas_hari = 31
    if int(bulan) in [4, 6, 9, 11]:
        batas_hari = 30
    elif int(bulan) == 2:
        if int(tahun) % 4 == 0 and (int(tahun) % 100 != 0 or int(tahun) % 400 == 0):
            batas_hari = 29
        else:
            batas_hari = 28
    if int(hari) > batas_hari:
        return False
    
    return True

def baris_valid(kolom):
    if len (kolom) !=8:
        return False
    for k in kolom:
        if k.strip()=="":
            return False

    if not(angka_valid(kolom[3]) and angka_valid(kolom[4]) and angka_valid(kolom[5])):
           return False

    harga =float(kolom[3])
    diskon=float(kolom[4])
    harga_akhir=float(kolom[5])
    if harga <= 0 :
        return False
    if diskon <0 or diskon > 100:
        return False
    if not tanggal_valid(kolom[7]):
        return False
    if round(harga * (1-diskon / 100), 2) !=harga_akhir:
        return False
    
    return True

def rentang_harga(harga):
    if harga < 150:
        return "<150"
    elif harga < 300:
        return "150-<300"
    else:
        return ">=300"

def grup_metode(metode):
    if metode == "Cash on Delivery":
        return "Tunai"
    else:
        return "Non-Tunai"
    
def perbarui_diskon(nama, jumlah, total_awal, total_akhir,
                    diskon, harga, harga_akhir):
    if diskon in nama:
        idx = nama.index(diskon)
    else:  
        nama.append(diskon)
        jumlah.append(0)
        total_awal.append(0)
        total_akhir.append(0)
        idx = len(nama) - 1
    jumlah[idx] += 1
    total_awal[idx] += harga
    total_akhir[idx] += harga_akhir

def perbarui_kategori(nama, jumlah, total_akhir, tunai, nontunai, kategori, harga_akhir, grup):
    if kategori in nama:
        idx = nama.index (kategori)
    else:
        nama.append(kategori)
        jumlah.append(0)
        total_akhir.append(0)
        tunai.append(0)
        nontunai.append(0)
        idx = len(nama) - 1
    jumlah[idx] += 1
    total_akhir[idx] += harga_akhir
    if grup == "Tunai":
        tunai[idx] += 1
    else:
        nontunai[idx] += 1

def perbarui_rentang(nama,jumlah,total_akhir,rentang,harga_akhir):
    if rentang in nama:
        idx=nama.index(rentang)
    else:
        nama.append(rentang)
        jumlah.append(0)
        total_akhir.append(0)
        idx = len(nama) - 1
    jumlah[idx] += 1
    total_akhir[idx] += harga_akhir

def baca_dan_olahdata(nama_file, batas_baris):
    #inisialisasi
    jumlah_dibaca=0
    jumlah_valid=0
    jumlah_tidak_valid=0
    jumlah_dihitung=0

    #Rekap A
    diskon_nama=[]
    diskon_jumlah=[]
    diskon_total_awal=[]
    diskon_total_akhir=[]

    #Rekap B
    kategori_nama=[]
    kategori_jumlah=[]
    kategori_total_akhir=[]
    kategori_tunai=[]
    kategori_nontunai=[]

    #Rekap C 
    rentang_nama=[]
    rentang_jumlah=[]
    rentang_total_akhir=[]

    with open(nama_file, "r", encoding="utf-8-sig") as f:
        header = f.readline().strip().split(",")
        for i in range(len(header)):
            header[i]= header[i].strip()
        if header != header_batua:
            print("Header Salah atau Tidak Sesuai")
            return None

        for baris in f:
            jumlah_dibaca += 1
            kolom= baris.strip().split(",")
            if not baris_valid(kolom):
                jumlah_tidak_valid += 1
            else :
                jumlah_valid += 1
                if jumlah_dihitung < batas_baris:
                    harga = float(kolom[3])
                    diskon = float(kolom[4])
                    harga_akhir = float(kolom[5])
                    rentang = rentang_harga(harga)
                    grup=grup_metode(kolom[6].strip())
                    perbarui_diskon(diskon_nama,diskon_jumlah,diskon_total_awal,diskon_total_akhir,diskon,harga,harga_akhir)
                    perbarui_kategori(kategori_nama, kategori_jumlah, kategori_total_akhir,
                  kategori_tunai, kategori_nontunai,
                  kolom[2].strip(), harga_akhir, grup)
                    perbarui_rentang(rentang_nama,rentang_jumlah,rentang_total_akhir,rentang,harga_akhir)
                    jumlah_dihitung += 1

        hasil = {
            "jumlah_dibaca": jumlah_dibaca,
            "jumlah_valid": jumlah_valid,
            "jumlah_tidak_valid": jumlah_tidak_valid,
            "jumlah_dihitung": jumlah_dihitung,
            "diskon_nama": diskon_nama,
            "diskon_jumlah": diskon_jumlah,
            "diskon_total_awal": diskon_total_awal,
            "diskon_total_akhir": diskon_total_akhir,
            "kategori_nama": kategori_nama,
            "kategori_jumlah": kategori_jumlah,
            "kategori_total_akhir": kategori_total_akhir,
            "kategori_tunai": kategori_tunai,
            "kategori_nontunai": kategori_nontunai,
            "rentang_nama": rentang_nama,
            "rentang_jumlah": rentang_jumlah,
            "rentang_total_akhir": rentang_total_akhir,
        }
        return hasil

def main():
    nama_file = "ecommerce_dataset_updated.csv"
    batas_baris = 1000

    if not file_ada(nama_file):
        print("File tidak ditemukan")
        return

    hasil = baca_dan_olahdata(nama_file, batas_baris)
    if hasil is None:
        return

    if hasil["jumlah_valid"] == 0:
        print("Dataset kosong atau hanya header")
        return
    print(hasil)

main()
