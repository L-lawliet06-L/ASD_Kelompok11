# ==============================
# APLIKASI DAFTAR MENU & HARGA CAFE
# MODE TERMINAL (PYTHON)
# ==============================

menu = {}

def tampilkan_menu():
    if not menu:
        print("\nMenu masih kosong.")
        return
    print("\n=== DAFTAR MENU CAFE ===")
    print("-----------------------")
    for nama, harga in menu.items():
        print(f"{nama:<15} : Rp{harga}")
    print("-----------------------")

def tambah_menu():
    nama = input("Nama menu   : ").title()
    harga = input("Harga (Rp)  : ")

    if not harga.isdigit():
        print("❌ Harga harus berupa angka!")
        return

    menu[nama] = int(harga)
    print("✅ Menu berhasil ditambahkan")

def update_menu():
    nama = input("Nama menu yang diupdate: ").title()
    if nama not in menu:
        print("❌ Menu tidak ditemukan")
        return

    harga = input("Harga baru (Rp): ")
    if not harga.isdigit():
        print("❌ Harga harus angka")
        return

    menu[nama] = int(harga)
    print("✅ Harga berhasil diupdate")

def hapus_menu():
    nama = input("Nama menu yang dihapus: ").title()
    if nama in menu:
        del menu[nama]
        print("✅ Menu berhasil dihapus")
    else:
        print("❌ Menu tidak ditemukan")

def transaksi():
    if not menu:
        print("❌ Menu kosong, tidak bisa transaksi")
        return

    keranjang = {}
    total = 0

    while True:
        tampilkan_menu()
        nama = input("Pilih menu (x untuk selesai): ").title()
        if nama.lower() == "x":
            break
        if nama not in menu:
            print("❌ Menu tidak ada")
            continue

        qty = input("Jumlah: ")
        if not qty.isdigit():
            print("❌ Jumlah harus angka")
            continue

        qty = int(qty)
        keranjang[nama] = keranjang.get(nama, 0) + qty

    print("\n=== STRUK PEMBELIAN ===")
    print("----------------------")
    for nama, qty in keranjang.items():
        subtotal = menu[nama] * qty
        total += subtotal
        print(f"{nama:<15} x{qty:<3} = Rp{subtotal}")
    print("----------------------")
    print(f"TOTAL BAYAR        = Rp{total}")
    print("----------------------")

def menu_utama():
    while True:
        print("""
===== APLIKASI CAFE =====
1. Tampilkan Menu
2. Tambah Menu
3. Update Harga Menu
4. Hapus Menu
5. Transaksi
0. Keluar
""")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            tampilkan_menu()
        elif pilih == "2":
            tambah_menu()
        elif pilih == "3":
            update_menu()
        elif pilih == "4":
            hapus_menu()
        elif pilih == "5":
            transaksi()
        elif pilih == "0":
            print("Terima kasih ☕")
            break
        else:
            print("❌ Pilihan tidak valid")

# ==============================
# PROGRAM DIMULAI
# ==============================
menu_utama()