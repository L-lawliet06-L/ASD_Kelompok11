# ASD_Kelompok11
# ☕ Cafe Enterprise System

Sistem Manajemen Café berbasis Python dengan arsitektur OOP profesional.

---

## 🚀 Fitur Utama

### 🔐 Authentication
- Login Admin & Kasir
- Role-based access
- CTRL + Z global untuk kembali ke menu utama

---

### 👨‍💼 Admin Features
- Lihat Menu
- Tambah Menu
- Update Menu
- Hapus Menu
- Laporan Bulanan PDF
- Dashboard Grafik Penjualan

---

### 💳 Kasir Features
- Transaksi Penjualan
- Input Nama Pemesan
- Input Jumlah Pesanan
- Diskon (%)
- Pajak 10%
- Hitung Kembalian otomatis
- Cetak:
  - Invoice A4 (PDF)
  - Struk Thermal (PDF)
- QR Code pembayaran
- Barcode Invoice
- Laporan Bulanan PDF
- Dashboard Grafik

---

### 📊 Dashboard
- Grafik Menu Terlaris (matplotlib)

---

### 📄 PDF Output
- Invoice A4 format tabel rapi
- Struk thermal layout printer kasir
- Logo café
- Nomor invoice otomatis
- QR Code
- Barcode Code128
- Laporan Bulanan detail (Nama, Tanggal, Menu, Qty, Total)

---

## 🧠 Arsitektur

Menggunakan OOP (Object Oriented Programming):

```
CafeSystem
├── MenuManager
├── TransactionManager
└── PDFGenerator
```

Struktur file:

```
📁 cafe-enterprise
 ├── cafe_system.py
 ├── menu.json
 ├── sales.json
 ├── logo_cafe.png
 └── README.md
```

---

# 🛠️ Instalasi

## 1️⃣ Clone Repository

```bash
git clone https://github.com/username/cafe-enterprise.git
cd cafe-enterprise
```

---

## 2️⃣ Buat Virtual Environment (Recommended)

```bash
python -m venv venv
```

Aktifkan:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install qrcode
pip install python-barcode
pip install reportlab
pip install matplotlib
pip install pillow
```

Atau gunakan:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Jalankan Program

```bash
python cafe_system.py
```

---

# 🔑 Default Login

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | 1234     |
| Kasir | kasir    | 1234     |

---

# 🎮 Cara Penggunaan

## CTRL + Z (Penting)

Tekan **CTRL + Z** atau **CTRL + C** kapan saja untuk kembali ke:

➡ MENU UTAMA (Login)

Berlaku di:
- Saat pilih menu
- Saat input transaksi
- Saat tambah/update menu
- Saat laporan
- Saat grafik

---

## 💳 Alur Transaksi

1. Login sebagai kasir
2. Pilih "Transaksi"
3. Input:
   - Nama Pemesan
   - Pilih menu
   - Jumlah
4. Input Diskon (jika ada)
5. Sistem hitung:
   - Pajak 10%
   - Total bayar
   - Kembalian
6. Pilih cetak:
   - Invoice A4
   - Struk Thermal

---

# 📦 Output Files

Setelah transaksi:

```
Invoice_INV0001.pdf
Struk_INV0001.pdf
qr_INV0001.png
barcode_INV0001.png
```

Laporan bulanan:

```
Laporan_Bulanan.pdf
```

---

# 📈 Dashboard Grafik

Menampilkan grafik:

- Menu Terlaris
- Total jumlah penjualan per item

Menggunakan matplotlib.

---

# ⚠ Error Handling

Sistem sudah menangani:

- Input harga salah
- Input jumlah bukan angka
- Uang kurang
- Menu tidak ditemukan
- CTRL + Z keluar dari sesi
- File JSON kosong

---

# 💎 Kelebihan Sistem

✔ OOP Architecture  
✔ Clean Code  
✔ PDF Professional Layout  
✔ Thermal Receipt Mode  
✔ QR & Barcode  
✔ Statistik Penjualan  
✔ Role-based Login  
✔ Global CTRL+Z  

---

# 🔮 Pengembangan Selanjutnya

- Versi GUI (Tkinter / CustomTkinter)
- Versi Web (Flask)
- Database MySQL/PostgreSQL
- Multi-user production system
- Export Excel
- Sistem stok otomatis
- Integrasi printer thermal asli

---

# 👨‍💻 Author

Cafe Enterprise System  
Built with ❤️ using Python

---

# 📜 License

Open-source project for educational & commercial prototype use.