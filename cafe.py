# ==============================
# APLIKASI DAFTAR MENU & HARGA CAFE
# MODE TERMINAL (PYTHON)
# ==============================

menu = {}


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

def tampilkan_menu():
    if not menu:
        print("\nMenu masih kosong.")
        return
    print("\n=== DAFTAR MENU CAFE ===")
    print("-----------------------")
    for nama, harga in menu.items():
        print(f"{nama:<15} : Rp {format_rp(harga)}")
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
    if not menu:
        print("❌ Menu masih kosong")
        return

    tampilkan_menu()
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
    cart = Queue()
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
        cart.enqueue((nama, qty))

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
menu_utama()