import csv
import os

nama_file = "ecommerce_dataset_updated.csv"
batas_baris = 1000
header_batua = ["User_ID", "Product_ID", "Category", "Price (Rs.)", "Discount (%)",
                "Final_Price(Rs.)", "Payment_Method", "Purchase_Date"]


def validasi_data(kolom):
    if len(kolom) != 8:
        return "Jumlah kolom harus 8"
    for k in kolom:
        if k.strip() == "":
            return "Semua kolom harus terisi"

    for i in range(3, 6):
        if not kolom[i].strip().replace(".", "", 1).isdigit():
            return "Price, Discount, dan Final Price harus angka"
    harga = float(kolom[3])
    diskon = float(kolom[4])
    if harga <= 0:
        return "Price harus lebih dari 0"
    if diskon < 0 or diskon > 100:
        return "Discount harus antara 0 sampai 100"

    tanggal = kolom[7].strip().split("-")
    if len(tanggal) != 3:
        return "Tanggal harus format DD-MM-YYYY"
    hari, bulan, tahun = tanggal
    if not (hari.isdigit() and bulan.isdigit() and tahun.isdigit()):
        return "Tanggal harus format DD-MM-YYYY"
    if len(hari) != 2 or len(bulan) != 2 or len(tahun) != 4:
        return "Tanggal harus format DD-MM-YYYY"
    if int(hari) < 1 or int(hari) > 31:
        return "Tanggal tidak valid"
    if int(bulan) < 1 or int(bulan) > 12:
        return "Tanggal tidak valid"
    if int(tahun) < 2000 or int(tahun) > 2100:
        return "Tanggal tidak valid"

    batas_hari = 31
    if int(bulan) in [4, 6, 9, 11]:
        batas_hari = 30
    elif int(bulan) == 2:
        if int(tahun) % 4 == 0 and (int(tahun) % 100 != 0 or int(tahun) % 400 == 0):
            batas_hari = 29
        else:
            batas_hari = 28
    if int(hari) > batas_hari:
        return "Tanggal tidak valid"

    if round(harga * (1 - diskon / 100), 2) != float(kolom[5]):
        return "Final Price tidak sesuai dengan Price dan Discount"
    return ""

def baca_data():
    data = []
    dibaca = 0
    with open(nama_file, "r", newline="", encoding="utf-8-sig") as f:
        pembaca = csv.reader(f)
        if next(pembaca) != header_batua:
            print("Header salah atau tidak sesuai")
            return None, 0
        for baris in pembaca:
            dibaca += 1
            if validasi_data(baris) == "":
                for i in range(8):
                    baris[i] = baris[i].strip()
                data.append(baris)
    return data, dibaca

def urutkan(nilai_urut, semua_list, menurun=False):
   
    n = len(nilai_urut)
    for i in range(n - 1):
        idx = i
        for j in range(i + 1, n):
            if menurun and nilai_urut[j] > nilai_urut[idx]:
                idx = j
            elif not menurun and nilai_urut[j] < nilai_urut[idx]:
                idx = j
        if idx != i:
            for lst in semua_list:
                lst[i], lst[idx] = lst[idx], lst[i]

def tampilkan_daftar(data, daftar):
    if len(daftar) == 0:
        print("Data tidak ditemukan.")
        return
    kop = ("-" * 105 + "\n" + "No".ljust(7) + "User_ID".ljust(10) + "Product_ID".ljust(14)
           + "Category".ljust(16) + "Price".rjust(9) + "Disc".rjust(6) + "Final".rjust(10)
           + "  " + "Metode".ljust(18) + "Tanggal\n" + "-" * 105)
    print(kop)
    jumlah = 0
    for idx in daftar:
        b = data[idx]
        print(str(idx + 1).ljust(7) + b[0].ljust(10) + b[1].ljust(14) + b[2].ljust(16) + b[3].rjust(9)
              + b[4].rjust(6) + b[5].rjust(10) + "  " + b[6].ljust(18) + b[7])
        jumlah += 1
        if jumlah % 20 == 0 and jumlah < len(daftar):
            if input("-- %d/%d -- Enter = lanjut, q = berhenti: " % (jumlah, len(daftar))).lower() == "q":
                break
            print(kop)
    print("Total data:", len(daftar))

