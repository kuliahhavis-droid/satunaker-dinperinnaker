# 📘 Panduan Lengkap Menjalankan Website SatuNaker di Localhost:3000
### Sistem Informasi Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga

Dokumen ini merupakan panduan teknis operasional resmi untuk mengunduh, mengonfigurasi, dan menjalankan aplikasi web **SatuNaker** pada lingkungan komputer lokal (*localhost:3000*) untuk kebutuhan demonstrasi, bimbingan, evaluasi penguji, maupun pengembangan lebih lanjut.

---

## 💻 1. Prasyarat Sistem (Prerequisites)

Sebelum menjalankan aplikasi, pastikan komputer Anda telah terinstal perangkat lunak berikut:

| Perangkat Lunak | Versi yang Disarankan | Perintah Pengecekan di Terminal |
| :--- | :--- | :--- |
| **Node.js** | Versi 18.17+ atau 20 LTS (Disarankan v20.x) | `node -v` |
| **NPM** | Versi 9+ atau 10+ (Terbawa otomatis dari Node.js) | `npm -v` |
| **Git** | Versi 2.30+ | `git --version` |
| **Peramban Web** | Google Chrome, Microsoft Edge, atau Mozilla Firefox | - |
| **Koneksi Internet** | Aktif (Dibutuhkan untuk sinkronisasi basis data Supabase Cloud) | - |

