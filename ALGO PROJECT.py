import csv
import os
from datetime import datetime

# ==========================================
# KELANA - KELOLA LAYANAN ALAT NANJAK & ALAM
# ==========================================

FILE_ALAT = "data_alat.csv"
FILE_PAKET = "data_paket.csv"
FILE_TRANSAKSI = "data_transaksi.csv"


# ==========================================
# 1. MEMBUAT FILE CSV OTOMATIS
# ==========================================

def siapkan_file():

    daftar_file = {
        FILE_ALAT: ["id", "nama", "kategori", "harga", "stok"],
        FILE_PAKET: ["id", "nama", "isi", "harga", "stok"],
        FILE_TRANSAKSI: [
            "id", "tanggal", "penyewa",
            "detail", "durasi", "total"
        ]
    }

    for nama_file, kolom in daftar_file.items():

        if not os.path.exists(nama_file):
            with open(nama_file, "w", newline="",
                      encoding="utf-8") as file:

                writer = csv.writer(file)
                writer.writerow(kolom)


# ==========================================
# 2. FUNGSI MEMBACA DAN MENYIMPAN CSV
# ==========================================

def baca_data(nama_file):

    with open(nama_file, "r", newline="",
              encoding="utf-8") as file:

        reader = csv.DictReader(file)
        return list(reader)


def simpan_data(nama_file, data):

    with open(nama_file, "w", newline="",
              encoding="utf-8") as file:

        if not data:
            return

        writer = csv.DictWriter(
            file, fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)


def tambah_data(nama_file, data):

    with open(nama_file, "a", newline="",
              encoding="utf-8") as file:

        writer = csv.DictWriter(
            file, fieldnames=data.keys()
        )

        writer.writerow(data)


def id_baru(nama_file):

    data = baca_data(nama_file)

    if len(data) == 0:
        return "1"

    nomor = max(int(item["id"]) for item in data) + 1
    return str(nomor)


def input_angka(pesan, minimal=0):

    while True:
        try:
            angka = int(input(pesan))

            if angka < minimal:
                print("Angka tidak boleh kurang dari", minimal)
            else:
                return angka

        except ValueError:
            print("Masukkan angka yang benar!")


def format_rupiah(angka):
    return "Rp" + format(angka, ",").replace(",", ".")


# ==========================================
# 3. MENAMPILKAN DATA ALAT
# ==========================================

def tampilkan_alat():

    data = baca_data(FILE_ALAT)

    print("\n========== DAFTAR ALAT CAMPING ==========")

    if not data:
        print("Belum ada alat tersedia.")
        return

    for alat in data:
        print("----------------------------------------")
        print("ID       :", alat["id"])
        print("Nama     :", alat["nama"])
        print("Kategori :", alat["kategori"])
        print("Harga    :", format_rupiah(int(alat["harga"])))
        print("Stok     :", alat["stok"])


# ==========================================
# 4. MENAMBAHKAN ALAT (ADMIN)
# ==========================================

def admin_tambah_alat():

    print("\n========== TAMBAH ALAT ==========")

    nama = input("Nama alat       : ")
    kategori = input("Kategori        : ")
    harga = input_angka("Harga per hari  : ", 1)
    stok = input_angka("Jumlah stok     : ", 1)

    data = {
        "id": id_baru(FILE_ALAT),
        "nama": nama,
        "kategori": kategori,
        "harga": str(harga),
        "stok": str(stok)
    }

    tambah_data(FILE_ALAT, data)

    print("\nAlat berhasil ditambahkan!")


# ==========================================
# 5. MENAMBAHKAN PAKET BUNDLING (ADMIN)
# ==========================================

def admin_tambah_paket():

    print("\n========== TAMBAH PAKET BUNDLING ==========")

    nama = input("Nama paket       : ")
    isi = input("Isi paket        : ")
    harga = input_angka("Harga per hari   : ", 1)
    stok = input_angka("Jumlah paket     : ", 1)

    data = {
        "id": id_baru(FILE_PAKET),
        "nama": nama,
        "isi": isi,
        "harga": str(harga),
        "stok": str(stok)
    }

    tambah_data(FILE_PAKET, data)

    print("\nPaket berhasil ditambahkan!")


# ==========================================
# 6. MENAMPILKAN PAKET BUNDLING
# ==========================================

def tampilkan_paket():

    data = baca_data(FILE_PAKET)

    print("\n========== PAKET BUNDLING ==========")

    if not data:
        print("Belum ada paket tersedia.")
        return

    for paket in data:
        print("----------------------------------------")
        print("ID       :", paket["id"])
        print("Nama     :", paket["nama"])
        print("Isi      :", paket["isi"])
        print("Harga    :", format_rupiah(int(paket["harga"])))
        print("Stok     :", paket["stok"])


