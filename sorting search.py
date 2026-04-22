# Daftar menu & harga cafe
menu_cafe = [
    {"nama": "Espresso", "harga": 15000},
    {"nama": "Latte", "harga": 25000},
    {"nama": "Cappuccino", "harga": 22000},
    {"nama": "Americano", "harga": 18000},
    {"nama": "Mocha", "harga": 27000},
    {"nama": "Teh Hijau", "harga": 12000},
    {"nama": "Smoothie", "harga": 30000}
]

# Fungsi menampilkan menu
def tampilkan_menu(menu):
    print("\n=== Daftar Menu & Harga Cafe ===")
    for item in menu:
        print(f"{item['nama']:15} Rp {item['harga']}")

# Fungsi pencarian menu berdasarkan nama
def cari_menu(menu, keyword):
    hasil = [item for item in menu if keyword.lower() in item['nama'].lower()]
    return hasil

# Fungsi sorting
def sorting_menu(menu, berdasarkan="harga"):
    if berdasarkan == "harga":
        return sorted(menu, key=lambda x: x['harga'])
    elif berdasarkan == "nama":
        return sorted(menu, key=lambda x: x['nama'])
    else:
        return menu

# Program utama dengan loop
while True:
    print("\n=== Cafe System ===")
    print("1. Tampilkan semua menu")
    print("2. Cari menu")
    print("3. Sorting menu")
    print("4. Keluar")

    pilihan = input("Pilih opsi (1/2/3/4): ")

    if pilihan == "1":
        tampilkan_menu(menu_cafe)

    elif pilihan == "2":
        keyword = input("Masukkan nama menu yang dicari: ")
        hasil = cari_menu(menu_cafe, keyword)
        if hasil:
            tampilkan_menu(hasil)
        else:
            print("Menu tidak ditemukan.")

    elif pilihan == "3":
        kriteria = input("Urutkan berdasarkan (harga/nama): ")
        hasil_sorting = sorting_menu(menu_cafe, berdasarkan=kriteria)
        tampilkan_menu(hasil_sorting)

    elif pilihan == "4":
        print("Terima kasih sudah menggunakan sistem cafe. Sampai jumpa!")
        break

    else:
        print("Pilihan tidak valid. Silakan coba lagi.")