def menu_tampilkan(data):
    print("\nTAMPILKAN DATA\n1. Tampilkan semua data\n2. Filter berdasarkan metode pembayaran")
    pilihan = input("Pilih (1-2): ").strip()
    daftar = []
    if pilihan == "1":
        for i in range(len(data)):
            daftar.append(i)
    elif pilihan == "2":
        metode = []
        for b in data:
            if b[6] not in metode:
                metode.append(b[6])
        metode.sort()
        for i in range(len(metode)):
            print(str(i + 1) + ". " + metode[i])
        pil = input("Pilih metode: ").strip()
        if not (pil.isdigit() and 1 <= int(pil) <= len(metode)):
            print("Pilihan tidak valid.")
            return
        for i in range(len(data)):
            if data[i][6] == metode[int(pil) - 1]:
                daftar.append(i)
    else:
        print("Pilihan tidak valid.")
        return
    tampilkan_daftar(data, daftar)

def minta_data(lama):
    baru = []
    for i in range(8):
        if i == 5:
            baru.append("")
            continue
        petunjuk = ""
        if lama is not None:
            petunjuk = " [" + lama[i] + "]"
        teks = input(header_batua[i] + petunjuk + ": ").strip()
        if teks == "" and lama is not None:
            teks = lama[i]  # Enter = pakai nilai lama
        baru.append(teks)
    if baru[3].replace(".", "", 1).isdigit() and baru[4].replace(".", "", 1).isdigit():
        baru[5] = "%.2f" % round(float(baru[3]) * (1 - float(baru[4]) / 100), 2)
    else:
        print("Data tidak valid: Price dan Discount harus angka\nData tidak disimpan.")
        return None
    pesan = validasi_data(baru)
    if pesan != "":
        print("Data tidak valid:", pesan, "\nData tidak disimpan.")
        return None
    return baru

def pilih_data(data, judul):
    print("\n" + judul)
    teks = input("Masukkan No data: ").strip()
    if not teks.isdigit() or int(teks) < 1 or int(teks) > len(data):
        print("Nomor tidak valid.")
        return -1
    tampilkan_daftar(data, [int(teks) - 1])
    return int(teks) - 1

def tambah_ubah_data(data, ubah=False):
    if ubah:
        idx = pilih_data(data, "UBAH DATA")
        if idx == -1:
            return
        print("Tekan Enter untuk mempertahankan nilai lama. Final Price dihitung otomatis.")
        baru = minta_data(data[idx])
    else:
        print("\nTAMBAH DATA (Final Price dihitung otomatis)")
        baru = minta_data(None)
    if baru is None:
        return
    if ubah:
        data[idx] = baru
        print("Data berhasil diubah.")
    else:
        data.append(baru)
        print("Data berhasil ditambahkan dengan No", len(data), "| Final Price =", baru[5])

def hapus_data(data):
    idx = pilih_data(data, "HAPUS DATA")
    if idx != -1 and input("Yakin ingin menghapus? (y/n): ").strip().lower() == "y":
        data.pop(idx)
        print("Data berhasil dihapus.")

def cari_data(data):
    kata = input("\nCARI DATA\nKata kunci (User_ID/Product_ID/Category/Metode/Tanggal): ").strip().lower()
    daftar = []
    for i in range(len(data)):
        b = data[i]
        if kata != "" and kata in (b[0] + " " + b[1] + " " + b[2] + " " + b[6] + " " + b[7]).lower():
            daftar.append(i)
    tampilkan_daftar(data, daftar)

def hitung_rekap(data, mode):

    daftar_kunci = []
    for b in data:
        if mode == "diskon":
            k = float(b[4])
        elif mode == "kategori":
            k = b[2]
        elif float(b[3]) < 150:
            k = "<150"
        elif float(b[3]) < 300:
            k = "150-<300"
        else:
            k = ">=300"
        daftar_kunci.append(k)

    kunci = []
    if mode == "rentang":
        kunci = ["<150", "150-<300", ">=300"]
    else:
        for k in daftar_kunci:
            if k not in kunci:
                kunci.append(k)
    jml = [0] * len(kunci)
    awal = [0] * len(kunci)
    akhir = [0] * len(kunci)
    for j in range(len(data)):
        i = kunci.index(daftar_kunci[j])
        jml[i] += 1
        awal[i] += float(data[j][3])
        akhir[i] += float(data[j][5])
    if mode == "diskon":
        urutkan(kunci, [kunci, jml, awal, akhir])  # level diskon diurutkan naik
    return kunci, jml, awal, akhir

