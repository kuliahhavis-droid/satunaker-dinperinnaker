# 🏛️ Sistem Informasi Satu Data (SatuNaker)
### Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga

[![Next.js](https://img.shields.io/badge/Next.js-16.4-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel)](https://vercel.com/)

> **"Mewujudkan Tata Kelola Data Statistik Sektoral yang Terintegrasi, Valid, Akurat, dan Terpercaya Menuju Satu Data Indonesia di Tingkat Daerah"**

---

## 📌 Gambaran Umum Sistem

**SatuNaker** adalah portal portal data statistik sektoral terpadu yang dirancang dan dikembangkan sebagai simpul sentral (*Single Source of Truth*) di lingkungan **Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga**. 

Sistem ini mentransformasikan pencatatan data konvensional berbasis lembar sebar (*spreadsheet*) terfragmentasi (*data silo*) menjadi arsitektur web modern terpusat yang aman, waktu-nyata (*real-time*), dan akuntabel. Melalui sistem ini, pimpinan dinas dapat memantau indikator kinerja sektoral secara langsung, sedangkan operator unit kerja dapat menginput, memperbarui, mengekspor, serta mencetak laporan ber-kop resmi Pemerintah Kabupaten Purbalingga secara instan.

🌐 **Akses Produksi (Live):** [https://satunaker-dinperinnaker.vercel.app](https://satunaker-dinperinnaker.vercel.app)  
📁 **Repositori Resmi:** [https://github.com/kuliahhavis-droid/satunaker-dinperinnaker](https://github.com/kuliahhavis-droid/satunaker-dinperinnaker)

---

## 🏢 Cakupan Unit Kerja Operasional

SatuNaker mengintegrasikan aliran pencatatan data dari **7 (tujuh) unit kerja** di lingkungan DINPERINNAKER Kabupaten Purbalingga (berdasarkan Peraturan Bupati Purbalingga Nomor 91 Tahun 2025):

1. **Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK)**
   - Pencatatan Perjanjian Kerja Bersama (PKB), LKS Bipartit, kepesertaan BPJS Ketenagakerjaan, mogok kerja, dan penyelesaian perselisihan hubungan industrial.
2. **Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK)**
   - Registrasi pencari kerja (AK-1), penempatan tenaga kerja lokal/antardaerah (AKAD/AKAN), bursa kerja (*Job Fair*), dan pemagangan.
3. **Bidang Industri**
   - Pembinaan Industri Kecil Menengah (IKM), legalitas NIB/SIINas, fasilitasi sertifikasi halal, dan pengawasan kawasan sentra industri.
4. **Subbagian Perencanaan dan Keuangan (Sekretariat)**
   - Kompilasi indikator Laporan Kinerja Instansi Pemerintah (LKjIP), realisasi anggaran, dan evaluasi program kerja dinas.
5. **Subbagian Umum dan Kepegawaian (Sekretariat)**
   - Pengelolaan aset operasional, data aparatur sipil negara (ASN) dinas, dan ketatausahaan surat dinas.
6. **UPTD Balai Latihan Kerja (BLK)**
   - Rekapitulasi peserta pelatihan vokasi institusional/MTU, kelulusan, dan sertifikasi kompetensi BNSP.
7. **UPTD Pengembangan Industri Logam (PILOG)**
   - Produksi komponen knalpot lokal, utilisasi mesin uji emisi, fasilitasi standardisasi SNI, dan pelayanan teknis IKM logam.

---

## ⚡ Fitur-Fitur Unggulan

- 📊 **Dasbor Eksekutif & Pemantauan Interaktif:** Visualisasi capaian data makro dinas, persentase kelengkapan bukti fisik, serta penyaringan cepat berdasarkan tahun anggaran kinerja.
- 🔒 **Role-Based Access Control (RBAC):** Hak akses berjenjang untuk 5 tingkatan pengguna (*Super Admin*, *Kepala Dinas*, *Admin Bidang*, *Admin Sekretariat*, dan *Admin UPTD*).
- 🛡️ **Auto-Lock Unit Kerja:** Mekanisme penguncian otomatis pada formulir penambahan data operator bidang untuk mencegah kekeliruan penginputan data lintas unit kerja.
- 🔗 **Integrasi Bukti Fisik Awan:** Tautan langsung ke repositori digital Google Drive dinas untuk verifikasi instan berkas fisik (SK, sertifikat, risalah mediasi).
- 🖨️ **Generator Cetak Ber-Kop Resmi Pemkab:** Pencetakan dokumen berstandar Tata Naskah Dinas Pemerintah Kabupaten Purbalingga lengkap dengan format tanda tangan Kepala Dinas berbasis *CSS Print Media*.
- 📥 **Ekspor Lembar Sebar Excel (.xlsx):** Fasilitas unduh rekapitulasi data sektoral tabular secara utuh dan bersih.
- 💾 **Pencadangan Mandiri (Backup & Restore SQL):** Fitur ekspor basis data SQL/JSON serta pemulihan mandiri (*disaster recovery*) langsung dari antarmuka web.
- 🌓 **Dual Theme & Command Palette:** Tampilan Mode Terang (*Light Mode*) dan Mode Gelap (*Dark Mode*) serta navigasi pintas keyboard (`Ctrl + K`).

---

## 🔐 Standar Operasional Prosedur (SOP) Keamanan Akun

> [!IMPORTANT]
> **Kebijakan Kerahasiaan Kredensial Produksi:**
> Demi menjaga keamanan dan integritas data kepemerintahan daerah, **kata sandi awal akun pengguna TIDAK dicantumkan pada repositori publik ini**. Kredensial awal diserahkan secara tertutup melalui **Berita Acara Serah Terima Sistem** kepada Penanggung Jawab IT / Administrator DINPERINNAKER.

### Tindakan Wajib Setelah Serah Terima:
1. Administrator sistem wajib segera melakukan penggantian kata sandi *default* untuk seluruh akun melalui menu **Manajemen Pengguna** (`/users`).
2. Terapkan kata sandi kuat dengan kombinasi huruf besar, huruf kecil, angka, dan karakter simbol khusus.
3. Hak akses pengeditan dan penghapusan data master hanya diperuntukkan bagi peran **Super Admin**.

---

## 🛠️ Arsitektur Teknologi

| Lapisan Sistem | Teknologi / Komponen |
| :--- | :--- |
| **Kerangka Kerja Web** | [Next.js 16 (App Router)](https://nextjs.org/) + [React 19](https://react.dev/) |
| **Bahasa Pemrograman** | [TypeScript 5](https://www.typescriptlang.org/) (Strict Mode) |
| **Desain Antarmuka & Gaya** | [Tailwind CSS v4](https://tailwindcss.com/) + Lucide React Icons |
| **Animasi & Interaksi** | Framer Motion & Sonner Toast Notifications |
| **Basis Data Utama** | [Supabase PostgreSQL Cloud](https://supabase.com/) (*Row Level Security* & Realtime) |
| **Mesin Ekspor Berkas** | SheetJS (XLSX Engine) |
| **Infrastruktur Hosting** | [Vercel Cloud Platform](https://vercel.com/) (Edge Network & Serverless) |

---

## 🚀 Panduan Instalasi Lokal (Pengembangan)

Jika tim teknis dinas ingin menjalankan sistem di komputer lokal:

### 1. Kloning Repositori
```bash
git clone https://github.com/kuliahhavis-droid/satunaker-dinperinnaker.git
cd satunaker-dinperinnaker
```

### 2. Instalasi Dependensi
```bash
npm install
```

### 3. Konfigurasi Variabel Lingkungan
Salin berkas `.env.example` menjadi `.env.local`:
```bash
cp .env.example .env.local
```
Sesuaikan parameter kredensial Supabase Anda:
```env
NEXT_PUBLIC_SUPABASE_URL=https://twfgsuycpikbnxpsrwrk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

### 4. Menjalankan Server Lokal
```bash
npm run dev
```
Buka peramban web pada alamat [http://localhost:3000](http://localhost:3000).

---

## 📄 Skema Basis Data

Struktur tabel relasional basis data PostgreSQL telah tersedia lengkap pada berkas:
👉 **[`supabase_schema.sql`](./supabase_schema.sql)**

Skema mencakup 4 tabel utama:
1. `unit_kerja` — Master 7 unit kerja dinas.
2. `profiles` — Profil pengguna dan otorisasi hak akses (RBAC).
3. `data_records` — Entitas pencatatan data statistik sektoral per tahun dan tautan bukti fisik.
4. `log_aktivitas` — Jejak audit digital (*audit trail*) setiap aktivitas penambahan, pengubahan, dan penghapusan data.

---

## 📍 Kontak Resmi Instansi

**Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga**  
Pemerintah Kabupaten Purbalingga  
- 🏢 **Alamat:** Jl. Letnan Kusni No. 06, Kedung Menjangan, Kec. Purbalingga, Jawa Tengah 53315  
- 📞 **Telepon:** (0281) 891044  
- 🌐 **Situs Resmi:** [https://dinperinnaker.purbalinggakab.go.id](https://dinperinnaker.purbalinggakab.go.id)  
- ✉️ **Surel Resmi:** dinperinnaker@purbalinggakab.go.id  

---

*Hak Cipta © 2026 DINPERINNAKER Kabupaten Purbalingga. Dikembangkan dalam Program Kerja Praktik Teknik Informatika Universitas Muhammadiyah Purwokerto.*
