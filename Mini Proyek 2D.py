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

def urutkan_diskon(nama, jumlah, total_awal, total_akhir):
    n = len(nama)
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if nama[j] < nama[idx_min]:
                idx_min = j
        if idx_min != i:
            nama[i], nama[idx_min] = nama[idx_min], nama[i]
            jumlah[i], jumlah[idx_min] = jumlah[idx_min], jumlah[i]
            total_awal[i], total_awal[idx_min] = total_awal[idx_min], total_awal[i]
            total_akhir[i], total_akhir[idx_min] = total_akhir[idx_min], total_akhir[i]


def urutkan_kategori(nama, jumlah, total_akhir, tunai, nontunai, dominan, nilai_urut):
    n = len(nama)
    for i in range(n - 1):
        idx_maks = i
        for j in range(i + 1, n):
            if nilai_urut[j] > nilai_urut[idx_maks]:
                idx_maks = j
        if idx_maks != i:
            nama[i], nama[idx_maks] = nama[idx_maks], nama[i]
            jumlah[i], jumlah[idx_maks] = jumlah[idx_maks], jumlah[i]
            total_akhir[i], total_akhir[idx_maks] = total_akhir[idx_maks], total_akhir[i]
            tunai[i], tunai[idx_maks] = tunai[idx_maks], tunai[i]
            nontunai[i], nontunai[idx_maks] = nontunai[idx_maks], nontunai[i]
            dominan[i], dominan[idx_maks] = dominan[idx_maks], dominan[i]
            nilai_urut[i], nilai_urut[idx_maks] = nilai_urut[idx_maks], nilai_urut[i]

def cari_terbanyak(nama, jumlah):
    terbanyak = 0
    nama_terbanyak = "-"
    for i in range(len(nama)):
        if jumlah[i] > terbanyak:
            terbanyak = jumlah[i]
            nama_terbanyak = nama[i]
    return nama_terbanyak, terbanyak
    
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

def hitung_rata(total,jumlah):
    if jumlah > 0:
        return total / jumlah
    else:
        return 0
def metode_dominan(tunai, nontunai):
    if tunai > nontunai:
        return "Tunai", tunai
    if nontunai > tunai:
        return "Non-tunai", nontunai
    else:
        return "sama", tunai

def tampilkan_ringkasan_baris(hasil):
    garis = "=" * 78

    print(garis)
    print("Rekap Transaksi E-Commerce 2024")
    print(garis)
    print("Baris dibaca        :", hasil["jumlah_dibaca"])
    print("Baris valid         :", hasil["jumlah_valid"])
    print("Baris tidak valid   :", hasil["jumlah_tidak_valid"])
    print("Baris dianalisis    :", hasil["jumlah_dihitung"])

def tampilkan_tabel_a(hasil):
    d_nama = hasil["diskon_nama"]
    d_jumlah = hasil["diskon_jumlah"]
    d_awal = hasil["diskon_total_awal"]
    d_akhir = hasil["diskon_total_akhir"]
  

    print()
    print("TABEL A. Rekap Per Level Diskon")
    print("-" * 78)
    print("Diskon".ljust(9) + "Jumlah".rjust(8) + "Rata Harga Awal".rjust(20)
          + "Rata Harga Akhir".rjust(21) + "Rata Potongan".rjust(20))
    print("-" * 78)
    for i in range(len(d_nama)):
        rata_awal = hitung_rata(d_awal[i], d_jumlah[i])
        rata_akhir = hitung_rata(d_akhir[i], d_jumlah[i])
        potongan = rata_awal - rata_akhir
        print((str(int(d_nama[i])) + "%").ljust(9) + str(d_jumlah[i]).rjust(8)
              + ("%.2f" % rata_awal).rjust(20) + ("%.2f" % rata_akhir).rjust(21)
              + ("%.2f" % potongan).rjust(20))

def tampilkan_tabel_b(hasil):
    k_nama = hasil["kategori_nama"]
    k_jumlah = hasil["kategori_jumlah"]
    k_akhir = hasil["kategori_total_akhir"]
  

    print()
    print("TABEL B. Rekap Per Kategori Produk")
    print("-" * 78)
    print("Kategori".ljust(20) + "Jumlah".rjust(8) + "Rata Harga Akhir".rjust(22))
    print("-" * 78)
    for i in range(len(k_nama)):
        rata = hitung_rata(k_akhir[i], k_jumlah[i])
        print(k_nama[i].ljust(20) + str(k_jumlah[i]).rjust(8) + ("%.2f" % rata).rjust(22))