def tabel_rekap(data, mode, judul, nama_kolom):
    kunci, jml, awal, akhir = hitung_rekap(data, mode)
    print("\n" + judul + "\n" + "-" * 78)
    if mode == "diskon":
        print(nama_kolom.ljust(9) + "Jumlah".rjust(8) + "Rata Harga Awal".rjust(20)
              + "Rata Harga Akhir".rjust(21) + "Rata Potongan".rjust(20))
    else:
        print(nama_kolom.ljust(20) + "Jumlah".rjust(8) + "Rata Harga Akhir".rjust(22))
    print("-" * 78)
    for i in range(len(kunci)):
        rata_awal = 0
        rata_akhir = 0
        if jml[i] > 0:
            rata_awal = awal[i] / jml[i]
            rata_akhir = akhir[i] / jml[i]
        if mode == "diskon":
            print((str(int(kunci[i])) + "%").ljust(9) + str(jml[i]).rjust(8) + ("%.2f" % rata_awal).rjust(20)
                  + ("%.2f" % rata_akhir).rjust(21) + ("%.2f" % (rata_awal - rata_akhir)).rjust(20))
         else:
                   print(kunci[i].ljust(20) + str(jml[i]).rjust(8) + ("%.2f" % rata_akhir).rjust(22))
       
def tampil_terbanyak(data):
    print("\nRingkasan Transaksi Terbanyak\n" + "-" * 78)
    kunci, jml, _, _ = hitung_rekap(data, "diskon")
    i = jml.index(max(jml))
    print("Level diskon terbanyak  : %d%% (%d transaksi)" % (int(kunci[i]), jml[i]))
    kunci, jml, _, _ = hitung_rekap(data, "rentang")
    i = jml.index(max(jml))
    print("Rentang harga terbanyak : %s (%d transaksi)" % (kunci[i], jml[i]))

def tabel_d(data):
    nama, jumlah, _, total_akhir = hitung_rekap(data, "kategori")
    tunai = [0] * len(nama)
    nontunai = [0] * len(nama)
    for b in data:
        i = nama.index(b[2])
        if b[6] == "Cash on Delivery":
            tunai[i] += 1
        else:
            nontunai[i] += 1

    dominan = []
    nilai_urut = []
    for i in range(len(nama)):
        if tunai[i] > nontunai[i]:
            dominan.append("Tunai")
        elif nontunai[i] > tunai[i]:
            dominan.append("Non-tunai")
        else:
            dominan.append("Sama")
        nilai_urut.append(max(tunai[i], nontunai[i]))

    urutkan(nilai_urut, [nama, jumlah, total_akhir, tunai, nontunai, dominan, nilai_urut], menurun=True)

    print("\nTABEL D. Tunai dan Nontunai Mana Paling Banyak\n" + "-" * 78)
    print("No".ljust(5) + "Kategori".ljust(20) + "Tunai".rjust(8) + "Non-Tunai".rjust(12) + "Dominan".rjust(14))
    print("-" * 78)
    for i in range(len(nama)):
        print(str(i + 1).ljust(5) + nama[i].ljust(20) + str(tunai[i]).rjust(8)
              + str(nontunai[i]).rjust(12) + dominan[i].rjust(14))

def menu_ringkasan(data):
    data = data[:batas_baris]
    if len(data) == 0:
        print("Belum ada data untuk diringkas.")
        return
    print("\nBaris dianalisis:", len(data))
    while True:
        print("\nMENU RINGKASAN\n1. Tabel A - Per Level Diskon\n2. Tabel B - Per Kategori Produk\n"
              "3. Tabel C - Per Rentang Harga\n4. Ringkasan Transaksi Terbanyak\n"
              "5. Tabel D - Tunai dan Non-Tunai\n6. Tampilkan Semua\n0. Kembali")
        p = input("Pilih menu (0-6): ").strip()
        if p == "0":
            return
        if p not in ["1", "2", "3", "4", "5", "6"]:
            print("Pilihan tidak valid, masukkan angka 0 sampai 6.")
            continue
        if p == "1" or p == "6":
            tabel_rekap(data, "diskon", "TABEL A. Rekap Per Level Diskon", "Diskon")
        if p == "2" or p == "6":
            tabel_rekap(data, "kategori", "TABEL B. Rekap Per Kategori Produk", "Kategori")
        if p == "3" or p == "6":
            tabel_rekap(data, "rentang", "TABEL C. Rekap Per Rentang Harga", "Rentang Harga")
        if p == "4" or p == "6":
            tampil_terbanyak(data)
        if p == "5" or p == "6":
            tabel_d(data)

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