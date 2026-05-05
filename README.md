# Arithmetic_Coding_Web_Flask
A full-stack web application that demonstrates the Arithmetic Coding compression algorithm. This project uses a Flask backend to handle the complex mathematical calculations and scaling logic, providing a seamless experience for encoding and decoding data.

# 🗜️ Arithmetic Coding — Pembelajaran Interaktif

> Aplikasi web interaktif untuk memvisualisasikan dan memahami algoritma **Arithmetic Coding** secara step-by-step, dibangun dengan Flask dan antarmuka modern berbasis dark theme.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📖 Tentang Proyek

Arithmetic Coding adalah teknik kompresi data lossless yang merepresentasikan seluruh pesan sebagai satu bilangan dalam rentang `[0, 1)`. Berbeda dengan Huffman Coding yang memetakan tiap simbol ke kode biner tetap, Arithmetic Coding mampu mendekati batas entropi Shannon secara optimal.

Aplikasi ini dibuat sebagai **alat bantu pembelajaran** yang menampilkan:

- Proses penyempitan interval secara interaktif per simbol
- Tabel probabilitas dan frekuensi karakter
- Visualisasi bitstream hasil encoding dengan highlight bit `0` dan `1`
- Statistik kompresi: rasio kompresi, entropi, panjang bitstream
- Algoritma scaling E1/E2/E3 dengan presisi 16-bit

---

## ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| 🔢 Encoding Step-by-Step | Menampilkan nilai `low` dan `high` sebelum dan sesudah setiap simbol |
| 📊 Tabel Probabilitas | Frekuensi, probabilitas, dan cumulative range tiap simbol |
| 🧮 Bitstream Viewer | Output bit dengan pewarnaan untuk bit `0` (biru) dan `1` (oranye) |
| 📉 Rasio Kompresi | Perbandingan ukuran bitstream vs ukuran asli (ASCII 8-bit) |
| 📐 Entropi Shannon | Kalkulasi entropi teoritis sebagai batas bawah kompresi |
| 🎨 UI Dark Mode | Antarmuka modern dengan efek glow dan grid background |
| ⚡ Contoh Cepat | Tombol preset teks untuk langsung mencoba encoding |

---

## 🖥️ Demo Tampilan

```
Input  : "hello world"
Output : 01001011010110...
Entropi: 2.8454 bit/simbol
Rasio  : 47.16% dari ukuran asli
```

---

## 🚀 Instalasi & Menjalankan

### Prasyarat

- Python **3.8** atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

**1. Clone repositori**

```bash
git clone https://github.com/username/arithmetic-coding.git
cd arithmetic-coding
```

**2. Buat virtual environment** *(direkomendasikan)*

```bash
python -m venv venv

# Aktivasi di Linux/macOS
source venv/bin/activate

# Aktivasi di Windows
venv\Scripts\activate
```

**3. Install dependensi**

```bash
pip install flask
```

**4. Siapkan struktur folder**

Pastikan struktur direktori sebagai berikut:

```
arithmetic-coding/
├── app.py
└── templates/
    └── index.html
```

> ⚠️ File `index.html` **harus** berada di dalam folder `templates/` agar Flask dapat menemukannya.

**5. Jalankan aplikasi**

```bash
python app.py
```

**6. Buka di browser**

```
http://127.0.0.1:5000
```

---

## 📁 Struktur Proyek

```
arithmetic-coding/
├── app.py              # Backend Flask + logika Arithmetic Coding
├── templates/
│   └── index.html      # Frontend interaktif (Tailwind CSS + Vanilla JS)
├── requirements.txt    # Daftar dependensi
└── README.md
```

---

## 🔧 Konfigurasi

Parameter encoding dapat diubah langsung di `app.py`:

```python
PRECISION    = 16          # Presisi bit (menentukan MAX_RANGE)
MAX_RANGE    = (1 << 16) - 1   # = 65535
HALF         = 32768
QUARTER      = 16384
THREE_QUARTER = 49152
```

---

## 📡 API Endpoint

### `POST /encode`

Melakukan encoding teks menggunakan Arithmetic Coding.

**Request Body:**
```json
{
  "text": "hello world"
}
```

**Response:**
```json
{
  "success": true,
  "text": "hello world",
  "bitstream": "010011010...",
  "bit_length": 44,
  "original_bits": 88,
  "compression_ratio": 50.0,
  "entropy": 2.8454,
  "total_chars": 11,
  "prob_table": [...],
  "encoding_steps": [...]
}
```

**Batasan input:**
- Hanya huruf kecil `a–z` dan spasi
- Maksimal **200 karakter**

---

## ⚙️ Cara Kerja Algoritma

1. **Hitung Frekuensi** — Hitung kemunculan tiap simbol dalam teks
2. **Buat Tabel Kumulatif** — Tentukan rentang `[low, high)` untuk tiap simbol
3. **Penyempitan Interval** — Untuk setiap simbol, persempit interval `[low, high)` sesuai rentang simbolnya
4. **Scaling E1/E2/E3** — Renormalisasi interval menggunakan bit stuffing untuk mencegah underflow
5. **Finalisasi** — Output bit terakhir berdasarkan posisi interval akhir

---

## 🛠️ Teknologi

- **Backend:** Python, Flask
- **Frontend:** HTML5, Tailwind CSS (CDN), Vanilla JavaScript
- **Font:** Syne (UI), Space Mono (kode/angka) via Google Fonts
- **Algoritma:** Arithmetic Coding dengan integer arithmetic 16-bit + E1/E2/E3 scaling

---

## 📝 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

## 🤝 Kontribusi

Kontribusi sangat disambut! Silakan buka *issue* atau kirim *pull request*.

1. Fork repositori ini
2. Buat branch baru: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m 'feat: tambah fitur X'`
4. Push ke branch: `git push origin fitur/nama-fitur`
5. Buka Pull Request
