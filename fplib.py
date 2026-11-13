
from functools import reduce
import math

# Memeriksa apakah nilai merupakan angka yang valid.
_adalah_angka = lambda n: (
    isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n)
)


# 1. Menggabungkan beberapa fungsi menjadi satu alur.
def pipe(*fungsi):
    """Menjalankan beberapa fungsi secara berurutan."""
    if not all(map(callable, fungsi)):
        raise TypeError("Semua argumen pipe() harus berupa fungsi.")
    return lambda data: reduce(lambda hasil, f: f(hasil), fungsi, data)


# 2. Mengambil nilai dari field dictionary.
def ambil(data, kunci, default=None):
    """Mengambil satu field dari setiap item."""
    if not isinstance(data, (list, tuple)):
        return []
    return list(map(
        lambda item: item.get(kunci, default) if isinstance(item, dict) else default,
        data
    ))


# 3. Menyaring data berdasarkan kondisi.
def saring(data, kondisi):
    """Mengembalikan item yang memenuhi kondisi."""
    if not isinstance(data, (list, tuple)):
        return []
    if not callable(kondisi):
        raise TypeError("Parameter 'kondisi' harus berupa fungsi.")
    return list(filter(kondisi, data))


# 4. Mencari teks pada satu atau beberapa field.
def cari(data, kata_kunci, kunci):
    """Mencari data tanpa membedakan huruf besar dan kecil."""
    if not isinstance(data, (list, tuple)):
        return []
    kata = str(kata_kunci).strip().lower()
    if kata == "":
        return []
    daftar_kunci = [kunci] if isinstance(kunci, str) else list(kunci)
    return saring(
        data,
        lambda item: isinstance(item, dict) and any(
            map(lambda k: kata in str(item.get(k, "")).lower(), daftar_kunci)
        )
    )


# 5. Mengurutkan data berdasarkan field.
def urutkan(data, kunci, terbalik=False):
    """Mengembalikan data baru yang sudah diurutkan."""
    if not isinstance(data, (list, tuple)):
        return []

    def nilai_urut(item):
        nilai = item.get(kunci) if isinstance(item, dict) else None
        if isinstance(nilai, str):
            nilai = nilai.lower()
        return (nilai is None, 0 if nilai is None else nilai)

    return sorted(data, key=nilai_urut, reverse=terbalik)


# 6. Mengelompokkan data berdasarkan field atau fungsi.
def kelompokkan(data, kunci):
    """Mengelompokkan item ke dalam dictionary."""
    if not isinstance(data, (list, tuple)):
        return {}
    ambil_nilai = kunci if callable(kunci) else (
        lambda item: item.get(kunci) if isinstance(item, dict) else None
    )

    def gabung(hasil, item):
        nilai = ambil_nilai(item)
        nilai = "Lainnya" if nilai is None else nilai
        return {**hasil, nilai: hasil.get(nilai, []) + [item]}

    return reduce(gabung, data, {})


# 7. Menjumlahkan nilai angka.
def jumlahkan(data, kunci=None):
    """Menjumlahkan angka dari list atau field dictionary."""
    if not isinstance(data, (list, tuple)):
        return 0
    nilai = data if kunci is None else ambil(data, kunci, 0)
    angka = saring(nilai, _adalah_angka)
    return reduce(lambda total, n: total + n, angka, 0)


# 8. Menghitung rata-rata.
def rata_rata(data, kunci=None):
    """Menghitung rata-rata nilai angka."""
    if not isinstance(data, (list, tuple)):
        return 0
    nilai = data if kunci is None else ambil(data, kunci, 0)
    angka = saring(nilai, _adalah_angka)
    if len(angka) == 0:
        return 0
    return jumlahkan(angka) / len(angka)


# 9. Memvalidasi input pengguna.
def validasi(nilai, jenis="teks", pilihan=None, minimum=None, maksimum=None):
    """Memeriksa teks, angka, jam, dan pilihan input."""
    if nilai is None or str(nilai).strip() == "":
        return (False, "Input tidak boleh kosong.")
    teks = str(nilai).strip()

    if jenis == "angka":
        try:
            angka = float(teks)
        except ValueError:
            return (False, "Input harus berupa angka.")
        if not math.isfinite(angka):
            return (False, "Input harus berupa angka.")
        if minimum is not None and angka < minimum:
            return (False, f"Angka tidak boleh kurang dari {minimum}.")
        if maksimum is not None and angka > maksimum:
            return (False, f"Angka tidak boleh lebih dari {maksimum}.")

    elif jenis == "jam":
        bagian = teks.split(":")
        format_benar = (
            len(bagian) == 2
            and all(map(lambda b: len(b) == 2 and b.isascii() and b.isdigit(), bagian))
            and 0 <= int(bagian[0]) <= 23
            and 0 <= int(bagian[1]) <= 59
        )
        if not format_benar:
            return (False, "Format jam harus HH:MM, contoh 07:30.")

    elif jenis != "teks":
        return (False, "Jenis validasi tidak dikenal.")

    if pilihan is not None:
        daftar = list(map(lambda p: str(p).lower(), pilihan))
        if teks.lower() not in daftar:
            return (False, "Pilihan harus salah satu dari: " + ", ".join(map(str, pilihan)) + ".")

    return (True, "")


