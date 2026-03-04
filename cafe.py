import json
import datetime
import re
import sys
import os
import qrcode
import barcode
import matplotlib.pyplot as plt

from barcode.writer import ImageWriter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch

MENU_FILE = "menu.json"
SALES_FILE = "sales.json"
LOGO_PATH = "logo_cafe.png"

USERS = {
    "admin": "1234",
    "kasir": "1234"
}

# ================= UTILITIES =================

def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n↩ Kembali ke Menu Utama...")
        raise

def format_rupiah(n):
    return f"Rp{int(n):,}".replace(",", ".")

def parse_number(text):
    clean = re.sub(r"[^\d]", "", text)
    if clean == "":
        raise ValueError
    return int(clean)

# ================= MENU MANAGER =================

class MenuManager:
    def __init__(self):
        self.menu = self.load()

    def load(self):
        try:
            with open(MENU_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(MENU_FILE, "w") as f:
            json.dump(self.menu, f, indent=4)

    def show(self):
        print("\n📋 DAFTAR MENU")
        print("="*40)
        for name, price in self.menu.items():
            print(f"{name:<20} {format_rupiah(price):>15}")
        print("="*40)

    def add(self):
        try:
            name = safe_input("Nama menu: ").title()
            price = parse_number(safe_input("Harga: "))
            self.menu[name] = price
            self.save()
            print("✔ Menu ditambahkan")
        except:
            print("❌ Input tidak valid")

    def update(self):
        try:
            name = safe_input("Nama menu: ").title()
            if name not in self.menu:
                print("Menu tidak ada")
                return
            price = parse_number(safe_input("Harga baru: "))
            self.menu[name] = price
            self.save()
            print("✔ Menu diperbarui")
        except:
            print("❌ Input tidak valid")

    def delete(self):
        try:
            name = safe_input("Nama menu: ").title()
            if name in self.menu:
                del self.menu[name]
                self.save()
                print("✔ Menu dihapus")
        except:
            print("❌ Input tidak valid")

# ================= PDF GENERATOR =================

class PDFGenerator:

    def generate_invoice(self, invoice_no, cart, total, discount, tax, grand_total):
        filename = f"Invoice_{invoice_no}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=pagesizes.A4)
        elements = []
        styles = getSampleStyleSheet()

        try:
            elements.append(Image(LOGO_PATH, width=1.5*inch, height=1.5*inch))
        except:
            pass

        elements.append(Paragraph("<b>CAFE ENTERPRISE</b>", styles['Title']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Invoice: {invoice_no}", styles['Normal']))
        elements.append(Paragraph(f"Tanggal: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 15))

        data = [["Menu", "Qty", "Subtotal"]]

        for name, qty in cart.items():
            data.append([name, qty[0], format_rupiah(qty[1])])

        data.append(["", "", ""])
        data.append(["Total", "", format_rupiah(total)])
        data.append(["Diskon", "", f"{discount}%"])
        data.append(["Pajak 10%", "", format_rupiah(tax)])
        data.append(["Grand Total", "", format_rupiah(grand_total)])

        table = Table(data, colWidths=[200, 50, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN',(1,1),(-1,-1),'CENTER')
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Terima kasih ☕", styles['Normal']))

        doc.build(elements)
        os.startfile(filename)

    def generate_receipt(self, invoice_no, cart, grand_total):
        filename = f"Struk_{invoice_no}.pdf"
        width = 226
        height = 800

        doc = SimpleDocTemplate(filename, pagesize=(width, height))
        elements = []
        styles = getSampleStyleSheet()

        try:
            elements.append(Image(LOGO_PATH, width=60, height=60))
        except:
            pass

        elements.append(Paragraph("<para align=center><b>CAFE ENTERPRISE</b></para>", styles["Normal"]))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Invoice: {invoice_no}", styles["Normal"]))
        elements.append(Spacer(1, 10))

        data = []
        for name, qty in cart.items():
            data.append([f"{name} x{qty[0]}"])
            data.append([format_rupiah(qty[1])])
            data.append([""])

        data.append(["--------------------"])
        data.append([f"Grand Total: {format_rupiah(grand_total)}"])
        data.append(["--------------------"])

        elements.append(Table(data, colWidths=[200]))
        elements.append(Spacer(1, 10))

        # QR Code
        qr = qrcode.make(f"Invoice {invoice_no} Total {grand_total}")
        qr_path = f"qr_{invoice_no}.png"
        qr.save(qr_path)
        elements.append(Image(qr_path, width=80, height=80))

        # Barcode
        CODE128 = barcode.get_barcode_class('code128')
        barcode_img = CODE128(invoice_no, writer=ImageWriter())
        barcode_path = f"barcode_{invoice_no}"
        barcode_img.save(barcode_path)
        elements.append(Image(barcode_path + ".png", width=150, height=40))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<para align=center>Terima Kasih ☕</para>", styles["Normal"]))

        doc.build(elements)
        os.startfile(filename)

# ================= TRANSACTION =================

class TransactionManager:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager
        self.sales = self.load()
        self.invoice_counter = len(self.sales) + 1
        self.pdf = PDFGenerator()

    def load(self):
        try:
            with open(SALES_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(SALES_FILE, "w") as f:
            json.dump(self.sales, f, indent=4)

    def kasir_menu(self):
        while True:
            print("\n--- MENU KASIR ---")
            print("1. Transaksi")
            print("2. Laporan Bulanan")
            print("3. Dashboard Grafik")
            print("0. Kembali")

            try:
                choice = safe_input("Pilih: ")

                if choice == "1":
                    self.transact()
                elif choice == "2":
                    self.generate_monthly_report()
                elif choice == "3":
                    self.show_chart()
                elif choice == "0":
                    break
            except:
                break

    def transact(self):
        try:
            cart = {}
            total = 0

            while True:
                self.menu_manager.show()
                name = safe_input("Pilih menu (x selesai): ").title()
                if name.lower() == "x":
                    break
                if name not in self.menu_manager.menu:
                    print("Menu tidak ada")
                    continue

                qty = int(safe_input("Jumlah: "))
                subtotal = self.menu_manager.menu[name] * qty
                cart[name] = (qty, subtotal)
                total += subtotal

            if not cart:
                return

            discount = float(safe_input("Diskon (%): "))
            total_after_discount = total - (total * discount / 100)
            tax = total_after_discount * 0.10
            grand_total = total_after_discount + tax

            pay = parse_number(safe_input("Bayar: "))
            print("Kembalian:", format_rupiah(pay - grand_total))

            invoice_no = f"INV{self.invoice_counter:04d}"
            self.invoice_counter += 1

            self.sales[invoice_no] = {
                "tanggal": str(datetime.datetime.now()),
                "items": cart,
                "total": grand_total
            }

            self.save()

            print("1. Invoice A4")
            print("2. Struk Thermal")
            cetak = safe_input("Pilih cetak: ")

            if cetak == "1":
                self.pdf.generate_invoice(invoice_no, cart, total, discount, tax, grand_total)
            elif cetak == "2":
                self.pdf.generate_receipt(invoice_no, cart, grand_total)

        except:
            print("↩ Kembali...")

    def generate_monthly_report(self):
        filename = "Laporan_Bulanan.pdf"
        doc = SimpleDocTemplate(filename, pagesize=pagesizes.A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("<b>LAPORAN BULANAN</b>", styles['Title']))
        elements.append(Spacer(1, 20))

        total_income = 0
        data = [["Invoice", "Tanggal", "Total"]]

        for inv, sale in self.sales.items():
            total_income += sale["total"]
            data.append([inv, sale["tanggal"][:10], format_rupiah(sale["total"])])

        data.append(["TOTAL", "", format_rupiah(total_income)])

        table = Table(data, colWidths=[100,150,150])
        table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.black)]))
        elements.append(table)

        doc.build(elements)
        os.startfile(filename)

    def show_chart(self):
        item_count = {}

        for s in self.sales.values():
            for item in s["items"]:
                item_count[item] = item_count.get(item, 0) + 1

        if not item_count:
            print("Belum ada data")
            return

        plt.figure()
        plt.bar(item_count.keys(), item_count.values())
        plt.xticks(rotation=45)
        plt.title("Menu Terlaris")
        plt.tight_layout()
        plt.show()

# ================= MAIN =================

class CafeSystem:
    def __init__(self):
        self.menu_manager = MenuManager()
        self.transaction_manager = TransactionManager(self.menu_manager)

    def login(self):
        while True:
            try:
                print("\n=== LOGIN ===")
                user = safe_input("Username: ")
                pw = safe_input("Password: ")
                if user in USERS and USERS[user] == pw:
                    return user
                print("Login salah")
            except:
                sys.exit()

    def run(self):
        while True:
            user = self.login()

            if user == "admin":
                self.admin_menu()
            elif user == "kasir":
                self.transaction_manager.kasir_menu()

    def admin_menu(self):
        while True:
            print("\n--- ADMIN ---")
            print("1. Lihat Menu")
            print("2. Tambah Menu")
            print("3. Update Menu")
            print("4. Hapus Menu")
            print("0. Logout")

            try:
                choice = safe_input("Pilih: ")

                if choice == "1":
                    self.menu_manager.show()
                elif choice == "2":
                    self.menu_manager.add()
                elif choice == "3":
                    self.menu_manager.update()
                elif choice == "4":
                    self.menu_manager.delete()
                elif choice == "0":
                    break
            except:
                break

if __name__ == "__main__":
    CafeSystem().run()