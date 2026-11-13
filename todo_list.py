# todo_list.py
# Aplikasi To-Do List (terminal) - memakai library buatan sendiri: fplib.py
# Jalankan dengan: python todo_list.py

import fplib

BELUM = "Belum selesai"
SELESAI = "Selesai"

# Data awal (disimpan selama program berjalan saja)
DATA_AWAL = [
    {"id": 1, "judul": "Mengerjakan tugas Python", "status": BELUM},
    {"id": 2, "judul": "Membaca materi Functional Programming", "status": SELESAI},
    {"id": 3, "judul": "Membersihkan kamar", "status": BELUM},
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
def format_tugas(tugas):
    tanda = "x" if tugas["status"] == SELESAI else " "
    return f"  {tugas['id']}. [{tanda}] {tugas['judul']}"


def format_daftar(daftar):
    if len(daftar) == 0:
        return "  (tidak ada tugas)"
    return "\n".join(map(format_tugas, daftar))


def format_kelompok(kelompok, jumlah):
    # Tampilkan sesuai urutan status; status yang kosong dilewati
    urutan = fplib.saring([BELUM, SELESAI], lambda s: s in kelompok)
    if len(urutan) == 0:
        return "  (tidak ada tugas)"
    return "\n\n".join(map(
        lambda s: f"[{s}] - {jumlah[s]} tugas\n" + format_daftar(kelompok[s]),
        urutan
    ))


# ---------- Fungsi data (pure function) ----------
def tambah_tugas(data, judul):
    # ambil: semua id yang ada, lalu id baru = id terbesar + 1
    id_baru = max(fplib.ambil(data, "id"), default=0) + 1
    return data + [{"id": id_baru, "judul": judul, "status": BELUM}]


def tandai_selesai(data, id_tugas):
    # map: buat tugas baru dengan status Selesai; tugas lain dibiarkan
    # {**t, ...} menyalin dictionary, jadi dictionary asli tidak berubah
    return list(map(
        lambda t: {**t, "status": SELESAI} if t["id"] == id_tugas else t,
        data
    ))


def ringkasan(data):
    # Ubah status jadi angka: 1 = selesai, 0 = belum
    penanda = list(map(lambda t: 1 if t["status"] == SELESAI else 0, data))
    jumlah_selesai = fplib.jumlahkan(penanda)
    persen = fplib.rata_rata(penanda) * 100          # rata-rata 1/0 = persentase
    return f"Progres: {jumlah_selesai} dari {len(data)} tugas selesai ({persen:.0f}%)"


# ---------- Menu ----------
def menu_tambah(data):
    print("\n--- Tambah Tugas ---")
    judul = minta_input("Judul tugas: ")
    print("  Tugas berhasil ditambahkan.")
    return tambah_tugas(data, judul)


def menu_lihat(data):
    print("\n--- Daftar Tugas ---")
    tampil = fplib.pipe(lambda d: fplib.urutkan(d, "id"), format_daftar)
    print(tampil(data))
    print(ringkasan(data))


def menu_selesai(data):
    print("\n--- Tandai Tugas Selesai ---")
    belum = fplib.saring(data, lambda t: t["status"] == BELUM)
    if len(belum) == 0:
        print("  Semua tugas sudah selesai.")
        return data
    print(format_daftar(belum))
    # Pilihan nomor yang diizinkan = id dari tugas yang belum selesai
    id_boleh = list(map(str, fplib.ambil(belum, "id")))
    pilih = minta_input("Nomor tugas: ", pilihan=id_boleh)
    print("  Tugas ditandai selesai.")
    return tandai_selesai(data, int(pilih))


def menu_kelompok(data):
    print("\n--- Tugas Berdasarkan Status ---")
    kelompok = fplib.kelompokkan(data, "status")
    jumlah = fplib.hitung_frekuensi(data, "status")
    print(format_kelompok(kelompok, jumlah))


def main():
    print("=== TO-DO LIST ===")
    data = DATA_AWAL
    while True:
        print("\nMENU")
        print("1. Tambah tugas")
        print("2. Lihat daftar tugas")
        print("3. Tandai tugas selesai")
        print("4. Kelompokkan berdasarkan status")
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
            data = menu_selesai(data)
        elif pilihan == "4":
            menu_kelompok(data)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