> [!NOTE]
> Jika Node.js belum terpasang di komputer Anda, unduh penginstal resmi versi LTS melalui: [https://nodejs.org/](https://nodejs.org/).

---

## 🚀 2. Langkah-Langkah Menjalankan di Localhost:3000

### Langkah 1: Buka Terminal / PowerShell
Buka aplikasi **Terminal**, **PowerShell**, atau **Command Prompt** (atau buka terminal terintegrasi di VS Code dengan menekan tombol `Ctrl + ~`).

Arahkan direktori aktif ke folder proyek `satudata-nextjs`:
```powershell
cd D:\Magang\sistem-satudata-dinperinnaker\satudata-nextjs
```
*(Sesuaikan path folder jika Anda menaruh repositori di lokasi lain).*

---

### Langkah 2: Periksa dan Konfigurasi File Lingkungan (`.env.local`)
Pastikan berkas bernama `.env.local` telah tersedia di dalam folder root `satudata-nextjs`.

Jika belum ada, buat salinannya dari template `.env.example`:
```powershell
copy .env.example .env.local
```

Buka dan pastikan isi berkas `.env.local` memuat parameter kredensial Supabase PostgreSQL aktif:
```env
# ========================================================
# KONEKSI RESMI SUPABASE CLOUD (SATUNAKER PURBALINGGA)
# ========================================================
NEXT_PUBLIC_SUPABASE_URL=https://twfgsuycpikbnxpsrwrk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
*(Kredensial anonim publik di atas telah dikonfigurasi aktif mengarah ke basis data awan produksi DINPERINNAKER Kabupaten Purbalingga).*

---

### Langkah 3: Pasang Dependensi Node.js (`npm install`)
Unduh dan pasang seluruh pustaka pustaka dependensi proyek:
```powershell
npm install
```
Tunggu hingga proses instalasi paket selesai (biasanya memakan waktu 10–30 detik tergantung kecepatan internet).

---

### Langkah 4: Jalankan Server Pengembangan Lokal (`npm run dev`)
Ketikkan perintah berikut untuk menyalakan server lokal Next.js dengan akselerasi Turbopack:
```powershell
npm run dev
```

Jika server berhasil berjalan, Anda akan melihat pesan berikut di layar terminal:
```text
  ▲ Next.js 16.4.2 (Turbopack)
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 1450ms
```

---

### Langkah 5: Buka Aplikasi di Browser
Buka peramban web (Google Chrome atau Microsoft Edge), lalu ketikkan alamat berikut di bilah URL:
👉 **[http://localhost:3000](http://localhost:3000)**

Halaman login SatuNaker atau Dashboard Eksekutif akan langsung terbuka dengan animasi halus.

---

## 🔑 3. Daftar Akun Pengguna untuk Pengujian & Demo

SatuNaker menerapkan **Role-Based Access Control (RBAC)** dengan batasan wewenang berjenjang. Anda dapat mencoba login menggunakan salah satu akun simulasi berikut:

| No | Peran Akun (Role) | Username / Email | Password Pengujian | Lingkup Wewenang & Hak Akses |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Super Admin** | `superadmin` *(atau `superadmin@dinperinnaker.go.id`)* | `admin123` *(atau `SuperAdmin#2026`)* | Akses **penuh 100%**: Kelola seluruh unit kerja, Manajemen Pengguna (`/users`), Master Unit Kerja (`/unit-kerja`), Backup & Restore Database (`/backup`), ekspor Excel, dan cetak laporan. |
| **2** | **Admin Bidang HIJTK** | `admin_hijtk` *(atau `hijtk@dinperinnaker.go.id`)* | `admin_hijtk#2026` *(atau `password123`)* | Hanya dapat menginput, mengedit, dan menghapus data Bidang Hubungan Industrial & Jamsostek. Formulir entri otomatis terkunci (*auto-lock*) pada unit kerja HIJTK. |
| **3** | **Admin Bidang PPTK** | `admin_pptk` *(atau `pptk@dinperinnaker.go.id`)* | `admin_pptk#2026` *(atau `password123`)* | Khusus mengelola data Bidang Pelatihan & Penempatan Tenaga Kerja (Pencari kerja, penempatan, bursa kerja). Terkunci otomatis pada unit kerja PPTK. |
| **4** | **Admin Bidang Industri** | `admin_renkeu` *(atau `renkeu@dinperinnaker.go.id`)* | `admin_renkeu#2026` *(atau `password123`)* | Khusus data Sekretariat / Perencanaan Keuangan (LKjIP, anggaran, program dinas). |
| **5** | **Admin BLK** | `admin_blk` *(atau `blk@dinperinnaker.go.id`)* | `admin_blk#2026` *(atau `password123`)* | Khusus data UPTD Balai Latihan Kerja (Peserta pelatihan, sertifikasi kompetensi BNSP). |
| **6** | **Kepala Dinas (Pimpinan)** | `kadis` *(atau `kadis@dinperinnaker.go.id`)* | `kadis#2026` *(atau `password123`)* | Mode **Eksekutif (Read-Only)**: Memantau grafik statistik makro dinas, persentase kelengkapan bukti fisik, filter multi-tahun, ekspor Excel, dan pratinjau cetak ber-kop resmi. |

> [!TIP]
> **Kata Sandi Cadangan Bersama:** Seluruh akun operator juga dapat dibuka menggunakan kata sandi alternatif `password123`.

---

## 🧭 4. Skenario Pengujian Fitur Utama di Localhost:3000

Saat mendemonstrasikan sistem di hadapan Dosen Pembimbing maupun Penguji, ikuti alur skenario pengujian berikut:

### Skenario 1: Halaman Login & Proteksi Keamanan (`/login`)
- Coba masukkan sembarang password yang salah untuk membuktikan validasi peringatan error interaktif.
- Centang fitur **Ingat Saya (Remember Me)** lalu tekan tombol **Masuk ke Sistem**.
- Sistem menampilkan *loading overlay* dinamis dan mengarahkan ke dasbor.

### Skenario 2: Dasbor Eksekutif & Filter Tahun Anggaran (`/`)
- Amati 4 kartu KPI utama (Total Indikator Sektoral, Rekaman Data Masuk, Unit Kerja Aktif, dan Kelengkapan Bukti Fisik).
- Klik tombol **Filter Tahun** (misal pilih tahun 2024 atau 2025) untuk menguji kalkulasi agregasi dinamis tanpa memuat ulang (*reload*) halaman.

### Skenario 3: Manajemen Data Sektoral & Proteksi Auto-Lock (`/kelola-data`)
- Masuk sebagai `admin_hijtk`, lalu klik tombol **+ Tambah Data**.
- Perhatikan pada kolom pilihan **Unit Kerja**: sistem secara otomatis mengunci dropdown pada *"Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja"* sehingga operator tidak dapat merusak atau mengubah data milik bidang lain.
- Isi nama indikator, satuan, jumlah, dan tempelkan tautan URL Google Drive bukti fisik (contoh: `https://drive.google.com/drive/folders/contoh`).
- Klik **Simpan Data**. Sistem memicu animasi konfeti perayaan (*canvas-confetti*) dan notifikasi *toast* sukses.

### Skenario 4: Pusat Rekapitulasi Laporan & Ekspor Excel (`/laporan`)
- Buka menu **Laporan**.
- Gunakan fitur pencarian instan dan filter unit kerja.
- Klik tombol **Ekspor ke Excel (.xlsx)**. File lembar sebar akan terunduh otomatis ke folder Downloads komputer Anda dengan format tabel yang rapi dan terstruktur.

### Skenario 5: Mesin Cetak Ber-Kop Resmi Pemkab Purbalingga (`/laporan/print`)
- Klik tombol **Cetak Laporan Resmi**.
- Halaman pratinjau cetak terbuka dengan standar Tata Naskah Dinas resmi:
  - Lambang Garuda / Kop Dinas resmi Kabupaten Purbalingga.
  - Garis ganda pembatas kop surat.
  - Tabel statistik buku terbuka (open border).
  - Lembar pengesahan tanda tangan Kepala Dinas (Johan Arifin, S.Sos., M.Si. NIP. 19740618 199311 1 001).
- Tekan `Ctrl + P` untuk melihat hasil pratinjau cetak di peramban (dapat langsung diekspor sebagai PDF).

### Skenario 6: Modul Administrator Khusus Super Admin
- Login sebagai `superadmin`:
  - **Master Unit Kerja (`/unit-kerja`):** Tambah, ubah kode singkatan, atau perbarui deskripsi 7 unit kerja dinas.
  - **Manajemen Akun (`/users`):** Tambah operator baru, ubah peran RBAC, aktifkan/nonaktifkan status akun, atau reset sandi staf dinas.
  - **Pencadangan Mandiri (`/backup`):** Klik **Unduh Cadangan Basis Data (JSON/SQL)** untuk mengamankan data instansi.

---

## ⌨️ 5. Fitur Aksesibilitas Cepat
- **Command Palette (`Ctrl + K`):** Tekan kombinasi tombol `Ctrl + K` pada papan ketik di halaman mana pun untuk membuka jendela pencarian cepat menuju menu apa saja secara instan.
- **Mode Gelap / Terang (Dark / Light Theme):** Klik ikon matahari/bulan pada navbar atas untuk beralih antara tema gelap dan terang secara mulus.

---

## 🛠️ 6. Panduan Pemecahan Masalah (Troubleshooting)

### Kendala 1: Port 3000 Sedang Digunakan (Port Already in Use)
**Gejala:** Muncul pesan `Error: listen EADDRINUSE: address already in use :::3000`.  
**Solusi A (Jalankan di port lain):**
```powershell
npm run dev -- -p 3001
```
Lalu buka [http://localhost:3001](http://localhost:3001).

**Solusi B (Matikan proses yang mengunci port 3000):**
```powershell
npx kill-port 3000
npm run dev
```

---

### Kendala 2: Cache Next.js Tersangkut atau Layar Putih (Blank)
**Gejala:** Perubahan kode tidak muncul atau kompilasi lokal melambat.  
**Solusi:** Hapus folder cache `.next` lalu nyalakan ulang server:
```powershell
Remove-Item -Recurse -Force .next
npm run dev
```

---

### Kendala 3: Gagal Terhubung ke Basis Data Supabase
**Gejala:** Notifikasi "Gagal memuat data dari basis data".  
**Solusi:**
1. Pastikan komputer Anda terhubung ke internet.
2. Periksa kembali isi file `.env.local` dan pastikan nilai `NEXT_PUBLIC_SUPABASE_URL` diawali dengan `https://` dan tidak memiliki spasi di awal/akhir baris.
3. Simpan perubahan file, lalu restart server lokal (`Ctrl + C` lalu ketik `npm run dev`).

---

*Hak Cipta © 2026 DINPERINNAKER Kabupaten Purbalingga & Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto.*
