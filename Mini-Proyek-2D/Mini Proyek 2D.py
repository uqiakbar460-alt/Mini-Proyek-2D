import os

header=["User_ID","Product_ID","Category","Price (Rs.)","Discount","Final_Price (Rs.)","Payment_Method","Purchase_Date"]

def file(file):
    return os.path.exists(file)

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
    if not tanggal_valid:
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
