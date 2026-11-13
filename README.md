# Tugas Pemrograman Fungsional - Python

Lima aplikasi terminal sederhana yang memakai **satu library buatan sendiri**, `fplib.py`.
Data hanya disimpan selama program berjalan (tanpa database, API, GUI, atau framework).

## Struktur Folder

```
TUGAS_PEMROGRAMAN_FUNGSIONAL/
├── fplib.py              # library: 10 fungsi Functional Programming
├── kamus_mini.py
├── todo_list.py
├── catatan_belanja.py
├── rekomendasi_film.py
├── jadwal_harian.py
└── README.md
```

## Cara Menjalankan

Butuh Python 3.8+ (tanpa instalasi library tambahan). Buka terminal di folder ini, lalu:

```
python kamus_mini.py
python todo_list.py
python catatan_belanja.py
python rekomendasi_film.py
python jadwal_harian.py
```

Pengujian library `fplib.py` (data contoh + assert):

```
python fplib.py
```

Jika `python` tidak dikenali, gunakan `python3` (Mac/Linux) atau `py` (Windows).
Semua aplikasi harus dijalankan dari folder yang sama dengan `fplib.py`.

## Library fplib.py

| # | Fungsi | Kegunaan | Konsep Functional Programming |
|---|---|---|---|
| 1 | `pipe()` | Menyambung beberapa fungsi menjadi satu alur | Higher-order function, `reduce`, `lambda` |
| 2 | `ambil()` | Mengambil satu field dari setiap item | `map`, `lambda` |
| 3 | `saring()` | Memilih item yang memenuhi kondisi | `filter`, higher-order function |
| 4 | `cari()` | Mencari teks pada satu/beberapa field | Komposisi fungsi, `any` + `map` |
| 5 | `urutkan()` | Mengurutkan data (list baru) | Immutability (`sorted`) |
| 6 | `kelompokkan()` | Mengelompokkan item per field/fungsi | `reduce`, immutability |
| 7 | `jumlahkan()` | Menjumlahkan angka / field | `reduce`, komposisi |
| 8 | `rata_rata()` | Menghitung rata-rata (aman untuk data kosong) | Pure function, komposisi |
| 9 | `validasi()` | Memeriksa input pengguna -> `(valid, pesan)` | Pure function |
| 10 | `hitung_frekuensi()` | Menghitung kemunculan tiap nilai | `reduce`, immutability |

Semua fungsi tidak mengubah data asli dan mengembalikan nilai kosong (`[]`, `{}`, atau `0`) jika data tidak valid.

## Ringkasan Penggunaan Library per Aplikasi

- **Kamus Mini** (`kamus_mini.py`): `pipe` (urut lalu tampil / urut lalu kelompok), `ambil` (daftar kategori), `saring` (cek kata duplikat), `cari` (cari kata/arti), `urutkan` (A-Z), `kelompokkan` (per kategori), `validasi` (semua input), `hitung_frekuensi` (jumlah kata per kategori)
- **To-Do List** (`todo_list.py`): `pipe` (urut id lalu tampil), `ambil` (id baru & id yang boleh dipilih), `saring` (tugas belum selesai), `urutkan` (urut id), `kelompokkan` (per status), `jumlahkan` (jumlah tugas selesai), `rata_rata` (persentase progres), `validasi`, `hitung_frekuensi` (jumlah per status)
- **Catatan Belanja** (`catatan_belanja.py`): `pipe` (urut nama lalu tampil), `ambil` (id baru, id pilihan, kategori), `saring` (barang belum dibeli), `urutkan` (A-Z), `kelompokkan` (per kategori), `jumlahkan` (total & subtotal harga), `rata_rata` (rata-rata harga), `validasi`, `hitung_frekuensi` (jumlah per kategori)
- **Rekomendasi Film** (`rekomendasi_film.py`): `pipe` (saring genre lalu urut rating), `ambil` (daftar genre), `saring` (film per genre), `cari` (cari judul), `urutkan` (urut rating), `rata_rata` (rata-rata rating), `validasi`, `hitung_frekuensi` (jumlah film per genre)
- **Jadwal Harian** (`jadwal_harian.py`): `pipe` (urut jam lalu kelompok waktu), `ambil` (cek jam bentrok), `saring` (waktu yang ada), `cari` (cari kegiatan), `urutkan` (urut jam), `kelompokkan` (per waktu), `jumlahkan` (total durasi), `rata_rata` (rata-rata durasi), `validasi`, `hitung_frekuensi` (jumlah per waktu)

## Matriks Fungsi x Aplikasi (jumlah pemanggilan `fplib.<fungsi>()`)

| Fungsi | Kamus Mini | To-Do List | Catatan Belanja | Rekomendasi Film | Jadwal Harian | Jumlah Aplikasi | Total Pemanggilan |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `pipe()` | 2 | 1 | 1 | 1 | 1 | 5 | 6 |
| `ambil()` | 1 | 2 | 3 | 1 | 1 | 5 | 8 |
| `saring()` | 1 | 2 | 2 | 1 | 1 | 5 | 7 |
| `cari()` | 1 | - | - | 1 | 1 | 3 | 3 |
| `urutkan()` | 2 | 1 | 1 | 2 | 2 | 5 | 8 |
| `kelompokkan()` | 1 | 1 | 1 | - | 1 | 4 | 4 |
| `jumlahkan()` | - | 1 | 3 | - | 1 | 3 | 5 |
| `rata_rata()` | - | 1 | 1 | 2 | 1 | 4 | 5 |
| `validasi()` | 1 | 1 | 1 | 1 | 1 | 5 | 5 |
| `hitung_frekuensi()` | 1 | 1 | 1 | 1 | 1 | 5 | 5 |

Syarat tugas: setiap fungsi dipakai minimal pada 3 dari 5 aplikasi. **Terpenuhi** (kolom "Jumlah Aplikasi" minimal 3).

## Matriks Fungsi x Nama File

| Fungsi | File aplikasi yang memanggil |
|---|---|
| `pipe()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `ambil()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `saring()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `cari()` | `kamus_mini.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `urutkan()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `kelompokkan()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `jadwal_harian.py` |
| `jumlahkan()` | `todo_list.py`, `catatan_belanja.py`, `jadwal_harian.py` |
| `rata_rata()` | `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `validasi()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |
| `hitung_frekuensi()` | `kamus_mini.py`, `todo_list.py`, `catatan_belanja.py`, `rekomendasi_film.py`, `jadwal_harian.py` |

## Hasil Pengujian

- `python fplib.py`: seluruh pengujian (assert) lolos, data asli tidak berubah.
- Kelima aplikasi berhasil diimpor tanpa kesalahan import.
- Pemindaian kode (AST): setiap fungsi benar-benar **dipanggil** (bukan sekadar diimpor) pada minimal 3 aplikasi.
- Semua menu setiap aplikasi dijalankan dengan input simulasi: input kosong, menu tidak valid, angka tidak valid, jam salah format, rating di luar 0-10, data duplikat, dan pilihan nomor yang tidak ada. Semua ditangani tanpa error.