def tampilkan_tabel_c(hasil):
    r_nama = hasil["rentang_nama"]
    r_jumlah = hasil["rentang_jumlah"]
    r_akhir = hasil["rentang_total_akhir"]
    urutan_rentang = ["<150", "150-<300", ">=300"]

    print()
    print("TABEL C. Rekap Per Rentang Harga")
    print("-" * 78)
    print("Rentang Harga".ljust(20) + "Jumlah".rjust(8) + "Rata Harga Akhir".rjust(22))
    print("-" * 78)
    for nama_r in urutan_rentang:
        if nama_r in r_nama:
            idx = r_nama.index(nama_r)
            jml = r_jumlah[idx]
            rata = hitung_rata(r_akhir[idx], jml)
        else:
            jml = 0
            rata = 0
        print(nama_r.ljust(20) + str(jml).rjust(8) + ("%.2f" % rata).rjust(22))

def tampilkan_terbanyak(hasil):
    level_t, jml_level_t = cari_terbanyak(hasil["diskon_nama"], hasil["diskon_jumlah"])
    rentang_t, jml_rentang_t = cari_terbanyak(hasil["rentang_nama"], hasil["rentang_jumlah"])

    print()
    print("Ringkasan Transaksi Terbanyak")
    print("-" * 78)
    if jml_level_t > 0:
        print("Level diskon terbanyak  : %d%% (%d transaksi)" % (int(level_t), jml_level_t))
    else:
        print("Level diskon terbanyak  : -")
    print("Rentang harga terbanyak : %s (%d transaksi)" % (rentang_t, jml_rentang_t))
    
def tampilkan_tabel_d(hasil):
    k_nama = hasil["kategori_nama"][:]
    k_jumlah = hasil["kategori_jumlah"][:]
    k_akhir = hasil["kategori_total_akhir"][:]
    k_tunai = hasil["kategori_tunai"][:]
    k_nontunai = hasil["kategori_nontunai"][:]

    k_dominan = []
    k_nilai_urut = []
    for i in range(len(k_nama)):
        dom, nilai = metode_dominan(k_tunai[i], k_nontunai[i])
        k_dominan.append(dom)
        k_nilai_urut.append(nilai)

    urutkan_kategori(k_nama, k_jumlah, k_akhir, k_tunai, k_nontunai, k_dominan, k_nilai_urut)

    print()
    print("TABEL D. Tunai dan Nontunai Mana Paling banyak)")
    print("-" * 78)
    print("No".ljust(5) + "Kategori".ljust(20) + "Tunai".rjust(8) + "Non-Tunai".rjust(12)
          + "Dominan".rjust(14))
    print("-" * 78)
    for i in range(len(k_nama)):
        print(str(i + 1).ljust(5) + k_nama[i].ljust(20) + str(k_tunai[i]).rjust(8)
              + str(k_nontunai[i]).rjust(12) + k_dominan[i].rjust(14))
    print("=" * 78)

def tampilkan_semua(hasil):
    tampilkan_tabel_a(hasil)
    tampilkan_tabel_b(hasil)
    tampilkan_tabel_c(hasil)
    tampilkan_terbanyak(hasil)
    tampilkan_tabel_d(hasil)

def tampilkan_menu():
    print()
    print("MENU TAMPILAN OUTPUT")
    print("1. Tabel A - Rekap Per Level Diskon")
    print("2. Tabel B - Rekap Per Kategori Produk")
    print("3. Tabel C - Rekap Per Rentang Harga")
    print("4. Ringkasan Transaksi Terbanyak")
    print("5. Tabel D - Tunai dan Non-Tunai")
    print("6. Tampilkan Semua")
    print("0. Keluar")

def menu_output(hasil):
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-6): ").strip()

        if pilihan == "1":
            tampilkan_tabel_a(hasil)
        elif pilihan == "2":
            tampilkan_tabel_b(hasil)
        elif pilihan == "3":
            tampilkan_tabel_c(hasil)
        elif pilihan == "4":
            tampilkan_terbanyak(hasil)
        elif pilihan == "5":
            tampilkan_tabel_d(hasil)
        elif pilihan == "6":
            tampilkan_semua(hasil)
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid, masukkan angka 0 sampai 6.")


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

def jalan_program():
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

    urutkan_diskon(hasil["diskon_nama"], hasil["diskon_jumlah"],
                   hasil["diskon_total_awal"], hasil["diskon_total_akhir"])
    tampilkan_ringkasan_baris(hasil)
    menu_output(hasil)
   
jalan_program()