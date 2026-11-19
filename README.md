# 📊 Sistem Informasi Satu Data (SatuNaker)
### Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga

> **"Satu Data untuk Perencanaan yang Akurat, Terukur, dan Terpercaya"**

Portal Satu Data terpadu untuk pengelolaan, validasi, dan pelaporan statistik sektoral bidang perindustrian dan ketenagakerjaan di lingkungan Pemerintah Kabupaten Purbalingga.

---

## 🚀 Fitur Utama

- **Single Source of Truth**: Integrasi data dari Bidang HIJTK, Bidang PPTK, Sekretariat (Renkeu & Umpeg), dan Balai UPTD (BLK & PILOG).
- **Dashboard Monitoring Real-time**: Metrik capaian makro, grafik sebaran sektoral Chart.js, persentase berkas Google Drive, dan filter per tahun anggaran.
- **Role-Based Access Control (RBAC)**: Pembagian wewenang ketat untuk 5 tingkatan pengguna (Super Admin, Admin Bidang, Admin UPTD, Admin Sekretariat, dan Kepala Dinas).
- **Validasi Kepemilikan Data**: Isolasi hak tambah, ubah, dan hapus data sektoral berbasis unit kerja dengan tanda kepemilikan visual (*Badge Ownership*).
- **Laporan Resmi Ber-Kop Surat Pemkab**: Generator cetak dokumen berstandar Tata Naskah Dinas resmi Pemkab Purbalingga siap cetak fisik atau simpan PDF.
- **Ekspor Lembar Kerja Excel**: Unduh rekapitulasi data sektoral langsung ke format `.xlsx` via SheetJS.
- **Pencadangan & Pemulihan Mandiri**: Unduh dump SQL / JSON dan fitur restore SQL langsung dari browser.
- **Dual Theme & Navigasi Cepat**: Mode Gelap (Dark Mode), Mode Terang (Light Mode), dan Command Palette (`Ctrl + K`).

---

## 🛠️ Spesifikasi Teknologi

- **Frontend & Fullstack**: [Next.js 16 (App Router)](https://nextjs.org) + [React 19](https://react.dev)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com) (Dual Theme)
- **Basis Data**: [Supabase Cloud PostgreSQL](https://supabase.com) (Realtime + RLS) & LocalStorage Fallback
- **Komponen & Visualisasi**: Framer Motion, Chart.js, Lucide Icons, SheetJS (XLSX), Sonner
- **Process Manager**: PM2 Cluster Mode (`ecosystem.config.cjs`)

---

## ⚡ Panduan Memulai Cepat (Quick Start)

### 1. Instalasi Dependensi
```bash
npm install
```

### 2. Konfigurasi Environment (`.env.local`)
Salin berkas `.env.example` menjadi `.env.local` *(opsional, sistem tetap jalan normal dengan data lokal)*:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Menjalankan Server Pengembangan
```bash
npm run dev
```
Buka peramban di [http://localhost:3000](http://localhost:3000).

---

## 🔑 Kredensial Akun Default (Demo)

| Username | Password | Role | Unit Kerja |
| :--- | :--- | :--- | :--- |
| `superadmin` | `SuperAdmin#2026` | **Super Admin** | Semua Unit |
| `kadis` | `kadis#2026` | **Kepala Dinas** | Mode Eksekutif (Read-Only) |
| `admin_hijtk` | `hijtk#2026` | **Admin Bidang** | Bidang HIJTK |
| `admin_pptk` | `pptk#2026` | **Admin Bidang** | Bidang PPTK |
| `admin_renkeu` | `renkeu#2026` | **Admin Sekretariat** | Subag Perencanaan & Keuangan |
| `admin_blk` | `blk#2026` | **Admin UPTD** | UPTD Balai Latihan Kerja (BLK) |
| `admin_pilog` | `pilog#2026` | **Admin UPTD** | UPTD Pengembangan Industri Logam |

*(Tersedia juga fitur **Quick Role Selector** di halaman `/login` untuk berpindah peran dalam satu kali klik)*.

---

## 📚 Dokumentasi Lengkap Proyek

Dokumentasi komprehensif teknis, arsitektur, diagram alur bisnis, skema basis data PostgreSQL, dan panduan deployment tersedia pada:
👉 **[DOKUMENTASI_PROYEK.md](./DOKUMENTASI_PROYEK.md)**

---

*Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga*
