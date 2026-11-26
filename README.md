# Aplikasi Pengelolaan dan Rekapitulasi Data Transaksi E-Commerce Tahun 2024

Program Python berbasis terminal untuk mengelola dan merangkum data transaksi e-commerce dari file CSV. Proyek ini dibuat sebagai Mini Proyek 2D.

## Latar Belakang

Transaksi e-commerce menghasilkan data dalam jumlah besar: harga produk, besar diskon, harga akhir, dan metode pembayaran. Data mentah seperti ini sulit dibaca langsung. Selain itu, file data sering berisi baris yang salah, misalnya kolom kosong, harga bukan angka, tanggal tidak valid, atau harga akhir yang tidak cocok dengan perhitungan diskon.

Program ini membantu membaca data tersebut, menyaring baris yang tidak valid, lalu menyajikan rekap yang mudah dipahami, seperti rata-rata harga per level diskon, per kategori, dan per rentang harga.

## Tujuan

1. Membaca data transaksi dari file CSV dan memeriksa keabsahan setiap barisnya.
2. Menyediakan fitur pengelolaan data (tampil, tambah, ubah, hapus, dan cari).
3. Menyajikan rekap transaksi dalam bentuk tabel ringkasan.
4. Menerapkan konsep dasar pemrograman Python: fungsi, list, perulangan, percabangan, kelas, dan algoritma pengurutan manual.

## Fitur Utama

| Menu | Fitur | Keterangan |
|---|---|---|
| a | Tampilkan data | Semua data atau difilter berdasarkan metode pembayaran. Tampil per 20 baris. |
| b | Tambah data | Final Price dihitung otomatis dari Price dan Discount. |
| c | Hapus data | Berdasarkan nomor data, dengan konfirmasi (y/n). |
| d | Ubah data | Tekan Enter untuk mempertahankan nilai lama. |
| e | Cari data | Berdasarkan User_ID, Product_ID, Category, metode pembayaran, atau tanggal. |
| f | Ringkasan | Menampilkan Tabel A sampai D dan ringkasan transaksi terbanyak. |
| g | Keluar | Menutup program. |

Isi menu Ringkasan:

- **Tabel A**: rekap per level diskon (jumlah, rata-rata harga awal, rata-rata harga akhir, rata-rata potongan).
- **Tabel B**: rekap per kategori produk.
- **Tabel C**: rekap per rentang harga (`<150`, `150-<300`, `>=300`).
- **Ringkasan transaksi terbanyak**: level diskon dan rentang harga dengan transaksi paling banyak.
- **Tabel D**: perbandingan pembayaran tunai (Cash on Delivery) dan non-tunai per kategori, beserta mana yang dominan.

## Metodologi

1. **Membaca data.** File dibaca dengan modul `csv`. Header diperiksa dan harus sama dengan format yang ditentukan.
2. **Validasi.** Setiap baris diperiksa oleh fungsi `validasi_data`. Baris yang tidak lolos tidak dimasukkan ke analisis dan dihitung sebagai "baris tidak valid".
3. **Penyimpanan di memori.** Baris yang valid disimpan dalam list, lalu dipakai oleh semua menu.
4. **Rekap.** Pengelompokan dan penjumlahan dilakukan manual dengan list dan perulangan, tanpa library tambahan.
5. **Pengurutan.** Menggunakan algoritma selection sort yang ditulis sendiri (fungsi `urutkan`): level diskon diurutkan naik, dan kategori pada Tabel D diurutkan menurun berdasarkan jumlah metode dominan.
6. **Struktur program.** Logika menu dibungkus dalam kelas `AplikasiRekap`, dan perhitungan Tabel D dalam kelas `TabelD`.

Aturan validasi satu baris:

- Jumlah kolom harus 8 dan semua kolom terisi.
- Price, Discount, dan Final Price harus angka.
- Price lebih dari 0, dan Discount antara 0 sampai 100.
- Tanggal berformat `DD-MM-YYYY`, tahun 2000 sampai 2100, dan valid menurut kalender (termasuk tahun kabisat).
- Final Price harus sama dengan `Price x (1 - Discount/100)`, dibulatkan 2 angka desimal.

## Struktur Repositori

