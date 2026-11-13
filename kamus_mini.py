# kamus_mini.py
# Aplikasi Kamus Mini (terminal) - memakai library buatan sendiri: fplib.py
# Jalankan dengan: python kamus_mini.py

import fplib

# Data awal (disimpan selama program berjalan saja)
DATA_AWAL = [
    {"kata": "Variabel", "arti": "Tempat menyimpan nilai data", "kategori": "Pemrograman"},
    {"kata": "Fungsi", "arti": "Blok kode yang bisa dipanggil berulang kali", "kategori": "Pemrograman"},
    {"kata": "Pure Function", "arti": "Fungsi yang hasilnya hanya bergantung pada input", "kategori": "Functional Programming"},
    {"kata": "Immutability", "arti": "Data tidak diubah, selalu dibuat data baru", "kategori": "Functional Programming"},
    {"kata": "Algoritma", "arti": "Langkah-langkah untuk menyelesaikan masalah", "kategori": "Umum"},
]


def minta_input(pertanyaan, jenis="teks", **aturan):
    """Meminta input sampai valid. Pengecekan memakai fplib.validasi()."""
    while True:
        nilai = input(pertanyaan).strip()
        valid, pesan = fplib.validasi(nilai, jenis, **aturan)
        if valid:
            return nilai
        print("  [!] " + pesan)


# ---------- Fungsi tampilan (pure function: hanya mengubah data jadi teks) ----------
def format_kata(item):
    return f"  - {item['kata']}: {item['arti']} [{item['kategori']}]"


def format_daftar(daftar):
    if len(daftar) == 0:
        return "  (tidak ada data)"
    return "\n".join(map(format_kata, daftar))          # map: ubah tiap item jadi teks


def format_kelompok(kelompok, jumlah):
    if len(kelompok) == 0:
        return "  (tidak ada data)"
    bagian = map(
        lambda p: f"[{p[0]}] - {jumlah[p[0]]} kata\n" + format_daftar(p[1]),
        kelompok.items()
    )
    return "\n\n".join(bagian)


# ---------- Fungsi data (pure function: tidak mengubah data asli) ----------
def kata_sudah_ada(data, kata):
    # saring: ambil kata yang sama (huruf besar/kecil diabaikan)
    sama = fplib.saring(data, lambda item: item["kata"].lower() == kata.lower())
    return len(sama) > 0


def tambah_kata(data, kata, arti, kategori):
    # Membuat list BARU (data + [...]), list lama tidak diubah
    return data + [{"kata": kata, "arti": arti, "kategori": kategori}]


# ---------- Menu ----------
def menu_tambah(data):
    print("\n--- Tambah Kata ---")
    kata = minta_input("Kata     : ")
    if kata_sudah_ada(data, kata):
        print(f"  [!] Kata '{kata}' sudah ada di kamus.")
        return data
    arti = minta_input("Arti     : ")
    # ambil: ambil semua kategori yang sudah ada, set() membuang duplikat
    kategori_ada = sorted(set(fplib.ambil(data, "kategori")))
    print("Kategori yang sudah ada: " + ", ".join(kategori_ada))
    kategori = minta_input("Kategori : ").title()
    print("  Kata berhasil ditambahkan.")
    return tambah_kata(data, kata, arti, kategori)


def menu_lihat(data):
    print("\n--- Daftar Kata (urut A-Z) ---")
    # pipe: urutkan dulu, lalu ubah menjadi teks
    tampil = fplib.pipe(lambda d: fplib.urutkan(d, "kata"), format_daftar)
    print(tampil(data))
    print(f"Total: {len(data)} kata")


def menu_cari(data):
    print("\n--- Cari Kata ---")
    kata_kunci = minta_input("Kata kunci: ")
    hasil = fplib.cari(data, kata_kunci, ["kata", "arti"])
    print(format_daftar(hasil) if hasil else "  Kata tidak ditemukan.")


def menu_kategori(data):
    print("\n--- Kata Berdasarkan Kategori ---")
    # pipe: urutkan kata A-Z, lalu kelompokkan berdasarkan kategori
    susun = fplib.pipe(
        lambda d: fplib.urutkan(d, "kata"),
        lambda d: fplib.kelompokkan(d, "kategori"),
    )
    jumlah = fplib.hitung_frekuensi(data, "kategori")    # jumlah kata per kategori
    print(format_kelompok(susun(data), jumlah))


def main():
    print("=== KAMUS MINI ===")
    data = DATA_AWAL
    while True:
        print("\nMENU")
        print("1. Tambah kata")
        print("2. Lihat daftar kata")
        print("3. Cari kata")
        print("4. Tampilkan berdasarkan kategori")
        print("0. Keluar")
        pilihan = minta_input("Pilih menu: ", pilihan=["0", "1", "2", "3", "4"])
        if pilihan == "0":
            print("Terima kasih!")
            break
        elif pilihan == "1":
            data = menu_tambah(data)        # data diganti dengan list baru
        elif pilihan == "2":
            menu_lihat(data)
        elif pilihan == "3":
            menu_cari(data)
        elif pilihan == "4":
            menu_kategori(data)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")