# ==========================================
# 7. MENCARI ALAT
# ==========================================

def cari_alat():

    kata = input("\nMasukkan nama alat yang dicari: ").lower()

    data = baca_data(FILE_ALAT)

    hasil = [
        alat for alat in data
        if kata in alat["nama"].lower()
        or kata in alat["kategori"].lower()
    ]

    print("\n========== HASIL PENCARIAN ==========")

    if not hasil:
        print("Alat tidak ditemukan.")
    else:
        for alat in hasil:
            print(
                alat["id"], "-", alat["nama"],
                "-", format_rupiah(int(alat["harga"])),
                "- Stok:", alat["stok"]
            )


# ==========================================
# 8. KERANJANG PENYEWAAN (USER)
# ==========================================

def user_penyewaan(nama_penyewa):

    keranjang = []

    while True:

        print("\n========== MENU PENYEWAAN ==========")
        print("1. Tambah alat")
        print("2. Tambah paket bundling")
        print("3. Lihat keranjang")
        print("4. Checkout")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":

            tampilkan_alat()

            id_alat = input("\nMasukkan ID alat: ")
            data = baca_data(FILE_ALAT)

            barang = next(
                (x for x in data if x["id"] == id_alat),
                None
            )

            if barang is None:
                print("Alat tidak ditemukan!")
                continue

            jenis = "alat"
            harga = int(barang["harga"])
            stok = int(barang["stok"])
            nama = barang["nama"]
            id_barang = barang["id"]

        elif pilihan == "2":

            tampilkan_paket()

            id_paket = input("\nMasukkan ID paket: ")
            data = baca_data(FILE_PAKET)

            barang = next(
                (x for x in data if x["id"] == id_paket),
                None
            )

            if barang is None:
                print("Paket tidak ditemukan!")
                continue

            jenis = "paket"
            harga = int(barang["harga"])
            stok = int(barang["stok"])
            nama = barang["nama"]
            id_barang = barang["id"]

        elif pilihan == "3":

            print("\n========== KERANJANG ==========")

            if not keranjang:
                print("Keranjang masih kosong.")
            else:
                for item in keranjang:
                    print(
                        item["nama"],
                        "| Jumlah:", item["jumlah"],
                        "| Harga/hari:", format_rupiah(item["harga"])
                    )

            continue

        elif pilihan == "4":

            if not keranjang:
                print("Keranjang masih kosong!")
                continue

            checkout(nama_penyewa, keranjang)
            break

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")
            continue

        jumlah = input_angka("Jumlah yang disewa: ", 1)

        # Menghitung jumlah barang yang sudah ada
        jumlah_lama = sum(
            item["jumlah"] for item in keranjang
            if item["jenis"] == jenis
            and item["id"] == id_barang
        )

        if jumlah + jumlah_lama > stok:
            print("Stok tidak mencukupi!")
            continue

        keranjang.append({
            "jenis": jenis,
            "id": id_barang,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah
        })

        print(nama, "berhasil ditambahkan ke keranjang!")


# ==========================================
# 9. CHECKOUT DAN TRANSAKSI
# ==========================================

def checkout(nama_penyewa, keranjang):

    durasi = input_angka(
        "\nBerapa hari penyewaan? ", 1
    )

    # Validasi ulang seluruh stok
    for item in keranjang:

        file = FILE_ALAT if item["jenis"] == "alat" else FILE_PAKET
        data = baca_data(file)

        barang = next(
            (x for x in data if x["id"] == item["id"]),
            None
        )

        if barang is None or int(barang["stok"]) < item["jumlah"]:
            print("Transaksi dibatalkan. Stok tidak mencukupi!")
            return

    total = 0
    detail = []

    # Mengurangi stok dan menghitung total
    for item in keranjang:

        file = FILE_ALAT if item["jenis"] == "alat" else FILE_PAKET
        data = baca_data(file)

        for barang in data:
            if barang["id"] == item["id"]:
                barang["stok"] = str(
                    int(barang["stok"]) - item["jumlah"]
                )

        simpan_data(file, data)

        subtotal = item["harga"] * item["jumlah"] * durasi
        total += subtotal

        detail.append(
            f'{item["nama"]} x {item["jumlah"]}'
        )

    print("\n========== RINCIAN PEMBAYARAN ==========")

    for item in keranjang:
        subtotal = item["harga"] * item["jumlah"] * durasi
        print(item["nama"], ":", format_rupiah(subtotal))

    print("Durasi :", durasi, "hari")
    print("TOTAL  :", format_rupiah(total))

    konfirmasi = input("\nKonfirmasi penyewaan? (y/n): ").lower()

    if konfirmasi != "y":

        # Mengembalikan stok jika checkout dibatalkan
        for item in keranjang:
            file = FILE_ALAT if item["jenis"] == "alat" else FILE_PAKET
            data = baca_data(file)

            for barang in data:
                if barang["id"] == item["id"]:
                    barang["stok"] = str(
                        int(barang["stok"]) + item["jumlah"]
                    )

            simpan_data(file, data)

        print("Penyewaan dibatalkan.")
        return

    transaksi = {
        "id": id_baru(FILE_TRANSAKSI),
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "penyewa": nama_penyewa,
        "detail": "; ".join(detail),
        "durasi": str(durasi),
        "total": str(total)
    }

    tambah_data(FILE_TRANSAKSI, transaksi)

    print("\nPenyewaan berhasil!")
    print("Terima kasih telah menggunakan KELANA.")