```
Mini-Proyek-2D/
├── main.py                          # program utama
├── ecommerce_dataset_updated.csv    # dataset transaksi
└── README.md                        # dokumentasi proyek
```

> Sesuaikan nama `main.py` dengan nama file program yang ada di repo.

## Persyaratan Sistem

- Python 3.8 atau lebih baru.
- Tidak perlu menginstal library tambahan. Program hanya memakai modul bawaan Python (`csv` dan `os`).
- File `ecommerce_dataset_updated.csv` harus berada di folder yang sama dengan file program.

## Cara Menjalankan Program

1. Clone repositori:
   ```bash
   git clone https://github.com/uqiakbar460-alt/Mini-Proyek-2D.git
   ```
2. Masuk ke folder repositori:
   ```bash
   cd Mini-Proyek-2D
   ```
3. Jalankan program:
   ```bash
   python main.py
   ```
   Di beberapa sistem, gunakan `python3 main.py`.

Program harus dijalankan dari dalam folder repositori supaya file CSV ditemukan.

## Panduan Penggunaan

Setelah program berjalan, akan tampil jumlah baris yang dibaca, baris valid, dan baris tidak valid, lalu menu utama:

```
MENU UTAMA
a. Tampilkan data
b. Tambah data
c. Hapus data
d. Ubah data
e. Cari data
f. Ringkasan
g. Keluar
```

Ketik huruf menu, lalu tekan Enter.

- **Tampilkan data (a):** pilih `1` untuk semua data, atau `2` untuk filter metode pembayaran. Saat data lebih dari 20 baris, tekan Enter untuk lanjut atau `q` untuk berhenti.
- **Tambah data (b):** isi User_ID, Product_ID, Category, Price, Discount, Payment_Method, dan Purchase_Date. Final Price tidak perlu diisi karena dihitung otomatis.
- **Hapus data (c):** masukkan nomor data (sesuai kolom `No`), lalu konfirmasi dengan `y`.
- **Ubah data (d):** masukkan nomor data. Tekan Enter pada kolom yang tidak ingin diubah.
- **Cari data (e):** ketik kata kunci. Pencarian tidak membedakan huruf besar dan kecil.
- **Ringkasan (f):** langsung menampilkan semua tabel rekap.

Jika data yang dimasukkan tidak valid, program menampilkan alasannya dan data tidak disimpan.

## Format Data

File CSV memiliki 8 kolom dengan header persis seperti berikut:

| Kolom | Isi | Contoh |
|---|---|---|
| `User_ID` | ID pengguna | `U1001` |
| `Product_ID` | ID produk | `P2005` |
| `Category` | Kategori produk | `Electronics` |
| `Price (Rs.)` | Harga awal, lebih dari 0 | `250.00` |
| `Discount (%)` | Diskon 0 sampai 100 | `20` |
| `Final_Price(Rs.)` | Harga setelah diskon | `200.00` |
| `Payment_Method` | Metode pembayaran | `Cash on Delivery` |
| `Purchase_Date` | Tanggal, format `DD-MM-YYYY` | `15-03-2024` |

Pada Tabel D, metode `Cash on Delivery` dihitung sebagai **Tunai**, dan semua metode lainnya dihitung sebagai **Non-Tunai**.

## Keterbatasan

- Perubahan lewat menu tambah, ubah, dan hapus hanya tersimpan di memori selama program berjalan. File CSV tidak ikut diperbarui, jadi perubahan hilang setelah program ditutup.
- Menu Ringkasan hanya menganalisis maksimal 1000 baris valid pertama (`batas_baris = 1000`).
- Baris yang tidak valid dilewati begitu saja tanpa daftar alasan per barisnya.
- Nama file CSV tertulis tetap di dalam kode, dan program harus dijalankan dari folder repositori.
- Hanya `Cash on Delivery` yang dianggap tunai.
- Tampilan di layar terminal yang cuma pakai teks, tanpa ikon atau gambar.

## Tim Pengembang

| Nama | NIM |
|---|---|
| Muhammad Syauqi Akbar | 2610932047 |
| Sultan Muda Bijaksana | 2610932023 |
| Nabila Safira Silfa | 2610933025 |
| Rahma Putri Zahrany Lesmana | 2610931032 |
