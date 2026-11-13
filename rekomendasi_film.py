# rekomendasi_film.py
# Aplikasi Rekomendasi Film (terminal) - memakai library buatan sendiri: fplib.py
# Jalankan dengan: python rekomendasi_film.py

import fplib

# Data awal (disimpan selama program berjalan saja)
DATA_AWAL = [
    {"judul": "Laskar Pelangi", "genre": "Drama", "rating": 7.8},
    {"judul": "Pengabdi Setan", "genre": "Horor", "rating": 8.0},
    {"judul": "Dilan 1990", "genre": "Romantis", "rating": 6.5},
    {"judul": "The Raid", "genre": "Aksi", "rating": 7.6},
    {"judul": "Ada Apa dengan Cinta", "genre": "Romantis", "rating": 7.4},
    {"judul": "Gundala", "genre": "Aksi", "rating": 6.1},
]


def minta_input(pertanyaan, jenis="teks", **aturan):
    """Meminta input sampai valid. Pengecekan memakai fplib.validasi()."""
    while True:
        nilai = input(pertanyaan).strip()
        valid, pesan = fplib.validasi(nilai, jenis, **aturan)
        if valid:
            return nilai
        print("  [!] " + pesan)


# ---------- Fungsi tampilan ----------
def format_film(film):
    return f"  - {film['judul']} ({film['genre']}) - rating {film['rating']:.1f}"


def format_daftar(daftar):
    if len(daftar) == 0:
        return "  (tidak ada film)"
    return "\n".join(map(format_film, daftar))


# ---------- Fungsi data (pure function) ----------
def tambah_film(data, judul, genre, rating):
    return data + [{"judul": judul, "genre": genre, "rating": rating}]


def daftar_genre(data):
    # ambil: semua genre, set() membuang duplikat, sorted() mengurutkan
    return sorted(set(fplib.ambil(data, "genre")))


# ---------- Menu ----------
def menu_tambah(data):
    print("\n--- Tambah Film ---")
    judul = minta_input("Judul          : ")
    print("Genre yang sudah ada: " + ", ".join(daftar_genre(data)))
    genre = minta_input("Genre          : ").title()
    rating = minta_input("Rating (0-10)  : ", "angka", minimum=0, maksimum=10)
    print("  Film berhasil ditambahkan.")
    return tambah_film(data, judul, genre, float(rating))


def menu_lihat(data):
    print("\n--- Daftar Film ---")
    print(format_daftar(data))
    print(f"Total: {len(data)} film, rata-rata rating {fplib.rata_rata(data, 'rating'):.2f}")


def menu_cari(data):
    print("\n--- Cari Film ---")
    kata_kunci = minta_input("Kata kunci judul: ")
    hasil = fplib.cari(data, kata_kunci, "judul")
    print(format_daftar(hasil) if hasil else "  Film tidak ditemukan.")


def menu_genre(data):
    print("\n--- Film Berdasarkan Genre ---")
    jumlah = fplib.hitung_frekuensi(data, "genre")
    print("Genre tersedia: " + ", ".join(map(lambda g: f"{g} ({jumlah[g]})", daftar_genre(data))))
    genre = minta_input("Pilih genre: ", pilihan=daftar_genre(data))
    # pipe: saring genre yang dipilih, lalu urutkan dari rating tertinggi
    susun = fplib.pipe(
        lambda d: fplib.saring(d, lambda f: f["genre"].lower() == genre.lower()),
        lambda d: fplib.urutkan(d, "rating", terbalik=True),
    )
    hasil = susun(data)
    print(format_daftar(hasil))
    print(f"Rata-rata rating genre ini: {fplib.rata_rata(hasil, 'rating'):.2f}")


def menu_urutkan(data):
    print("\n--- Urutkan Berdasarkan Rating ---")
    print("1. Rating tertinggi ke terendah")
    print("2. Rating terendah ke tertinggi")
    pilih = minta_input("Pilih urutan: ", pilihan=["1", "2"])
    # terbalik=True berarti dari besar ke kecil
    print(format_daftar(fplib.urutkan(data, "rating", terbalik=(pilih == "1"))))


def main():
    print("=== REKOMENDASI FILM ===")
    data = DATA_AWAL
    while True:
        print("\nMENU")
        print("1. Tambah film")
        print("2. Lihat daftar film")
        print("3. Cari film")
        print("4. Tampilkan film berdasarkan genre")
        print("5. Urutkan berdasarkan rating")
        print("0. Keluar")
        pilihan = minta_input("Pilih menu: ", pilihan=["0", "1", "2", "3", "4", "5"])
        if pilihan == "0":
            print("Terima kasih!")
            break
        elif pilihan == "1":
            data = menu_tambah(data)
        elif pilihan == "2":
            menu_lihat(data)
        elif pilihan == "3":
            menu_cari(data)
        elif pilihan == "4":
            menu_genre(data)
        elif pilihan == "5":
            menu_urutkan(data)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