# ==========================================
# 10. RIWAYAT TRANSAKSI
# ==========================================

def riwayat_transaksi(nama=None):

    data = baca_data(FILE_TRANSAKSI)

    if nama is not None:
        data = [
            x for x in data
            if x["penyewa"].lower() == nama.lower()
        ]

    print("\n========== RIWAYAT PENYEWAAN ==========")

    if not data:
        print("Belum ada riwayat transaksi.")
        return

    for transaksi in data:

        print("----------------------------------------")
        print("ID Transaksi :", transaksi["id"])
        print("Tanggal      :", transaksi["tanggal"])
        print("Penyewa      :", transaksi["penyewa"])
        print("Barang       :", transaksi["detail"])
        print("Durasi       :", transaksi["durasi"], "hari")
        print("Total        :", format_rupiah(int(transaksi["total"])))


# ==========================================
# 11. REKAP TOTAL TRANSAKSI (ADMIN)
# ==========================================

def rekap_transaksi():

    data = baca_data(FILE_TRANSAKSI)

    jumlah_transaksi = len(data)

    total_pendapatan = sum(
        int(x["total"]) for x in data
    )

    print("\n========== REKAP KELANA ==========")
    print("Jumlah transaksi :", jumlah_transaksi)
    print("Total pendapatan :", format_rupiah(total_pendapatan))

    riwayat_transaksi()


# ==========================================
# 12. MENU ADMIN
# ==========================================

def menu_admin():

    while True:

        print("\n================================")
        print("          MENU ADMIN")
        print("================================")
        print("1. Tambah alat")
        print("2. Tambah paket bundling")
        print("3. Tampilkan alat")
        print("4. Tampilkan paket")
        print("5. Riwayat dan rekap transaksi")
        print("6. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            admin_tambah_alat()

        elif pilihan == "2":
            admin_tambah_paket()

        elif pilihan == "3":
            tampilkan_alat()

        elif pilihan == "4":
            tampilkan_paket()

        elif pilihan == "5":
            rekap_transaksi()

        elif pilihan == "6":
            break

        else:
            print("Pilihan tidak valid!")


# ==========================================
# 13. MENU USER
# ==========================================

def menu_user():

    print("\n========== REGISTRASI PENYEWA ==========")

    nama = input("Masukkan nama penyewa: ").strip()

    if nama == "":
        print("Nama tidak boleh kosong!")
        return

    while True:

        print("\n========== MENU USER ==========")
        print("1. Tampilkan alat")
        print("2. Cari alat")
        print("3. Tampilkan paket bundling")
        print("4. Mulai penyewaan")
        print("5. Riwayat transaksi")
        print("6. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_alat()

        elif pilihan == "2":
            cari_alat()

        elif pilihan == "3":
            tampilkan_paket()

        elif pilihan == "4":
            user_penyewaan(nama)

        elif pilihan == "5":
            riwayat_transaksi(nama)

        elif pilihan == "6":
            break

        else:
            print("Pilihan tidak valid!")


# ==========================================
# 14. PROGRAM UTAMA
# ==========================================

def main():

    siapkan_file()

    while True:

        print("\n")
        print("========================================")
        print("       KELANA - CAMPING & HIKING")
        print(" Kelola Layanan Alat Nanjak & Alam")
        print("========================================")
        print("1. Login Admin")
        print("2. Masuk sebagai User")
        print("3. Keluar")

        pilihan = input("\nPilih menu (1/2/3): ")

        if pilihan == "1":
            menu_admin()

        elif pilihan == "2":
            menu_user()

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan KELANA!")
            break

        else:
            print("Pilihan tidak valid!")


# Menjalankan program
if __name__ == "__main__":
    main()