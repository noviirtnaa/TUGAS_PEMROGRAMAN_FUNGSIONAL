# jadwal_harian.py
# Aplikasi Jadwal Harian (terminal) - memakai library buatan sendiri: fplib.py
# Jalankan dengan: python jadwal_harian.py

import fplib

# Urutan waktu dalam sehari (dipakai untuk menampilkan kelompok)
URUTAN_WAKTU = ["Pagi", "Siang", "Sore", "Malam"]

# Data awal (sengaja tidak berurutan agar fitur urutkan terlihat)
DATA_AWAL = [
    {"jam": "08:00", "kegiatan": "Kuliah Pemrograman Fungsional", "durasi": 120, "waktu": "Pagi"},
    {"jam": "06:00", "kegiatan": "Bangun dan olahraga", "durasi": 60, "waktu": "Pagi"},
    {"jam": "16:00", "kegiatan": "Mengerjakan tugas", "durasi": 90, "waktu": "Sore"},
    {"jam": "12:30", "kegiatan": "Makan siang", "durasi": 45, "waktu": "Siang"},
    {"jam": "20:00", "kegiatan": "Belajar mandiri", "durasi": 60, "waktu": "Malam"},
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
def format_kegiatan(k):
    return f"  {k['jam']}  {k['kegiatan']} ({k['durasi']} menit)"


def format_daftar(daftar):
    if len(daftar) == 0:
        return "  (tidak ada kegiatan)"
    return "\n".join(map(format_kegiatan, daftar))


# ---------- Fungsi data (pure function) ----------
def tentukan_waktu(jam):
    """Menentukan Pagi/Siang/Sore/Malam dari jam berformat HH:MM."""
    jam_angka = int(jam.split(":")[0])
    if jam_angka < 11:
        return "Pagi"
    if jam_angka < 15:
        return "Siang"
    if jam_angka < 18:
        return "Sore"
    return "Malam"


def tambah_kegiatan(data, jam, kegiatan, durasi):
    baru = {"jam": jam, "kegiatan": kegiatan, "durasi": durasi,
            "waktu": tentukan_waktu(jam)}
    return data + [baru]                      # list baru, list lama tidak diubah


# ---------- Menu ----------
def menu_tambah(data):
    print("\n--- Tambah Kegiatan ---")
    jam = minta_input("Jam (HH:MM)       : ", "jam")
    # ambil: semua jam yang sudah terisi, untuk mencegah jam yang sama
    if jam in fplib.ambil(data, "jam"):
        print(f"  [!] Sudah ada kegiatan pada jam {jam}.")
        return data
    kegiatan = minta_input("Nama kegiatan     : ")
    durasi = minta_input("Durasi (menit)    : ", "angka", minimum=1, maksimum=1440)
    print("  Kegiatan berhasil ditambahkan.")
    return tambah_kegiatan(data, jam, kegiatan, int(float(durasi)))


def menu_lihat(data):
    print("\n--- Jadwal Harian ---")
    print(format_daftar(data))
    print(f"Total durasi     : {fplib.jumlahkan(data, 'durasi')} menit")
    print(f"Rata-rata durasi : {fplib.rata_rata(data, 'durasi'):.0f} menit")


def menu_cari(data):
    print("\n--- Cari Kegiatan ---")
    kata_kunci = minta_input("Kata kunci: ")
    hasil = fplib.cari(data, kata_kunci, "kegiatan")
    print(format_daftar(hasil) if hasil else "  Kegiatan tidak ditemukan.")


def menu_kelompok(data):
    print("\n--- Kegiatan Berdasarkan Waktu ---")
    # pipe: urutkan berdasarkan jam, lalu kelompokkan berdasarkan waktu
    susun = fplib.pipe(
        lambda d: fplib.urutkan(d, "jam"),
        lambda d: fplib.kelompokkan(d, "waktu"),
    )
    kelompok = susun(data)
    jumlah = fplib.hitung_frekuensi(data, "waktu")
    # Tampilkan sesuai urutan Pagi -> Malam, waktu yang kosong dilewati
    ada = fplib.saring(URUTAN_WAKTU, lambda w: w in kelompok)
    if len(ada) == 0:
        print("  (tidak ada kegiatan)")
        return
    print("\n\n".join(map(
        lambda w: f"[{w}] - {jumlah[w]} kegiatan\n" + format_daftar(kelompok[w]),
        ada
    )))


def menu_urutkan(data):
    print("\n--- Urutkan Berdasarkan Jam ---")
    print("1. Dari pagi ke malam")
    print("2. Dari malam ke pagi")
    pilih = minta_input("Pilih urutan: ", pilihan=["1", "2"])
    print(format_daftar(fplib.urutkan(data, "jam", terbalik=(pilih == "2"))))


def main():
    print("=== JADWAL HARIAN ===")
    data = DATA_AWAL
    while True:
        print("\nMENU")
        print("1. Tambah kegiatan")
        print("2. Lihat jadwal")
        print("3. Cari kegiatan")
        print("4. Kelompokkan berdasarkan waktu")
        print("5. Urutkan berdasarkan jam")
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
            menu_kelompok(data)
        elif pilihan == "5":
            menu_urutkan(data)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
