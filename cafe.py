# ==============================
# APLIKASI DAFTAR MENU & HARGA CAFE
# MODE TERMINAL (PYTHON)
# ==============================

import json
import os

menu = {}
MENU_FILE = "data.json"


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, value):
        node = Node(value)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value


def format_rp(amount):
    try:
        return f"{int(amount):,}".replace(",", ".")
    except Exception:
        return str(amount)


def load_menu():
    """Load menu dictionary from MENU_FILE if available."""
    global menu
    if os.path.exists(MENU_FILE):
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # ensure values are ints
            menu = {k: int(v) for k, v in data.items()}
        except Exception:
            print("⚠️ Gagal membaca file data.json, memulai dengan menu kosong.")
            menu = {}
    else:
        menu = {}


def save_menu():
    """Write current menu dictionary to MENU_FILE."""
    try:
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(menu, f, ensure_ascii=False, indent=2)
    except Exception:
        print("⚠️ Gagal menyimpan menu ke file.")


def parse_price(raw):
    """Convert a price string to integer rupiah value."""
    if not raw:
        return None
    cleaned = raw.replace(".", "").replace(",", "").replace(" ", "")
    if cleaned.isdigit():
        return int(cleaned)
    return None


def tampilkan_menu():
    if not menu:
        print("\nMenu masih kosong.")
        return
    print("\n=== DAFTAR MENU CAFE ===")
    print("-----------------------")
    for no, (nama, harga) in enumerate(menu.items(), 1):
        print(f"{no}. {nama:<12} : Rp {format_rp(harga)}")
    print("-----------------------")


def tambah_menu():
    nama = input("Nama menu   : ").title()
    harga = input("Harga (Rp)  : ")

    parsed = parse_price(harga)
    if parsed is None:
        print("❌ Harga harus berupa angka (boleh gunakan titik atau koma sebagai pemisah ribuan)!")
        return

    menu[nama] = parsed
    save_menu()
    print("✅ Menu berhasil ditambahkan")


def update_menu():
    if not menu:
        print("❌ Menu masih kosong")
        return

    tampilkan_menu()
    pilihan = input("Pilih nomor atau nama menu yang diupdate: ").title()
    
    # Cek apakah input adalah nomor
    nama = None
    if pilihan.isdigit():
        no = int(pilihan)
        menu_list = list(menu.items())
        if 1 <= no <= len(menu_list):
            nama = menu_list[no - 1][0]
    else:
        # Input adalah nama
        if pilihan in menu:
            nama = pilihan
    
    if nama is None:
        print("❌ Menu tidak ditemukan")
        return

    harga = input("Harga baru (Rp): ")
    parsed = parse_price(harga)
    if parsed is None:
        print("❌ Harga harus angka (boleh gunakan titik atau koma sebagai pemisah ribuan)!")
        return

    menu[nama] = parsed
    save_menu()
    print("✅ Harga berhasil diupdate")


def hapus_menu():
    if not menu:
        print("❌ Menu masih kosong")
        return
    
    tampilkan_menu()
    pilihan = input("Pilih nomor atau nama menu yang dihapus: ").title()
    
    # Cek apakah input adalah nomor
    nama = None
    if pilihan.isdigit():
        no = int(pilihan)
        menu_list = list(menu.items())
        if 1 <= no <= len(menu_list):
            nama = menu_list[no - 1][0]
    else:
        # Input adalah nama
        if pilihan in menu:
            nama = pilihan
    
    if nama is None:
        print("❌ Menu tidak ditemukan")
        return
    
    del menu[nama]
    save_menu()
    print("✅ Menu berhasil dihapus")


def transaksi():
    if not menu:
        print("❌ Menu kosong, tidak bisa transaksi")
        return
    cart = Queue()
    total = 0

    while True:
        tampilkan_menu()
        pilihan = input("Pilih nomor atau nama menu (x untuk selesai): ").title()
        
        if pilihan.lower() == "x":
            break
        
        # Cek apakah input adalah nomor
        nama = None
        if pilihan.isdigit():
            no = int(pilihan)
            menu_list = list(menu.items())
            if 1 <= no <= len(menu_list):
                nama = menu_list[no - 1][0]
        else:
            # Input adalah nama
            if pilihan in menu:
                nama = pilihan
        
        if nama is None:
            print("❌ Menu tidak ada")
            continue

        qty = input("Jumlah: ")
        if not qty.isdigit():
            print("❌ Jumlah harus angka")
            continue

        qty = int(qty)
        cart.enqueue((nama, qty))
        print(f"✅ {qty} x {nama} ditambahkan ke keranjang")

    print("\n=== STRUK PEMBELIAN ===")
    print("----------------------")
    while not cart.is_empty():
        nama, qty = cart.dequeue()
        subtotal = menu[nama] * qty
        total += subtotal
        print(f"{nama:<15} x{qty:<3} = Rp {format_rp(subtotal)}")
    print("----------------------")
    print(f"TOTAL BAYAR        = Rp {format_rp(total)}")
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
load_menu()      # <-- INI YANG WAJIB supaya data.json terbaca saat start
menu_utama()