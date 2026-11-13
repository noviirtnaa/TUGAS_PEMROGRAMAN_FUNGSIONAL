# catatan_belanja.py
# Aplikasi Catatan Belanja (terminal) - memakai library buatan sendiri: fplib.py
# Jalankan dengan: python catatan_belanja.py

import fplib

BELUM = "Belum dibeli"
SUDAH = "Sudah dibeli"

# Data awal (disimpan selama program berjalan saja)
DATA_AWAL = [
    {"id": 1, "nama": "Beras 5 kg", "kategori": "Makanan", "harga": 65000, "status": BELUM},
    {"id": 2, "nama": "Telur 1 kg", "kategori": "Makanan", "harga": 28000, "status": SUDAH},
    {"id": 3, "nama": "Sabun mandi", "kategori": "Kebersihan", "harga": 5000, "status": BELUM},
    {"id": 4, "nama": "Sampo", "kategori": "Kebersihan", "harga": 22000, "status": BELUM},
    {"id": 5, "nama": "Susu UHT", "kategori": "Minuman", "harga": 18000, "status": BELUM},
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
def rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


def format_barang(barang):
    tanda = "x" if barang["status"] == SUDAH else " "
    return f"  {barang['id']}. [{tanda}] {barang['nama']} - {rupiah(barang['harga'])}"


def format_daftar(daftar):
    if len(daftar) == 0:
        return "  (tidak ada barang)"
    return "\n".join(map(format_barang, daftar))


def format_kelompok(kelompok, jumlah):
    if len(kelompok) == 0:
        return "  (tidak ada barang)"
    return "\n\n".join(map(
        lambda p: (f"[{p[0]}] - {jumlah[p[0]]} barang, "
                   f"subtotal {rupiah(fplib.jumlahkan(p[1], 'harga'))}\n")
        + format_daftar(p[1]),
        kelompok.items()
    ))


# ---------- Fungsi data (pure function) ----------
def tambah_barang(data, nama, kategori, harga):
    id_baru = max(fplib.ambil(data, "id"), default=0) + 1
    barang = {"id": id_baru, "nama": nama, "kategori": kategori,
              "harga": harga, "status": BELUM}
    return data + [barang]                    # list baru, list lama tidak diubah


def tandai_dibeli(data, id_barang):
    # map: buat barang baru dengan status Sudah dibeli ({**b} = salinan dictionary)
    return list(map(
        lambda b: {**b, "status": SUDAH} if b["id"] == id_barang else b,
        data
    ))


# ---------- Menu ----------
def menu_tambah(data):
    print("\n--- Tambah Barang ---")
    nama = minta_input("Nama barang      : ")
    kategori_ada = sorted(set(fplib.ambil(data, "kategori")))
    print("Kategori yang sudah ada: " + ", ".join(kategori_ada))
    kategori = minta_input("Kategori         : ").title()
    harga = minta_input("Harga (Rp)       : ", "angka", minimum=0)
    print("  Barang berhasil ditambahkan.")
    return tambah_barang(data, nama, kategori, int(float(harga)))


def menu_lihat(data):
    print("\n--- Daftar Belanja (urut A-Z) ---")
    tampil = fplib.pipe(lambda d: fplib.urutkan(d, "nama"), format_daftar)
    print(tampil(data))
    belum = fplib.saring(data, lambda b: b["status"] == BELUM)
    print(f"Total semua barang    : {rupiah(fplib.jumlahkan(data, 'harga'))}")
    print(f"Yang belum dibeli     : {rupiah(fplib.jumlahkan(belum, 'harga'))}")
    print(f"Rata-rata harga barang: {rupiah(fplib.rata_rata(data, 'harga'))}")


def menu_dibeli(data):
    print("\n--- Tandai Barang Sudah Dibeli ---")
    belum = fplib.saring(data, lambda b: b["status"] == BELUM)
    if len(belum) == 0:
        print("  Semua barang sudah dibeli.")
        return data
    print(format_daftar(belum))
    id_boleh = list(map(str, fplib.ambil(belum, "id")))
    pilih = minta_input("Nomor barang: ", pilihan=id_boleh)
    print("  Barang ditandai sudah dibeli.")
    return tandai_dibeli(data, int(pilih))


def menu_kategori(data):
    print("\n--- Barang Berdasarkan Kategori ---")
    kelompok = fplib.kelompokkan(data, "kategori")
    jumlah = fplib.hitung_frekuensi(data, "kategori")
    print(format_kelompok(kelompok, jumlah))


def main():
    print("=== CATATAN BELANJA ===")
    data = DATA_AWAL
    while True:
        print("\nMENU")
        print("1. Tambah barang")
        print("2. Lihat daftar belanja")
        print("3. Tandai barang sudah dibeli")
        print("4. Kelompokkan berdasarkan kategori")
        print("0. Keluar")
        pilihan = minta_input("Pilih menu: ", pilihan=["0", "1", "2", "3", "4"])
        if pilihan == "0":
            print("Terima kasih!")
            break
        elif pilihan == "1":
            data = menu_tambah(data)
        elif pilihan == "2":
            menu_lihat(data)
        elif pilihan == "3":
            data = menu_dibeli(data)
        elif pilihan == "4":
            menu_kategori(data)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