# 10. Menghitung frekuensi kemunculan nilai.
def hitung_frekuensi(data, kunci=None):
    """Menghitung jumlah kemunculan setiap nilai."""
    if not isinstance(data, (list, tuple)):
        return {}
    nilai = data if kunci is None else ambil(data, kunci)
    valid = saring(nilai, lambda x: isinstance(x, (str, int, float, bool)))
    return reduce(lambda hasil, x: {**hasil, x: hasil.get(x, 0) + 1}, valid, {})


# Pengujian fungsi.
if __name__ == "__main__":
    belanja = [
        {"nama": "Apel", "kategori": "Buah", "harga": 12000, "dibeli": False},
        {"nama": "Susu", "kategori": "Minuman", "harga": 18000, "dibeli": True},
        {"nama": "Pisang", "kategori": "Buah", "harga": 9000, "dibeli": False},
        {"nama": "Teh", "kategori": "Minuman", "harga": 7000, "dibeli": False},
    ]
    salinan = [dict(b) for b in belanja]

    print("=== 1. pipe ===")
    alur = pipe(
        lambda d: saring(d, lambda b: not b["dibeli"]),
        lambda d: urutkan(d, "harga"),
        lambda d: ambil(d, "nama"),
    )
    print(alur(belanja))
    assert alur(belanja) == ["Teh", "Pisang", "Apel"]
    assert pipe()(5) == 5

    print("=== 2. ambil ===")
    print(ambil(belanja, "nama"))
    assert ambil(belanja, "nama") == ["Apel", "Susu", "Pisang", "Teh"]
    assert ambil(belanja, "tidak_ada", "-") == ["-", "-", "-", "-"]
    assert ambil(None, "nama") == []

    print("=== 3. saring ===")
    print(ambil(saring(belanja, lambda b: b["kategori"] == "Buah"), "nama"))
    assert len(saring(belanja, lambda b: b["harga"] > 10000)) == 2
    assert saring([], lambda b: True) == []

    print("=== 4. cari ===")
    print(ambil(cari(belanja, "AP", "nama"), "nama"))
    assert ambil(cari(belanja, "ap", "nama"), "nama") == ["Apel"]
    assert len(cari(belanja, "minum", ["nama", "kategori"])) == 2
    assert cari(belanja, "   ", "nama") == []

    print("=== 5. urutkan ===")
    print(ambil(urutkan(belanja, "harga", terbalik=True), "nama"))
    assert ambil(urutkan(belanja, "nama"), "nama") == ["Apel", "Pisang", "Susu", "Teh"]
    assert ambil(urutkan(belanja, "harga", True), "nama")[0] == "Susu"

    print("=== 6. kelompokkan ===")
    hasil = kelompokkan(belanja, "kategori")
    print({k: ambil(v, "nama") for k, v in hasil.items()})
    assert list(hasil.keys()) == ["Buah", "Minuman"]
    murah_mahal = kelompokkan(
        belanja, lambda b: "Murah" if b["harga"] < 10000 else "Mahal"
    )
    assert len(murah_mahal["Murah"]) == 2
    assert kelompokkan([], "kategori") == {}

    print("=== 7. jumlahkan ===")
    print(jumlahkan(belanja, "harga"))
    assert jumlahkan(belanja, "harga") == 46000
    assert jumlahkan([1, 2, "x", True, None]) == 3
    assert jumlahkan([]) == 0

    print("=== 8. rata_rata ===")
    print(rata_rata(belanja, "harga"))
    assert rata_rata(belanja, "harga") == 11500
    assert rata_rata([]) == 0

    print("=== 9. validasi ===")
    for contoh in [
        ("", "teks"), ("Roti", "teks"), ("abc", "angka"),
        ("-5", "angka"), ("25:00", "jam"), ("07:30", "jam")
    ]:
        print(contoh, "->", validasi(
            contoh[0], contoh[1],
            minimum=0 if contoh[1] == "angka" else None
        ))

    assert validasi("", "teks")[0] is False
    assert validasi("Roti")[0] is True
    assert validasi("abc", "angka")[0] is False
    assert validasi("-5", "angka", minimum=0)[0] is False
    assert validasi("07:30", "jam")[0] is True
    assert validasi("7:5x", "jam")[0] is False
    assert validasi("7:05", "jam")[0] is False
    assert validasi("0²:30", "jam")[0] is False
    assert validasi("buah", pilihan=["Buah", "Minuman"])[0] is True
    assert validasi("daging", pilihan=["Buah", "Minuman"])[0] is False

    print("=== 10. hitung_frekuensi ===")
    print(hitung_frekuensi(belanja, "kategori"))
    assert hitung_frekuensi(belanja, "kategori") == {"Buah": 2, "Minuman": 2}
    assert hitung_frekuensi(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert hitung_frekuensi([]) == {}

    assert belanja == salinan
    print("\nSemua pengujian berhasil. Data asli tidak berubah.")
