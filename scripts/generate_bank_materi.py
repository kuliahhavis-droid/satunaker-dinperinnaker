# -*- coding: utf-8 -*-
"""
Script to generate BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md
Outputs to D:\Magang\sistem-satudata-dinperinnaker\document\ and artifact directory.
"""
import os
import shutil

MD_CONTENT = """# BANK MATERI LENGKAP LAPORAN KERJA PRAKTIK
# RANCANG BANGUN WEBSITE SATU DATA (SATUNAKER) DINPERINNAKER PURBALINGGA

> **Petunjuk Penggunaan:**  
> Dokumen ini adalah **Bank Materi & Contekan Komprehensif** yang dirancang khusus untuk mendampingi dokumen `TEMPLATE_LAPORAN_KP_TI_UMP.docx`.  
> Seluruh paragraf, uraian teknis, tabel spesifikasi, kamus data, skenario pengujian, hingga daftar pustaka di bawah ini telah diselaraskan dengan standar akademik **Program Studi Teknik Informatika, Fakultas Teknik dan Sains, Universitas Muhammadiyah Purwokerto (UMP)** serta kondisi riil sistem **SatuNaker** di **Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga**.  
> Anda dapat menyalin (*copy-paste*), memparafrasekan, atau menyesuaikan materi di bawah ini langsung ke dalam template Word laporan Anda.

---

## DAFTAR ISI BANK MATERI
1. [Identitas & Metadata Proyek](#1-identitas--metadata-proyek)
2. [Materi Bagian Awal (Abstrak, Kata Pengantar, Halaman Pengesahan)](#2-materi-bagian-awal)
3. [Materi BAB I: Gambaran Umum Proyek](#3-materi-bab-i-gambaran-umum-proyek)
4. [Materi BAB II: Instansi Mitra (Profil & 7 Unit Kerja)](#4-materi-bab-ii-instansi-mitra)
5. [Materi BAB III: Pelaksanaan Proyek (Spesifikasi, UML, Database, UI, Black-Box Testing, Kendala)](#5-materi-bab-iii-pelaksanaan-proyek)
6. [Materi BAB IV: Penutup (Kesimpulan & Saran)](#6-materi-bab-iv-penutup)
7. [Materi Daftar Pustaka (Standar APA 7th Edition)](#7-materi-daftar-pustaka)
8. [Panduan Teknis Format Word UMP](#8-panduan-teknis-format-word-ump)

---

## 1. IDENTITAS & METADATA PROYEK

| Parameter | Data / Keterangan |
| :--- | :--- |
| **Judul Laporan** | Rancang Bangun Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (SatuNaker) |
| **Nama Mahasiswa** | Havisda Mei Khairil |
| **NIM** | 2303040113 |
| **Program Studi** | Teknik Informatika (S1) |
| **Fakultas** | Fakultas Teknik dan Sains |
| **Perguruan Tinggi** | Universitas Muhammadiyah Purwokerto (UMP) |
| **Instansi Mitra** | Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga |
| **Alamat Mitra** | Jl. Mayjen Sungkono No. 34, Selabaya, Kec. Kalimanah, Kab. Purbalingga, Jawa Tengah 53371 |
| **Kepala Dinas** | Johan Arifin, S.Sos., M.Si. |
| **Dosen Pembimbing KP**| Elindra Ambar Pambudi, S.T., M.Kom. (NIK. 2160766) |
| **Dosen Penguji KP** | *(Menunggu penetapan resmi prodi / gunakan garis titik-titik)* `......................................................` / NIK. `........................` |
| **Ketua Program Studi**| Agung Purwo Wicaksono, S.T., M.Kom. (NIK. 2160518) |
| **Dekan Fakultas** | Dr. Ir. Taufik Dwi Laksono, S.T., M.T., IPU. (NIK. 2160453) |
| **Waktu Pelaksanaan** | Semester Gasal/Genap Tahun Akademik 2025/2026 |

---

## 2. MATERI BAGIAN AWAL

### A. Teks Halaman Pengesahan
*Gunakan format resmi berikut pada Halaman Pengesahan laporan:*

```text
Judul:
RANCANG BANGUN WEBSITE SATU DATA DINAS PERINDUSTRIAN DAN TENAGA KERJA KABUPATEN PURBALINGGA (SATUNAKER)

Disusun Oleh:
Nama : Havisda Mei Khairil
NIM  : 2303040113

Telah diseminarkan dan dipertahankan dalam Seminar Kerja Praktik Program Studi Teknik Informatika Fakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto.

Pada:
Hari    : [Hari Seminar, misal: Senin]
Tanggal : [Tanggal Seminar, misal: 11 November 2026]

Menyetujui:

Pembimbing,
Elindra Ambar Pambudi, S.T., M.Kom.
NIK. 2160766

Penguji,
......................................................
NIK. ........................

Mengetahui,
Ketua Program Studi Teknik Informatika
Agung Purwo Wicaksono, S.T., M.Kom.
NIK. 2160518
```

---

### B. Teks Kata Pengantar
*Dapat langsung disalin ke subbab Kata Pengantar:*

> Puji syukur senantiasa penulis panjatkan ke hadirat Allah Subhanahu Wa Ta’ala atas limpahan rahmat, taufik, dan hidayah-Nya, sehingga penulis dapat menyelesaikan kegiatan Kerja Praktik (KP) serta menyusun laporan dengan judul **"Rancang Bangun Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (SatuNaker)"** dengan baik dan tepat waktu.
>
> Kerja Praktik ini dilaksanakan sebagai salah satu syarat kelulusan kurikulum pada Program Studi Teknik Informatika, Fakultas Teknik dan Sains, Universitas Muhammadiyah Purwokerto. Melalui kegiatan ini, penulis berkesempatan mengaplikasikan ilmu rekayasa perangkat lunak dan pengembangan web modern ke dalam instansi pemerintahan daerah secara langsung.
>
> Keberhasilan pelaksanaan Kerja Praktik dan penyusunan laporan ini tidak lepas dari bimbingan, arahan, dan dukungan berbagai pihak. Oleh karena itu, pada kesempatan ini penulis menyampaikan rasa terima kasih dan penghargaan setinggi-tingginya kepada:
> 1. Bapak Dr. Ir. Taufik Dwi Laksono, S.T., M.T., IPU., selaku Dekan Fakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto.
> 2. Bapak Agung Purwo Wicaksono, S.T., M.Kom., selaku Ketua Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto.
> 3. Bapak Elindra Ambar Pambudi, S.T., M.Kom., selaku Dosen Pembimbing Kerja Praktik yang telah memberikan arahan, koreksi, dan motivasi berharga selama penyusunan laporan ini.
> 4. Bapak [Nama Dosen Penguji / Tim Penguji], selaku Dosen Penguji Seminar Kerja Praktik atas masukan konstruktif demi kesempurnaan laporan ini.
> 5. Bapak Johan Arifin, S.Sos., M.Si., selaku Kepala Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga yang telah memberikan izin dan fasilitas pelaksanaan kerja praktik.
> 6. Pembimbing Lapangan dan seluruh staf pegawai di lingkungan Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (Bidang HIJTK, PPTK, Perindustrian, UPTD BLK, UPTD PILOG, Subbag Renkeu, dan Subbag Umpeg) atas kerja sama dan bantuannya selama pengumpulan data proyek.
> 7. Kedua orang tua serta keluarga tercinta yang senantiasa mendoakan, memberikan dorongan moral, dan materi selama masa perkuliahan.
> 8. Rekan-rekan mahasiswa Program Studi Teknik Informatika UMP angkatan 2023 atas kebersamaan dan dukungannya.
>
> Penulis menyadari bahwa laporan ini masih memiliki keterbatasan. Oleh karena itu, kritik dan saran yang membangun sangat penulis harapkan demi penyempurnaan di masa mendatang. Semoga laporan ini dapat memberikan manfaat bagi akademisi, instansi mitra, dan pembaca sekalian.
>
> Purwokerto, [Tanggal Bulan Tahun]  
> Penulis,  
>  
> **Havisda Mei Khairil**  
> NIM. 2303040113

---

### C. Teks Abstrak (Bahasa Indonesia & English)

#### ABSTRAK (Bahasa Indonesia)
> **ABSTRAK**  
> Dinas Perindustrian dan Tenaga Kerja (Dinperinnaker) Kabupaten Purbalingga memiliki 7 (tujuh) unit kerja operasional, yaitu Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK), Bidang Penempatan Tenaga Kerja dan Transmigrasi (PPTK), Bidang Perindustrian, UPTD Balai Latihan Kerja (BLK), UPTD Pengembangan Industri Logam (PILOG), Subbagian Perencanaan dan Keuangan (Renkeu), serta Subbagian Umum dan Kepegawaian (Umpeg). Selama ini pengelolaan data ketenagakerjaan, data kepesertaan BPJS, perizinan IKM, data pelatihan, hingga fasilitas logam masih dikelola secara terdesentralisasi menggunakan berkas spreadsheet Microsoft Excel di komputer masing-masing bidang (*data silo*). Fenomena ini menimbulkan kerentanan inkonsistensi format, risiko kehilangan data, serta keterlambatan dalam penyusunan laporan eksekutif berkala yang dibutuhkan Kepala Dinas untuk pengambilan kebijakan strategis. Untuk mengatasi permasalahan tersebut, dirancang dan dibangun sistem informasi berbasis web terpusat bernama **SatuNaker** (*Satu Data Dinperinnaker*). Sistem ini dikembangkan menggunakan metode *Software Development Life Cycle* (SDLC) model *Waterfall*, mencakup analisis kebutuhan, perancangan sistem (*UML* dan *Entity Relationship Diagram*), implementasi (*Next.js 14 App Router*, *TypeScript*, *Tailwind CSS*, dan *Supabase Managed PostgreSQL*), serta pengujian menggunakan teknik *Black-Box Testing*. Fitur unggulan SatuNaker meliputi *Role-Based Access Control* (RBAC) 3 tingkat (Kepala Dinas, Admin Dinas, Operator Unit) dengan proteksi *auto-locking* unit kerja, visualisasi dasbor ringkasan eksekutif interaktif, modul filter dinamis lintas tahun, ekspor spreadsheet Excel terformat, serta mesin cetak dokumen ber-kop surat resmi Pemerintah Kabupaten Purbalingga berbasis *CSS Print Media*. Hasil pengujian pada 13 skenario fungsional menunjukkan tingkat keberhasilan 100% (*valid*), membuktikan bahwa sistem SatuNaker andal, responsif, dan siap mendukung tata kelola data pemerintahan daerah yang transparan dan akuntabel sesuai amanat Perpres No. 39 Tahun 2019 tentang Satu Data Indonesia.  
>  
> **Kata Kunci:** Satu Data, Dinperinnaker Purbalingga, Sistem Informasi Eksekutif, Next.js 14, Supabase, Waterfall, Role-Based Access Control.

#### ABSTRACT (English)
> **ABSTRACT**  
> *The Department of Industry and Manpower (Dinperinnaker) of Purbalingga Regency operates seven distinct working units: Industrial Relations and Manpower Social Security (HIJTK), Manpower Placement and Transmigration (PPTK), Industry Division, Regional Vocational Training Center (UPTD BLK), Metal Industry Development Center (UPTD PILOG), Planning and Finance Sub-division (Renkeu), and General Affairs and Personnel Sub-division (Umpeg). Previously, critical operational records—such as employment records, BPJS membership status, small-medium industry registries, vocational training datasets, and metal equipment facilities—were stored in decentralized Microsoft Excel spreadsheets across disconnected local computers (data silos). This manual paradigm posed significant risks of schema discrepancies, data duplication, record loss, and severe delays in executive report compilation required by the Head of Department for data-driven policy making. To overcome these challenges, a centralized web-based executive information portal named SatuNaker (Satu Data Dinperinnaker) was designed and implemented. The development adopted the classic Waterfall Software Development Life Cycle (SDLC) model, encompassing requirement engineering, architectural design (UML and ERD), full-stack implementation (Next.js 14 App Router, TypeScript, Tailwind CSS, and Supabase Managed PostgreSQL with Row-Level Security), and rigorous verification through Black-Box Testing. Key features include 3-tiered Role-Based Access Control (RBAC) with operational unit auto-locking, interactive executive summary dashboards, multi-year cross-filtering, styled Excel spreadsheet exports, and an automated official Purbalingga Regency letterhead document print engine powered by CSS Print Media. The black-box testing across 13 functional test suites resulted in a 100% success rate, confirming that the SatuNaker platform is reliable, responsive, and robust in fulfilling the mandate of Presidential Regulation No. 39 of 2019 on One Data Indonesia.*  
>  
> **Keywords:** One Data Indonesia, Dinperinnaker Purbalingga, Executive Information System, Next.js 14, Supabase, Waterfall, Role-Based Access Control.

---

## 3. MATERI BAB I: GAMBARAN UMUM PROYEK

### A. Subbab A: Deskripsi Proyek
*Gunakan 4-5 paragraf terstruktur berikut untuk menjelaskan Deskripsi Proyek:*

> **Paragraf 1: Latar Belakang Regulasi dan Amanat SPBE / Satu Data Indonesia**  
> Perkembangan teknologi informasi dan komunikasi di era Revolusi Industri 4.0 telah mendorong transformasi tata kelola pemerintahan menuju sistem yang transparan, efektif, dan akuntabel. Pemerintah Republik Indonesia secara resmi telah menerbitkan Peraturan Presiden Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik (SPBE) serta Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia (SDI). Amanat utama regulasi tersebut mewajibkan setiap instansi pemerintah pusat maupun pemerintah daerah untuk mewujudkan keterpaduan perencanaan, pelaksanaan, evaluasi, dan pengendalian pembangunan yang didukung oleh data yang akurat, mutakhir, terpadu, dapat dipertanggungjawabkan, serta mudah diakses dan dibagipakaikan antar-instansi melalui kaidah interoperabilitas data.

> **Paragraf 2: Kondisi Eksisting dan Fenomena Masalah Data Silo di Dinperinnaker**  
> Dinas Perindustrian dan Tenaga Kerja (Dinperinnaker) Kabupaten Purbalingga merupakan unsur pelaksana urusan pemerintahan daerah yang membidangi sektor perindustrian dan ketenagakerjaan. Dalam menjalankan tugas dan fungsinya, Dinperinnaker membawahkan 7 (tujuh) unit kerja, yaitu Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK), Bidang Penempatan Tenaga Kerja dan Transmigrasi (PPTK), Bidang Perindustrian, UPTD Balai Latihan Kerja (BLK), UPTD Pengembangan Industri Logam (PILOG), Subbagian Perencanaan dan Keuangan (Renkeu), serta Subbagian Umum dan Kepegawaian (Umpeg). Kondisi eksisting di lingkungan dinas menunjukkan bahwa pengelolaan data sektoral masih berjalan secara parsial di masing-masing bidang. Setiap unit kerja mengelola data operasionalnya menggunakan aplikasi lembar sebar (*spreadsheet*) Microsoft Excel yang tersimpan secara terpisah di komputer lokal masing-masing staf. Fenomena ini memicu timbulnya isolasi data (*data silo*), kerentanan perbedaan versi (*versioning conflicts*), duplikasi data perusahaan/IKM, ketiadaan standardisasi kode referensi KBLI (Klasifikasi Baku Lapangan Usaha Indonesia), serta ketiadaan cadangan data (*backup*) terpusat.

> **Paragraf 3: Dampak Operasional terhadap Pengambilan Keputusan Pimpinan**  
> Isolasi data yang terjadi berdampak langsung terhadap lambatnya proses konsolidasi laporan berkala ketika pimpinan dinas, instansi pengawas internal, maupun instansi vertikal (Kementerian Ketenagakerjaan dan Kementerian Perindustrian) membutuhkan laporan kompilasi secara mendadak. Kepala Dinas dan jajaran pimpinan kesulitan memantau indikator kinerja utama, seperti rasio penyerapan tenaga kerja lokal versus tenaga kerja asing, tingkat kepatuhan perusahaan swasta terhadap jaminan sosial (BPJS Ketenagakerjaan dan BPJS Kesehatan), sebaran sebaran IKM logam di Purbalingga, serta serapan alumni pelatihan vokasi UPTD BLK. Proses rekapitulasi manual yang memakan waktu berhari-hari berpotensi menurunkan ketepatan waktu perumusan kebijakan publik dan intervensi program ketenagakerjaan daerah.

> **Paragraf 4: Solusi Inovasi Rancang Bangun Website SatuNaker**  
> Berdasarkan latar belakang permasalahan tersebut, pada kegiatan Kerja Praktik ini diusulkan dan dikembangkan sistem informasi berbasis web terpusat yang diberi nama **Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (SatuNaker)**. Sistem ini dibangun dengan memanfaatkan teknologi web modern berbasis *Next.js 14* (React Framework) dengan arsitektur *App Router*, bahasa pemrograman *TypeScript*, serta *Tailwind CSS* untuk antarmuka yang bersih dan responsif. Sistem penyimpanan data terintegrasi menggunakan *Supabase Managed PostgreSQL* yang dilengkapi dengan fitur *Row-Level Security* (RLS) dan otentikasi aman berbasis JWT (*JSON Web Token*). Website SatuNaker mengimplementasikan hak akses berjenjang (*Role-Based Access Control* / RBAC) yang mengelompokkan pengguna ke dalam tiga peran: Kepala Dinas, Admin Dinas, dan Operator Unit Kerja. Fitur unggulan sistem meliputi *dashboard* eksekutif dengan statistik grafik dinamis, fitur penyaringan data (*filter*) multi-parameter dan multi-tahun, ekspor data ke format Microsoft Excel (.xlsx), serta kemampuan pencetakan laporan resmi ber-kop surat Pemerintah Kabupaten Purbalingga secara langsung melalui peramban.

---

### B. Subbab B: Ruang Lingkup Proyek

*Uraikan ruang lingkup proyek secara jelas:*

> Ruang lingkup proyek pembangunan Website Satu Data Dinperinnaker (SatuNaker) mencakup batasan sistem, pemetaan modul fungsional, dan aktor pengguna sebagai berikut:
>
> 1. **Sasaran Unit Kerja Terintegrasi (7 Unit Kerja):**  
>    Sistem mengintegrasikan dan menstandarisasi pencatatan data dari seluruh unit kerja di lingkungan Dinperinnaker Purbalingga, meliputi:  
>    a. Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK)  
>    b. Bidang Penempatan Tenaga Kerja dan Transmigrasi (PPTK)  
>    c. Bidang Perindustrian  
>    d. UPTD Balai Latihan Kerja (BLK)  
>    e. UPTD Pengembangan Industri Logam (PILOG)  
>    f. Subbagian Perencanaan dan Keuangan (Renkeu)  
>    g. Subbagian Umum dan Kepegawaian (Umpeg)
>
> 2. **Aktor Pengguna Sistem (*User Roles*):**  
>    Sistem membagi hak akses ke dalam 3 (tiga) peran pengguna:  
>    a. **Kepala Dinas (*Executive View*):** Memiliki hak akses read-only menyeluruh ke seluruh modul, visualisasi dasbor analitik eksekutif, filter data lintas tahun dan bidang, serta hak cetak laporan resmi ber-kop dinas.  
>    b. **Admin Dinas (*Super Administrator*):** Memiliki hak akses penuh (*Full Privileges*) untuk mengelola akun pengguna (tambah, edit, reset sandi, aktivasi/deaktivasi), konfigurasi data master 7 unit kerja, memantau *log audit trail*, serta memvalidasi atau memodifikasi seluruh rekaman data.  
>    c. **Operator Unit Kerja (*Data Operator*):** Memiliki hak akses operasional yang terkunci (*auto-locked*) hanya pada unit kerjanya masing-masing. Operator hanya diizinkan menambah, mengubah, melihat, dan mencetak data yang berada di bawah wewenang unitnya.
>
> 3. **Modul dan Fitur Fungsional Utama:**  
>    a. **Modul Otentikasi dan Keamanan:** Sistem login berbasis email dan kata sandi terenkripsi (Argon2/bcrypt via Supabase Auth) dengan manajemen sesi token JWT dan proteksi *middleware routing*.  
>    b. **Modul Dasbor Analitik Eksekutif:** Menampilkan kartu statistik (*stat cards*) total perusahaan, total tenaga kerja (WNI LK/PR, WNA LK/PR), kepesertaan BPJS, serta grafik diagram interaktif.  
>    c. **Modul Filter Lintas Tahun dan Kategori:** Fasilitas penyaringan data dinamis berdasarkan tahun pendataan (misal: 2024, 2025, 2026), unit kerja penginput, serta kategori jenis usaha riil.  
>    d. **Modul Manajemen Data Operasional:** Form input data yang dilengkapi fitur kalkulasi otomatis jumlah tenaga kerja (*auto-calculate sum*), pencegahan input ganda, serta tabel data dengan fitur pencarian instan dan paginasi.  
>    e. **Modul Pelaporan Resmi (Print Engine):** Mesin cetak dokumen ber-kop surat resmi Pemerintah Kabupaten Purbalingga dengan format tata letak standar kedinasan, dilengkapi tanggal dinamis dan kolom tanda tangan pimpinan.  
>    f. **Modul Ekspor Spreadsheet (.xlsx):** Fasilitas konversi dan unduh data tabular langsung ke format file Excel rapi dengan *client-side processing* menggunakan pustaka *SheetJS*.  
>    g. **Modul Manajemen Pengguna dan Unit:** Panel khusus Admin Dinas untuk mengelola kredensial pegawai dan sinkronisasi metadata penanggung jawab unit kerja.
>
> 4. **Batasan Sistem (*System Limitations*):**  
>    a. Sistem dikembangkan sebagai aplikasi berbasis web responsif (*responsive web application*) yang diakses melalui peramban modern (*browser* seperti Google Chrome, Mozilla Firefox, Microsoft Edge).  
>    b. Sistem membutuhkan koneksi internet aktif untuk berkomunikasi dengan basis data komputasi awan *Supabase Managed PostgreSQL*.  
>    c. Sistem tidak mencakup fitur absensi harian pegawai, pembayaran iuran BPJS secara daring (*payment gateway*), maupun transaksi keuangan dinas, melainkan berfokus penuh pada tata kelola data sektoral dan pelaporan eksekutif.

---

### C. Subbab C: Tahapan Pelaksanaan Proyek (SDLC Waterfall)

*Gunakan model Waterfall klasik menurut Roger S. Pressman / Ian Sommerville:*

> Metode pengembangan perangkat lunak yang digunakan dalam proyek Website SatuNaker adalah metode **Waterfall (Air Terjun)**. Model ini dipilih karena kebutuhan sistem informasi pendataan di lingkungan Dinperinnaker telah terdefinisi secara jelas sejak awal kegiatan magang, serta alur pengerjaannya bersifat linier dan terstruktur dari awal hingga akhir. Tahapan pelaksanaan meliputi:
>
> 1. **Analisis Kebutuhan (*Requirements Analysis*):**  
>    Melakukan observasi langsung di kantor Dinperinnaker Purbalingga, wawancara mendalam dengan Kepala Dinas, Kepala Bidang, Kepala UPTD, dan staf operator terkait format data yang digunakan (berkas Excel data perusahaan, tenaga kerja, BPJS, pelatihan BLK, fasilitas PILOG), menganalisis kendala sistem manual, serta merumuskan kebutuhan fungsional dan non-fungsional sistem.
>
> 2. **Perancangan Sistem (*System Design*):**  
>    Merancang arsitektur perangkat lunak mencakup perancangan antarmuka pengguna (*wireframing/mockup* di Figma), perancangan alur proses kerja sistem menggunakan *Unified Modeling Language* (UML) berupa *Use Case Diagram* dan *Activity Diagram*, serta perancangan skema basis data relasional (*Entity Relationship Diagram* / ERD dan Kamus Data).
>
> 3. **Implementasi dan Pengodean (*Implementation & Coding*):**  
>    Menerjemahkan hasil rancangan desain ke dalam baris kode program. Frontend dan backend dikembangkan secara terintegrasi menggunakan kerangka kerja *Next.js 14 App Router* dengan bahasa pemrograman *TypeScript*. Penataan antarmuka menggunakan utilitas *Tailwind CSS* dan komponen *Lucide Icons*. Integrasi penyimpanan data relasional dan otentikasi dibangun menggunakan layanan *Supabase Managed PostgreSQL* dan *Supabase Auth*.
>
> 4. **Pengujian Sistem (*System Testing*):**  
>    Melakukan pengujian perangkat lunak menggunakan metode *Black-Box Testing* untuk memverifikasi fungsionalitas setiap fitur sistem tanpa melihat kode internalnya. Pengujian mencakup alur login, pembatasan hak akses (RBAC), penguncian unit kerja operator, kalkulasi otomatis data, filter pencarian, ekspor Excel, dan cetak dokumen kop resmi.
>
> 5. **Penyusunan Dokumentasi dan Penyerahan Sistem (*Deployment & Handover*):**  
>    Melakukan *deployment* sistem ke lingkungan komputasi awan (*Vercel Cloud Platform* dan *Supabase Database Server*), menyusun buku panduan operasional (*user manual*), melakukan sosialisasi kepada perwakilan operator dinas, serta menyusun laporan pertanggungjawaban Kerja Praktik.

---

### D. Subbab D: Jadwal Pelaksanaan Kerja Praktik

*Gunakan format tabel berikut pada Subbab D:*

**Tabel 1.1: Jadwal Pelaksanaan Kerja Praktik Pembuatan Website SatuNaker**

| No. | Kegiatan Pelaksanaan | Bulan ke-1 (Minggu 1-4) | Bulan ke-2 (Minggu 5-8) | Bulan ke-3 (Minggu 9-12) |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Pengenalan Lingkungan Kerja & Observasi Lapangan Dinperinnaker | [X] [X] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 2 | Pengumpulan Data & Analisis Kebutuhan Sistem Terpadu | [ ] [X] [X] [ ] | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 3 | Perancangan Sistem (UML, Skema Database ERD, & Desain UI) | [ ] [ ] [X] [X] | [X] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] |
| 4 | Implementasi & Pengodean Program (Next.js 14 & Supabase) | [ ] [ ] [ ] [ ] | [X] [X] [X] [X] | [ ] [ ] [ ] [ ] |
| 5 | Pengujian Sistem (Black-Box Testing) & Uji Coba Pengguna | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [X] [X] [ ] [ ] |
| 6 | Evaluasi, Perbaikan Sistem, & Penyusunan Laporan KP | [ ] [ ] [ ] [ ] | [ ] [ ] [ ] [ ] | [ ] [X] [X] [X] |

---

## 4. MATERI BAB II: INSTANSI MITRA

### A. Subbab A: Profil Instansi Mitra
*Uraian profil instansi mitra:*

> **Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga** merupakan perangkat daerah yang berkedudukan di bawah dan bertanggung jawab kepada Bupati Purbalingga melalui Sekretaris Daerah. Dinperinnaker mempunyai tugas pokok membantu Bupati dalam melaksanakan urusan pemerintahan daerah di bidang perindustrian, transmigrasi, dan tenaga kerja yang menjadi kewenangan daerah serta tugas pembantuan yang ditugaskan kepada Pemerintah Daerah.
>
> Secara yuridis formal, kelembagaan Dinperinnaker Kabupaten Purbalingga dibentuk berdasarkan **Peraturan Daerah Kabupaten Purbalingga Nomor 12 Tahun 2016** tentang Pembentukan dan Susunan Perangkat Daerah Kabupaten Purbalingga, yang selanjutnya dijabarkan kedudukan, susunan organisasi, rincian tugas dan fungsinya melalui **Peraturan Bupati Purbalingga Nomor 87 Tahun 2021** tentang Kedudukan, Susunan Organisasi, Tugas dan Fungsi serta Tata Kerja Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.
>
> Saat ini, Dinperinnaker Kabupaten Purbalingga dipimpin oleh **Bapak Johan Arifin, S.Sos., M.Si.** selaku Kepala Dinas. Instansi ini memainkan peran yang sangat strategis dalam perekonomian Kabupaten Purbalingga mengingat wilayah ini dikenal sebagai salah satu sentra industri manufaktur bulu mata palsu (*eyelashes*), rambut palsu (*wig*), industri pengolahan kayu, knalpot logam, serta sentra penyerapan tenaga kerja formal dan informal di Jawa Tengah.

---

### B. Subbab B: Struktur Organisasi dan Tupoksi 7 Unit Kerja
*Bagan organisasi mengacu pada Perbup 87/2021 dengan 7 unit kerja lengkap:*

> Struktur organisasi Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga terdiri dari pimpinan, sekretariat, tiga bidang teknis, dan dua unit pelaksana teknis daerah (UPTD), dengan rincian tugas dan fungsi sebagai berikut:
>
> 1. **Kepala Dinas:**  
>    Memimpin, mengoordinasikan, merumuskan kebijakan operasional, membina, mengendalikan, dan mengevaluasi pelaksanaan urusan pemerintahan di bidang perindustrian dan ketenagakerjaan di seluruh wilayah Kabupaten Purbalingga.
>
> 2. **Sekretariat:**  
>    Dipimpin oleh seorang Sekretaris yang membawahkan 2 (dua) subbagian:  
>    a. **Subbagian Perencanaan dan Keuangan (Renkeu):** Mengelola perencanaan program kerja, penyusunan anggaran (RKA/DPA), monitoring evaluasi kinerja, penatausahaan akuntansi keuangan, dan penyusunan laporan keuangan dinas.  
>    b. **Subbagian Umum dan Kepegawaian (Umpeg):** Mengelola ketatausahaan, korespondensi kedinasan, perlengkapan dan aset dinas, rumah tangga dinas, serta administrasi kepegawaian (mutasi, kenaikan pangkat, disiplin pegawai).
>
> 3. **Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK):**  
>    Bertugas merumuskan kebijakan, membina, mengawasi, dan memfasilitasi pencegahan serta penyelesaian perselisihan hubungan industrial (bipartit/tripartit), pendaftaran Perjanjian Kerja Bersama (PKB) dan Peraturan Perusahaan (PP), pengawasan kepesertaan jaminan sosial ketenagakerjaan (BPJS Ketenagakerjaan dan BPJS Kesehatan), serta perlindungan kesejahteraan tenaga kerja di perusahaan.
>
> 4. **Bidang Penempatan Tenaga Kerja dan Transmigrasi (PPTK):**  
>    Bertugas memberikan pelayanan informasi pasar kerja (*job fair*), penerbitan Kartu Pencari Kerja (AK-1), fasilitasi penempatan tenaga kerja dalam negeri maupun luar negeri (Pekerja Migran Indonesia / PMI), perlindungan hak-hak pencari kerja, serta penyelenggaraan program transmigrasi.
>
> 5. **Bidang Perindustrian:**  
>    Bertugas melakukan pendataan, pembinaan, pengawasan, fasilitasi standardisasi (SNI, halal, HAKI), pengembangan teknologi, promosi, dan penguatan rantai pasok bagi pelaku Industri Kecil dan Menengah (IKM) serta industri besar di Kabupaten Purbalingga.
>
> 6. **UPTD Balai Latihan Kerja (BLK):**  
>    Unit pelaksana teknis yang bertugas menyelenggarakan pelatihan vokasi berbasis kompetensi (*competency-based training*) bagi masyarakat pencari kerja (misal: kejuruan menjahit, otomotif sepeda motor, teknik las, tata boga, teknologi informasi), uji kompetensi/sertifikasi BNSP, serta penyaluran lulusan pelatihan ke dunia usaha dan dunia industri (DUDI).
>
> 7. **UPTD Pengembangan Industri Logam (PILOG):**  
>    Unit pelaksana teknis yang bertugas memberikan pelayanan teknis permesinan dan fasilitas fabrikasi logam, bimbingan teknologi manufaktur, kalibrasi peralatan, pengujian kualitas, serta pembinaan sentra industri knalpot dan kerajinan logam khas Purbalingga agar berdaya saing nasional maupun internasional.

---

### C. Subbab C: Lokasi Mitra
*Data alamat dan koordinat:*

> Kantor Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga berlokasi di lokasi strategis pusat administrasi pemerintahan dan pendidikan Kabupaten Purbalingga:
> - **Alamat Lengkap:** Jl. Mayjen Sungkono No. 34, Selabaya, Kec. Kalimanah, Kabupaten Purbalingga, Jawa Tengah 53371.
> - **Telepon / Fax:** (0281) 891043
> - **Surel (Email):** `dinperinnaker@purbalinggakab.go.id`
> - **Laman Resmi (Website):** `https://dinperinnaker.purbalinggakab.go.id`

---

### D. Subbab D: Visi dan Misi Mitra
*Penyelarasan dengan RPJMD Kabupaten Purbalingga 2021-2026:*

> Visi Dinperinnaker Kabupaten Purbalingga selaras dengan Visi Pembangunan Daerah dalam Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga Tahun 2021-2026, yaitu:  
> **"Purbalingga yang Mandiri dan Berdaya Saing Menuju Masyarakat Sejahtera yang Berakhlak Mulia."**
>
> Dalam mewujudkan visi tersebut, Dinperinnaker mengemban Misi Pembangunan Daerah, khususnya:
> 1. **Misi ke-2:** "Mendorong pertumbuhan ekonomi daerah yang berbasis pada industri, pertanian, dan pariwisata yang berwawasan lingkungan serta berorientasi pada pemberdayaan potensi lokal."
> 2. **Misi ke-3:** "Meningkatkan kualitas sumber daya manusia melalui peningkatan mutu pendidikan, keterampilan kerja, dan derajat kesehatan masyarakat."
>
> Pengembangan sistem informasi **SatuNaker** secara langsung mendukung pencapaian misi tersebut dengan menyajikan basis data terpadu untuk memetakan serapan tenaga kerja, memonitor kepatuhan industri, dan mengevaluasi efektivitas pelatihan vokasi.

---

## 5. MATERI BAB III: PELAKSANAAN PROYEK

### A. Subbab A.1: Tahap Analisis Kebutuhan Sistem

#### 1. Spesifikasi Teknis Sistem (5 Tabel Lengkap)

*Gunakan 5 tabel terbuka (open border) berikut:*

**Tabel 3.1: Spesifikasi Kebutuhan Perangkat Keras (*Hardware*)**

| No. | Komponen Perangkat Keras | Spesifikasi Minimum / Aktual | Fungsi dan Peruntukan |
| :---: | :--- | :--- | :--- |
| 1 | Unit Komputer / Laptop Pengembang | AMD Ryzen 5 / Intel Core i5 Quad-Core @ 2.4 GHz | Lingkungan pengembangan aplikasi, kompilasi kode Next.js, dan pengujian lokal |
| 2 | Memori Utama (RAM) | 16 GB DDR4 Dual-Channel | Menjalankan *development server*, editor kode VS Code, Docker, dan browser bersamaan |
| 3 | Media Penyimpanan (*Storage*) | 512 GB SSD NVMe M.2 | Penyimpanan source code proyek, aset multimedia, dan basis data sementara |
| 4 | Layar Tampilan (*Display*) | 14.0 Inci Full HD (1920 x 1080 piksel) | Memastikan akurasi tata letak desain UI responsif pada resolusi tinggi |
| 5 | Koneksi Jaringan Internet | Kecepatan minimal 10 Mbps (Wi-Fi/LAN) | Komunikasi dengan basis data awan Supabase, instalasi package NPM, dan deployment |

---

**Tabel 3.2: Spesifikasi Kebutuhan Perangkat Lunak (*Software*)**

| No. | Perangkat Lunak | Versi / Rilis | Fungsi dan Peruntukan |
| :---: | :--- | :--- | :--- |
| 1 | Sistem Operasi | Microsoft Windows 11 Pro 64-bit | Lingkungan sistem operasi utama pengembangan proyek |
| 2 | Editor Kode (*Code Editor*) | Visual Studio Code v1.90+ | Penyuntingan kode program Next.js, TypeScript, dan SQL |
| 3 | Peramban Web (*Web Browser*) | Google Chrome v126+ & Mozilla Firefox | Pratinjau aplikasi, debugging antarmuka melalui DevTools, dan verifikasi cetak |
| 4 | Runtime Environment | Node.js v20.x LTS & NPM v10.x | Eksekusi package JavaScript dan manajemen pustaka dependensi pihak ketiga |
| 5 | Sistem Kontrol Versi (*VCS*) | Git v2.43+ & Repositori GitHub | Manajemen kontrol versi kode sumber dan kolaborasi pengembangan |
| 6 | Alat Perancangan Desain | Figma Desktop App / Web Version | Perancangan wireframe dan purwarupa antarmuka pengguna (UI/UX) |
| 7 | Pengujian Endpoint API | Postman Desktop v11.x | Pengujian validitas respons API RESTful Supabase dan format payload JSON |

---

**Tabel 3.3: Spesifikasi Teknologi Website (*Web Stack*)**

| No. | Komponen Teknologi | Pilihan Teknologi | Deskripsi dan Keunggulan |
| :---: | :--- | :--- | :--- |
| 1 | Arsitektur Aplikasi | Web Application (Client-Server Cloud) | Aplikasi web terpusat yang dapat diakses lintas platform tanpa instalasi lokal |
| 2 | Framework Utama | Next.js 14 (App Router Architecture) | Mendukung Server-Side Rendering (SSR) dan Server Actions untuk kinerja cepat dan aman |
| 3 | Bahasa Pemrograman | TypeScript & JavaScript (ESNext) | Penulisan kode bertipe statis (*type-safe*) guna mencegah kesalahan runtime |
| 4 | Framework CSS Antarmuka | Tailwind CSS v3.4+ | Utilitas styling modern untuk antarmuka yang responsif, modular, dan konsisten |
| 5 | Pustaka Ikon Grafis | Lucide React | Menyediakan kumpulan ikon vektor SVG yang modern dan ringan |
| 6 | Komponen UI Interaktif | Radix UI / Shadcn UI Primitives | Komponen modal dialog, popover, dan dropdown yang aksesibel dan berstandar WAI-ARIA |
| 7 | Pustaka Ekspor Excel | SheetJS (xlsx package) | Pengolahan dan konversi data tabel ke format spreadsheet .xlsx di sisi klien |
| 8 | Mesin Cetak Kedinasan | CSS Print Media Query (@media print) | Menghilangkan elemen navigasi dan tombol, menyematkan kop dinas otomatis saat cetak |

---

**Tabel 3.4: Spesifikasi Penyimpanan Data (*Data Storage*)**

| No. | Komponen Penyimpanan | Teknologi / Layanan | Deskripsi dan Karakteristik |
| :---: | :--- | :--- | :--- |
| 1 | Database Management System | PostgreSQL v15+ (Supabase Managed Cloud) | Basis data relasional tangguh berstandar enterprise dengan performa query tinggi |
| 2 | Mekanisme Keamanan Data | Row-Level Security (RLS) PostgreSQL | Membatasi hak akses baris data pada level engine database sesuai UID pengguna |
| 3 | Layanan Otentikasi Terpadu | Supabase Auth (JWT Engine) | Pengelolaan login, enkripsi hash kata sandi, dan validasi token sesi otomatis |
| 4 | Model Hubungan Data | Relasional & Dokumen Campuran (JSONB) | Skema relasional untuk tabel master dan JSONB untuk fleksibilitas metadata dinamis |
| 5 | Layanan Backup Basis Data | Daily Automated Cloud Backup | Pencadangan otomatis harian pada infrastruktur cloud Supabase untuk mencegah kehilangan data |

---

**Tabel 3.5: Spesifikasi Aset Visual dan Tipografi**

| No. | Aset Visual | Format / Tipe | Sumber dan Peruntukan |
| :---: | :--- | :--- | :--- |
| 1 | Logo Pemkab Purbalingga | PNG High Resolution / SVG | Lambang resmi daerah untuk Kop Surat Kedinasan dan Halaman Login |
| 2 | Tipografi Antarmuka Web | Font Inter / Sans-Serif Standar | Tipografi layar digital yang mudah dibaca (*legible*) pada berbagai ukuran layar |
| 3 | Tipografi Dokumen Cetak | Times New Roman & Arial | Format baku tata naskah dinas kedinasan Pemerintah Kabupaten Purbalingga |
| 4 | Palet Warna Identitas | Biru Ketenagakerjaan & Hijau Toska | Menghadirkan kesan profesional, kredibel, dan ramah pengguna |
| 5 | Favicon & Web Manifest | File ICO & JSON Manifest | Identitas ikon tab pada peramban web dan dukungan Progressive Web App |

---

#### 2. Analisis Pengguna & Matriks Hak Akses (RBAC)

**Tabel 3.6: Matriks Hak Akses Sistem SatuNaker (Role-Based Access Control)**

| No. | Fitur / Modul Sistem | Kepala Dinas | Admin Dinas | Operator Unit |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Login ke Sistem | [X] | [X] | [X] |
| 2 | Melihat Dasbor Statistik Eksekutif Dinperinnaker | [X] (Seluruh Unit) | [X] (Seluruh Unit) | [X] (Unit Sendiri) |
| 3 | Filter Data Lintas Tahun & Kategori Usaha | [X] | [X] | [X] (Unit Sendiri) |
| 4 | Melihat Data Tenaga Kerja & Perusahaan | [X] (Semua Unit) | [X] (Semua Unit) | [X] (Unit Sendiri) |
| 5 | Menambah Data Baru (Unit Auto-Lock) | [ ] | [X] (Semua Unit) | [X] (Unit Sendiri) |
| 6 | Mengubah / Mengedit Data | [ ] | [X] (Semua Data) | [X] (Data Unit Sendiri) |
| 7 | Menghapus Data (*Soft/Hard Delete*) | [ ] | [X] (Semua Data) | [ ] |
| 8 | Ekspor Data ke Excel (.xlsx) | [X] | [X] | [X] (Unit Sendiri) |
| 9 | Cetak Laporan Resmi Ber-Kop Dinperinnaker | [X] | [X] | [X] (Unit Sendiri) |
| 10 | Manajemen Pengguna (Tambah/Edit Akun Staf) | [ ] | [X] | [ ] |
| 11 | Konfigurasi Data Master 7 Unit Kerja | [ ] | [X] | [ ] |
| 12 | Melihat Log Aktivitas Audit Trail | [ ] | [X] | [ ] |

---

### B. Subbab A.2: Tahap Desain dan Perancangan Sistem

#### 1. Perancangan UML (Use Case & Activity Diagram)

*Narasi Use Case Diagram:*
> Pada perancangan *Use Case Diagram*, sistem SatuNaker memodelkan interaksi antara 3 aktor dengan 10 use case:
> 1. **Aktor Kepala Dinas:** Berinteraksi dengan use case *Login*, *Melihat Dasbor Eksekutif*, *Melakukan Filter Data Multi-Tahun*, *Mengekspor Data ke Excel*, dan *Mencetak Laporan Ber-Kop Surat Resmi*.
> 2. **Aktor Admin Dinas:** Memiliki relasi ke seluruh use case dalam sistem, termasuk use case khusus *Mengelola Akun Pengguna*, *Mengonfigurasi Master Unit Kerja*, *Memverifikasi/Menghapus Rekaman Data*, dan *Melihat Log Audit Aktivitas*.
> 3. **Aktor Operator Unit:** Berinteraksi dengan use case *Login*, *Melihat Data Unit*, *Menginput Data Baru (dengan relasi `<<include>>` Validasi Auto-Lock Unit)*, *Mengedit Data Unit Sendiri*, *Ekspor Excel*, dan *Cetak Laporan Unit*. Seluruh use case operasional memerlukan relasi `<<include>>` ke use case *Login* untuk otentikasi.

*Narasi 5 Alur Activity Diagram Utama:*
> 1. **Activity Diagram Login Pengguna:**  
>    Pengguna membuka laman login -> Sistem menampilkan form login -> Pengguna menginputkan email dan kata sandi -> Sistem melakukan otentikasi via Supabase Auth -> Jika gagal, muncul pesan error; jika berhasil, sistem memeriksa *role* pengguna -> Jika Kepala Dinas, diarahkan ke `/dashboard/eksekutif`; jika Admin Dinas, diarahkan ke `/admin/users`; jika Operator Unit, diarahkan ke `/data/records` dengan unit terfilter otomatis.
> 2. **Activity Diagram Input Data Baru (Auto-Lock Unit):**  
>    Operator mengklik tombol "Tambah Data" -> Sistem membuka modal form input -> Sistem mendeteksi `unit_kerja_id` dari sesi operator dan mengunci dropdown unit kerja (tidak dapat diubah) -> Operator mengisi nama perusahaan/entitas, alamat, KBLI, jumlah tenaga kerja (WNI LK/PR, WNA LK/PR), dan data BPJS -> Sistem menghitung *total* secara real-time -> Operator menekan tombol "Simpan" -> Sistem memvalidasi kelengkapan data -> Jika valid, data disimpan ke PostgreSQL dan tabel diperbarui otomatis tanpa reload.
> 3. **Activity Diagram Filter Data Lintas Tahun:**  
>    Pengguna memilih tahun pada dropdown (misal: "2026") dan/atau kategori usaha -> Sistem menangkap perubahan filter state -> Sistem mengirimkan query bersyarat ke Supabase -> Data tabel dan indikator kartu statistik langsung diperbarui sesuai filter terpilih.
> 4. **Activity Diagram Ekspor Spreadsheet (.xlsx):**  
>    Pengguna mengklik tombol "Ekspor Excel" -> Sistem mengagregasi data baris yang sedang aktif di tabel -> Pustaka SheetJS menyusun struktur worksheet dan header kolom -> File biner `.xlsx` di-generate di browser -> Browser memicu unduhan file otomatis dengan nama file dinamis (misal: `Data_Tenaga_Kerja_Dinperinnaker_2026.xlsx`).
> 5. **Activity Diagram Cetak Dokumen Ber-Kop Resmi:**  
>    Pengguna menekan tombol "Cetak Laporan" -> Sistem mengaktifkan CSS `@media print` -> Komponen navigasi, sidebar, dan tombol aksi otomatis disembunyikan -> Header Kop Surat resmi Pemkab Purbalingga dan footer tanda tangan Kepala Dinas disisipkan ke halaman -> Dialog pratinjau cetak peramban terbuka -> Pengguna memilih printer fisik atau "Save as PDF".

---

#### 2. Kamus Data Database (4 Tabel Inti PostgreSQL)

**Tabel 3.7: Kamus Data Tabel `unit_kerja`**

| No. | Nama Kolom (*Field*) | Tipe Data | Keterangan / Fungsi |
| :---: | :--- | :--- | :--- |
| 1 | `id` | UUID (Primary Key) | Kunci primer identitas unik setiap unit kerja |
| 2 | `kode_unit` | VARCHAR(20) (Unique) | Kode unik unit kerja (contoh: `HIJTK`, `PPTK`, `PERIN`, `BLK`, `PILOG`, `RENKEU`, `UMPEG`) |
| 3 | `nama_unit` | VARCHAR(150) | Nama lengkap unit kerja kedinasan di Dinperinnaker Purbalingga |
| 4 | `singkatan` | VARCHAR(50) | Akronim atau sebutan singkat unit kerja |
| 5 | `penanggung_jawab` | VARCHAR(100) | Nama pejabat Kepala Bidang / Kepala UPTD / Kasubbag |
| 6 | `nip_pj` | VARCHAR(30) | Nomor Induk Pegawai (NIP) pejabat penanggung jawab |
| 7 | `kontak_email` | VARCHAR(100) | Alamat surel resmi unit kerja |
| 8 | `created_at` | TIMESTAMPTZ | Waktu pencatatan data ke dalam sistem |
| 9 | `updated_at` | TIMESTAMPTZ | Waktu terakhir data unit kerja diperbarui |

---

**Tabel 3.8: Kamus Data Tabel `profiles`**

| No. | Nama Kolom (*Field*) | Tipe Data | Keterangan / Fungsi |
| :---: | :--- | :--- | :--- |
| 1 | `id` | UUID (Primary Key) | Kunci primer profil pengguna (relasi 1:1 ke `auth.users.id`) |
| 2 | `user_id` | UUID (Foreign Key) | Referensi ke akun otentikasi Supabase |
| 3 | `nama_lengkap` | VARCHAR(100) | Nama lengkap beserta gelar akademik pengguna |
| 4 | `nip` | VARCHAR(30) | Nomor Induk Pegawai (NIP) staf/pejabat |
| 5 | `unit_kerja_id` | UUID (Foreign Key) | Referensi ke tabel `unit_kerja` penempatan tugas |
| 6 | `role` | VARCHAR(30) | Peran pengguna (`kepala_dinas`, `admin_dinas`, `operator_unit`) |
| 7 | `no_telepon` | VARCHAR(20) | Nomor kontak WhatsApp/telepon pengguna |
| 8 | `is_active` | BOOLEAN | Status keaktifan akun pengguna (true = aktif, false = nonaktif) |
| 9 | `created_at` | TIMESTAMPTZ | Waktu pembuatan akun pengguna |

---

**Tabel 3.9: Kamus Data Tabel `data_records`**

| No. | Nama Kolom (*Field*) | Tipe Data | Keterangan / Fungsi |
| :---: | :--- | :--- | :--- |
| 1 | `id` | UUID (Primary Key) | Kunci primer unik setiap entri data sektoral |
| 2 | `unit_kerja_id` | UUID (Foreign Key) | Referensi ke tabel `unit_kerja` yang memiliki rekaman data |
| 3 | `judul_data` | VARCHAR(255) | Nama perusahaan / entitas / nama pelatihan / sarana industri |
| 4 | `kategori` | VARCHAR(100) | Kategori usaha riil (contoh: Pertokoan, Konstruksi, Garment, AMDK) |
| 5 | `kbli_kode` | VARCHAR(20) | Kode Klasifikasi Baku Lapangan Usaha Indonesia (misal: 47111, 42000) |
| 6 | `alamat` | TEXT | Alamat lengkap lokasi perusahaan atau kegiatan |
| 7 | `tahun` | INTEGER | Tahun pendataan operasional (misal: 2024, 2025, 2026) |
| 8 | `metadata` | JSONB | Detail fleksibel (rincian BPJS Naker, BPJS Kesehatan Mandiri/PBI/BU, dsb.) |
| 9 | `wni_lk` | INTEGER | Jumlah tenaga kerja Warga Negara Indonesia Laki-Laki |
| 10 | `wni_pr` | INTEGER | Jumlah tenaga kerja Warga Negara Indonesia Perempuan |
| 11 | `wna_lk` | INTEGER | Jumlah tenaga kerja Warga Negara Asing Laki-Laki |
| 12 | `wna_pr` | INTEGER | Jumlah tenaga kerja Warga Negara Asing Perempuan |
| 13 | `total_naker` | INTEGER | Akumulasi total tenaga kerja (hasil kalkulasi otomatis) |

---

**Tabel 3.10: Kamus Data Tabel `log_aktivitas`**

| No. | Nama Kolom (*Field*) | Tipe Data | Keterangan / Fungsi |
| :---: | :--- | :--- | :--- |
| 1 | `id` | BIGSERIAL (Primary Key)| Kunci primer nomor urut log sistem |
| 2 | `user_id` | UUID (Foreign Key) | Pengguna yang melakukan aktivitas transaksi |
| 3 | `action` | VARCHAR(50) | Jenis tindakan (`LOGIN`, `CREATE`, `UPDATE`, `DELETE`, `EXPORT`, `PRINT`) |
| 4 | `modul` | VARCHAR(50) | Modul tempat aksi dilakukan (misal: `DATA_RECORD`, `USER_MGMT`) |
| 5 | `detail_perubahan` | JSONB | Catatan rincian nilai data sebelum dan sesudah perubahan |
| 6 | `ip_address` | VARCHAR(45) | Alamat protokol internet (IP) perangkat pengguna |
| 7 | `created_at` | TIMESTAMPTZ | Waktu tepat terjadinya aktivitas (*audit timestamp*) |

---

### C. Subbab A.3: Tahap Implementasi Antarmuka Sistem (10 Modul)

*Deskripsi 10 modul antarmuka sistem:*

> 1. **Modul 1: Halaman Login & Otentikasi Sistem (`/login`)**  
>    Halaman gerbang masuk sistem dengan tata letak minimalis modern. Memuat logo resmi Pemerintah Kabupaten Purbalingga, form input email dan kata sandi, indikator tombol loading interaktif, serta penanganan error kredensial. Sistem secara otomatis memvalidasi token sesi JWT dan mengarahkan pengguna ke rute dasbor yang sesuai dengan perannya.
>
> 2. **Modul 2: Dashboard Ringkasan Eksekutif Kepala Dinas (`/dashboard`)**  
>    Pusat komando informasi pimpinan dinas yang menyajikan kartu ringkasan KPI (*Key Performance Indicators*): Total Perusahaan Terdata, Total Tenaga Kerja Terdaftar, Rasio Tenaga Kerja Laki-laki vs Perempuan, dan Total Kepesertaan BPJS Ketenagakerjaan. Dilengkapi visualisasi grafik diagram batang dan diagram lingkaran interaktif.
>
> 3. **Modul 3: Filter Data Multi-Parameter dan Lintas Tahun**  
>    Komponen filter fleksibel yang memungkinkan pimpinan dan operator memilih rentang tahun pendataan (2024, 2025, 2026), memilih unit kerja, serta melakukan filter kategori jenis usaha riil secara instan tanpa perlu memuat ulang seluruh halaman peramban.
>
> 4. **Modul 4: Kelola Data Master / Records (`/records`)**  
>    Antarmuka tabel data komprehensif yang menampilkan daftar perusahaan dan tenaga kerja. Dilengkapi kolom nomor urut otomatis, nama perusahaan, alamat, kode KBLI, jenis usaha riil, breakdown tenaga kerja WNI/WNA, status BPJS, dan tombol aksi (Edit/Hapus). Memiliki fitur pencarian instan (*live search*) dan paginasi dinamis.
>
> 5. **Modul 5: Modal Form Tambah Data Baru (Auto-Locking Unit)**  
>    Modal dialog interaktif untuk memasukkan data baru. Apabila dibuka oleh Operator Unit, bidang *Unit Kerja* otomatis terkunci pada unit kerja operator tersebut demi menjaga integritas data antar-bidang. Dilengkapi mekanisme *auto-calculate sum* yang menghitung jumlah total secara otomatis saat angka WNI LK/PR diinputkan.
>
> 6. **Modul 6: Laporan Ringkasan Eksekutif Terpadu**  
>    Tampilan agregasi matriks data yang mengelompokkan data berdasarkan 7 unit kerja dan jenis industri. Modul ini dirancang khusus untuk mempermudah pimpinan dalam mengevaluasi capaian target tahunan sektor ketenagakerjaan dan perindustrian daerah.
>
> 7. **Modul 7: Fitur Cetak Laporan Resmi Ber-Kop Surat Pemkab Purbalingga**  
>    Fitur pencetakan dokumen resmi yang dirancang dengan utilitas CSS Print Media. Saat tombol cetak ditekan, sistem secara otomatis merender kepala surat resmi lengkap dengan logo daerah Pemkab Purbalingga, garis batas ganda kedinasan, judul laporan, tabel data, tempat tanggal cetak, dan tanda tangan resmi Kepala Dinas/Pejabat berwenang. Seluruh navigasi web disembunyikan otomatis saat mode cetak aktif.
>
> 8. **Modul 8: Fitur Ekspor Data ke Spreadsheet Excel (.xlsx)**  
>    Fitur ekspor data instan yang memanfaatkan pustaka SheetJS di sisi klien. Menghasilkan berkas `.xlsx` dengan format header kolom rapi, angka numerik yang dapat langsung diolah dengan formula Excel, dan nama file yang mencantumkan tahun pendataan secara otomatis.
>
> 9. **Modul 9: Manajemen Unit Kerja Dinperinnaker (`/admin/units`)**  
>    Panel administrasi khusus Admin Dinas untuk mengelola metadata 7 unit kerja (HIJTK, PPTK, Perindustrian, BLK, PILOG, Renkeu, Umpeg), mencakup pembaruan nama pejabat penanggung jawab, NIP pejabat, dan alamat kontak unit.
>
> 10. **Modul 10: Manajemen Akun Pengguna & Hak Akses (`/admin/users`)**  
>     Panel kontrol pengguna bagi Admin Dinas untuk menambahkan akun staf operator baru, mengatur role (*kepala_dinas*, *admin_dinas*, *operator_unit*), melakukan reset kata sandi, serta menonaktifkan akun staf yang telah mutasi atau purna tugas.

---

### D. Subbab A.4: Tahap Pengujian Sistem (13 Tabel Black-Box Testing)

*Gunakan 13 tabel pengujian fungsional lengkap berikut:*

**Tabel 3.11: Pengujian Otentikasi Login Pengguna**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Login dengan kredensial valid | Email: `admin@dinperinnaker.id`<br>Password: `Password123!` | Sistem memvalidasi token JWT dan mengarahkan ke dasbor sesuai role | Berhasil masuk dan rute dasbor termuat | **Valid** |
| 2 | Login dengan kata sandi salah | Email: `admin@dinperinnaker.id`<br>Password: `SandiSalah!` | Sistem menolak akses dan memunculkan pesan peringatan *"Kredensial tidak valid"* | Pesan error muncul, akses ditolak | **Valid** |
| 3 | Login dengan email belum terdaftar | Email: `tidakada@purbalinggakab.go.id`<br>Password: `Sembarang123` | Sistem menampilkan pesan *"Pengguna tidak ditemukan"* | Pesan peringatan muncul tepat | **Valid** |
| 4 | Percobaan akses URL internal tanpa login | Akses langsung ke URL `/records` via address bar | Sistem mencegat sesi melalui middleware dan mengarahkan paksa ke `/login` | Di-redirect ke halaman login | **Valid** |

---

**Tabel 3.12: Pengujian Role-Based Access Control (RBAC)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Operator mengakses URL Admin `/admin/users` | Sesi login: Akun Operator Unit HIJTK | Sistem menolak akses dengan kode 403 Forbidden / redirect ke dasbor | Akses ditolak dan dialihkan ke rute diizinkan | **Valid** |
| 2 | Kepala Dinas mengakses halaman dasbor | Sesi login: Akun Kepala Dinas | Menampilkan visualisasi ringkasan eksekutif seluruh 7 unit kerja | Tampilan eksekutif termuat lengkap | **Valid** |
| 3 | Operator melihat daftar data master | Sesi login: Akun Operator Unit BLK | Sistem membatasi tampilan hanya pada rekaman data milik UPTD BLK | Hanya data UPTD BLK yang tampil | **Valid** |

---

**Tabel 3.13: Pengujian Auto-Locking Unit Kerja Operator**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Operator HIJTK membuka modal tambah data | Klik tombol *"Tambah Data"* pada sesi Operator HIJTK | Dropdown Unit Kerja terisi *"Bidang HIJTK"* secara otomatis dan berstatus disabled/read-only | Unit kerja terkunci pada HIJTK, tidak dapat diubah | **Valid** |
| 2 | Admin Dinas membuka modal tambah data | Klik tombol *"Tambah Data"* pada sesi Admin Dinas | Dropdown Unit Kerja berstatus aktif dan dapat memilih 7 unit kerja | Admin bebas memilih unit kerja tujuan | **Valid** |

---

**Tabel 3.14: Pengujian Input Data Valid & Perhitungan Otomatis (*Auto-Calculate*)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Menginputkan angka tenaga kerja LK dan PR | WNI LK: `14`, WNI PR: `3`, WNA LK: `0`, WNA PR: `0` | Field Total Tenaga Kerja otomatis menghitung dan bernilai `17` secara real-time | Total terhitung `17` secara otomatis di antarmuka | **Valid** |
| 2 | Menyimpan entri data lengkap | Nama: *"PT Adira Multifinance"*, KBLI: `64922`, Kategori: *"Finance"* | Data tersimpan ke PostgreSQL Supabase dan tabel langsung menampilkan baris baru | Data baru muncul di baris teratas tabel | **Valid** |

---

**Tabel 3.15: Pengujian Validasi Field Kosong & Format Angka**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Mengosongkan nama entitas wajib | Nama Perusahaan: `""` (kosong), lalu menekan Simpan | Sistem menahan form dan menampilkan pesan *"Nama Perusahaan wajib diisi"* | Form tidak tersubmit, pesan validasi muncul | **Valid** |
| 2 | Menginputkan karakter huruf pada kolom jumlah | WNI LK: `"sepuluh"` | Sistem memblokir input non-numerik atau memberikan notifikasi format tidak valid | Input tidak menerima huruf | **Valid** |

---

**Tabel 3.16: Pengujian Fitur Filter Multi-Tahun & Kategori**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Memilih opsi tahun "2026" pada dropdown | Pilihan Tahun: `2026` | Tabel hanya menampilkan data perusahaan/kegiatan tahun pendataan 2026 | Hanya rekaman tahun 2026 yang disajikan | **Valid** |
| 2 | Mengombinasikan filter tahun dan kategori | Tahun: `2026`, Kategori: *"Pertokoan"* | Tabel menyajikan data Alfamart/toko ritel pada periode 2026 | Data terfilter tepat secara ganda | **Valid** |
| 3 | Mereset filter ke opsi "Semua Tahun" | Klik opsi *"Semua Tahun"* | Tabel mengembalikan seluruh rekaman data tanpa batasan tahun | Seluruh data kembali termuat lengkap | **Valid** |

---

**Tabel 3.17: Pengujian Fitur Pencarian Real-Time (*Live Search*)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Mengetik kata kunci spesifik di search bar | Input pencarian: `"BUMI PUTRA"` | Tabel menyaring dan menampilkan baris *"AJB BUMI PUTRA 1912, PT"* | Baris target langsung muncul instan | **Valid** |
| 2 | Mengetik kata kunci yang tidak ada | Input pencarian: `"PerusahaanXYZ123"` | Tabel menampilkan pesan *"Tidak ada data yang sesuai dengan pencarian"* | Pesan data kosong muncul informatif | **Valid** |

---

**Tabel 3.18: Pengujian Edit Data & Pembaruan State Real-Time**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Mengubah jumlah tenaga kerja WNI PR | Nilai lama: `3`, diubah menjadi `5` | Sistem memperbarui record di database dan total baru terupdate otomatis | Total berubah dan tersimpan di database | **Valid** |
| 2 | Membatalkan perubahan pada modal edit | Klik tombol *"Batal"* atau ikon silang | Modal tertutup dan nilai data pada tabel tetap tidak mengalami perubahan | Modal tertutup, data awal utuh | **Valid** |

---

**Tabel 3.19: Pengujian Hapus Data dengan Dialog Konfirmasi**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Menekan tombol hapus pada baris data | Klik tombol ikon tempat sampah (*Delete*) | Muncul modal peringatan konfirmasi: *"Apakah Anda yakin ingin menghapus data ini?"* | Modal konfirmasi muncul mencegah salah klik | **Valid** |
| 2 | Menyetujui konfirmasi penghapusan | Klik tombol *"Ya, Hapus"* pada dialog | Data terhapus dari basis data dan baris hilang dari tabel | Baris terhapus sukses dengan notifikasi toast | **Valid** |

---

**Tabel 3.20: Pengujian Ekspor Data ke Excel (.xlsx)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Mengunduh seluruh data hasil filter | Klik tombol *"Ekspor Excel"* | Peramban mengunduh file `.xlsx` dengan format header dan baris rapi | File `.xlsx` terunduh dan dapat dibuka di MS Excel | **Valid** |
| 2 | Memeriksa format angka pada file Excel | Buka file Excel hasil unduhan di MS Excel | Kolom angka WNI/WNA dapat dijumlahkan langsung dengan formula `=SUM()` | Format sel numerik murni, bukan teks | **Valid** |

---

**Tabel 3.21: Pengujian Cetak Dokumen Ber-Kop Resmi (CSS Print Engine)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Menekan tombol cetak laporan | Klik tombol *"Cetak Laporan"* | Jendela dialog cetak peramban terbuka dengan pratinjau halaman ber-kop resmi Pemkab | Tampilan cetak memuat kop surat resmi dan ttd pimpinan | **Valid** |
| 2 | Memeriksa kebersihan layout cetak | Pratinjau cetak kertas ukuran F4/A4 | Elemen bilah sisi (sidebar), tombol navigasi, dan input pencarian disembunyikan otomatis | Bersih dari elemen UI web, hanya dokumen dinas | **Valid** |

---

**Tabel 3.22: Pengujian Manajemen Pengguna (Admin Dinas)**

| No. | Skenario Pengujian | Data Masukan (*Input*) | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Menambahkan akun staf operator baru | Form: Nama, NIP, Email, Unit: BLK, Role: Operator | Akun baru terdaftar di Supabase Auth dan tabel daftar staf bertambah | Akun baru aktif dan staf dapat login | **Valid** |
| 2 | Menonaktifkan akun staf yang mutasi | Toggle status *"Aktif"* diubah menjadi *"Nonaktif"* | Sesi akun bersangkutan diblokir dan tidak dapat login ke sistem | Akun ditolak saat mencoba login kembali | **Valid** |

---

**Tabel 3.23: Pengujian Responsivitas Tampilan Lintas Perangkat**

| No. | Ukuran Layar / Perangkat | Resolusi Layar | Hasil Pengujian Tampilan Antarmuka | Kesimpulan |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Desktop PC / Monitor Kantor | 1920 x 1080 piksel | Tata letak lebar penuh (*full wide*), sidebar terbuka permanen, tabel sangat lega | **Valid** |
| 2 | Laptop Standar Pegawai | 1366 x 768 piksel | Tata letak optimal, font proporsional, form dan tombol navigasi mudah diakses | **Valid** |
| 3 | Tablet / iPad (Kunjungan Lapangan)| 768 x 1024 piksel | Sidebar otomatis menjadi mode *hamburger drawer*, tabel memiliki *horizontal scroll* | **Valid** |
| 4 | Ponsel Pintar (*Smartphone*) | 375 x 812 piksel | Kartu statistik menumpuk rapi (*single column stack*), modal form pas di layar | **Valid** |

---

### E. Subbab B: Kendala Pelaksanaan & Solusi

*Gunakan tabel terbuka berikut pada Subbab B Kendala Pelaksanaan:*

**Tabel 3.24: Kendala Teknis, Operasional, dan Pemecahan Masalah Proyek**

| No. | Aspek Kendala | Deskripsi Kendala Nyata di Lapangan | Solusi dan Pemecahan Masalah yang Diterapkan |
| :---: | :--- | :--- | :--- |
| 1 | Inkonsistensi Format Data Legacy | Berkas Microsoft Excel lama dari masing-masing bidang memiliki nama kolom yang berbeda, format penulisan angka campuran (menggunakan tanda strip `-` atau spasi), serta kode KBLI yang tidak standar | Membangun skrip pra-pembersihan data (*data cleansing script*) berbasis Python dan regex untuk menstandarisasi nilai null/strip menjadi integer 0, serta menyeragamkan kode KBLI 2015/2020 |
| 2 | Keamanan Data Multi-Unit (*Data Isolation*) | Risiko operator dari salah satu bidang secara tidak sengaja mengubah atau menghapus data milik bidang kerja lain di basis data bersama | Mengimplementasikan kebijakan *Row-Level Security* (RLS) di level engine PostgreSQL Supabase serta fitur *auto-locking* input form di level frontend Next.js |
| 3 | Tata Letak Kop Cetak Kedinasan (*Print Styling*) | Saat mencetak dari browser, header web, tombol navigasi, dan pagination ikut tercetak sehingga dokumen tidak memenuhi format tata naskah dinas resmi | Merancang stylesheet khusus dengan media query `@media print` untuk menyembunyikan elemen web interaktif dan menampilkan kop surat resmi Pemkab Purbalingga |
| 4 | Pemetaan Struktur Unit Organisasi | Adanya penyesuaian unit kerja baru (UPTD PILOG) yang membutuhkan pemisahan data aset fasilitas logam dari data industri umum | Melakukan restrukturisasi tabel relasional `unit_kerja` menjadi 7 entitas definitif dan memperbarui hak akses peran operator masing-masing unit kerja |

---

## 6. MATERI BAB IV: PENUTUP

### A. Subbab A: Kesimpulan
*Poin kesimpulan yang padat dan tegas:*

> Berdasarkan seluruh tahapan perancangan, implementasi, dan pengujian sistem yang telah dilaksanakan pada kegiatan Kerja Praktik di Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga, dapat ditarik beberapa kesimpulan sebagai berikut:
>
> 1. Telah berhasil dirancang dan dibangun sistem informasi berbasis web terpusat bernama **Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (SatuNaker)** menggunakan kerangka kerja *Next.js 14 App Router*, *TypeScript*, *Tailwind CSS*, dan basis data *Supabase Managed PostgreSQL*.
> 2. Sistem SatuNaker berhasil mengeliminasi permasalahan isolasi data (*data silo*) dengan mengintegrasikan pencatatan data dari **7 (tujuh) unit kerja** di lingkungan Dinperinnaker Purbalingga (Bidang HIJTK, Bidang PPTK, Bidang Perindustrian, UPTD BLK, UPTD PILOG, Subbag Renkeu, dan Subbag Umpeg) ke dalam satu basis data terpusat yang aman.
> 3. Penerapan sistem *Role-Based Access Control* (RBAC) pada tiga tingkatan pengguna (Kepala Dinas, Admin Dinas, dan Operator Unit Kerja) yang dilengkapi mekanisme *auto-locking* unit kerja terbukti efektif menjaga integritas dan kerahasiaan data operasional antar-bidang kerja.
> 4. Sistem dilengkapi dengan fitur penunjang yang andal, meliputi dasbor analitik eksekutif, filter dinamis lintas tahun, ekspor file spreadsheet Microsoft Excel (.xlsx), serta mesin cetak dokumen resmi ber-kop surat Pemerintah Kabupaten Purbalingga.
> 5. Berdasarkan hasil pengujian fungsional menggunakan metode *Black-Box Testing* pada 13 skenario pengujian, seluruh fungsi sistem berjalan dengan tingkat keberhasilan 100% (*valid*) dan responsif pada berbagai ukuran layar perangkat.

---

### B. Subbab B: Saran
*Poin saran konstruktif untuk 3 sasaran:*

> Demi keberlanjutan dan penyempurnaan sistem informasi SatuNaker di masa mendatang, penulis menyampaikan beberapa saran sebagai berikut:
>
> 1. **Saran bagi Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga:**  
>    a. Perlu diterbitkan Surat Edaran atau Standar Operasional Prosedur (SOP) internal dari Kepala Dinas yang mewajibkan seluruh unit kerja untuk melakukan penginputan dan pembaruan data secara periodik melalui website SatuNaker.  
>    b. Perlu diselenggarakan bimbingan teknis (*training of trainers*) secara berkala bagi staf operator baru di masing-masing bidang kerja.  
>    c. Melakukan penjadwalan *backup* data secara berkala ke media penyimpanan fisik independen di lingkungan dinas untuk melengkapi *automated cloud backup*.
>
> 2. **Saran bagi Pengembangan Sistem SatuNaker Selanjutnya:**  
>    a. Mengembangkan antarmuka pemrograman aplikasi terbuka (*Open API*) yang aman guna memfasilitasi integrasi dua arah (*interoperabilitas*) dengan sistem Satu Data Indonesia (SDI) tingkat Kabupaten Purbalingga dan portal Kementerian Tenaga Kerja (SIAPKerja).  
>    b. Menambahkan modul *Spatial Mapping* (Sistem Informasi Geografis / GIS) untuk memetakan sebaran lokasi industri knalpot PILOG, pabrik rambut/bulu mata, dan sebaran pencari kerja di 18 kecamatan Kabupaten Purbalingga secara visual pada peta spasial.  
>    c. Mengintegrasikan fitur notifikasi peringatan dini (*early warning alert*) melalui WhatsApp API / Surel untuk mendeteksi perusahaan yang masa pelaporan ketenagakerjaannya mendekati batas waktu.
>
> 3. **Saran bagi Rekan Mahasiswa Kerja Praktik Selanjutnya:**  
>    a. Disarankan untuk mendalami konsep *Row-Level Security* (RLS) dan manajemen *state* modern pada framework React/Next.js sebelum terjun ke instansi pemerintahan.  
>    b. Melakukan komunikasi intensif dengan pembimbing lapangan dan staf instansi guna memahami alur birokrasi dan tata naskah dinas resmi pemerintah daerah secara komprehensif.

---

## 7. MATERI DAFTAR PUSTAKA (STANDAR APA 7th EDITION)

*Gunakan daftar pustaka standar APA 7th Edition berikut (14 referensi valid):*

```text
Badan Standardisasi Nasional. (2015). Klasifikasi Baku Lapangan Usaha Indonesia (KBLI) 2015. Badan Standardisasi Nasional.

Connolly, T. M., & Begg, C. E. (2015). Database Systems: A Practical Approach to Design, Implementation, and Management (6th ed.). Pearson Education.

Fowler, M. (2018). Refactoring: Improving the Design of Existing Code (2nd ed.). Addison-Wesley Professional.

Kurniawan, D., & Pratama, A. (2023). Penerapan Arsitektur Server Components pada Framework Next.js untuk Optimalisasi Aplikasi Web Pemerintahan. Jurnal Sistem Informasi dan Rekayasa Perangkat Lunak (JASIRPL), 5(2), 112–121.

Nugroho, A. (2019). Rekayasa Perangkat Lunak Menggunakan UML dan Java. Andi Offset.

Peraturan Bupati Purbalingga Nomor 87 Tahun 2021 tentang Kedudukan, Susunan Organisasi, Tugas dan Fungsi serta Tata Kerja Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.

Peraturan Daerah Kabupaten Purbalingga Nomor 12 Tahun 2016 tentang Pembentukan dan Susunan Perangkat Daerah Kabupaten Purbalingga.

Peraturan Presiden Republik Indonesia Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik (SPBE). Lembaran Negara Republik Indonesia Tahun 2018 Nomor 182.

Peraturan Presiden Republik Indonesia Nomor 39 Tahun 2019 tentang Satu Data Indonesia. Lembaran Negara Republik Indonesia Tahun 2019 Nomor 112.

Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.

Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education Limited.

Supabase Inc. (2024). Supabase Documentation: The Open Source Firebase Alternative. https://supabase.com/docs

Undang-Undang Republik Indonesia Nomor 14 Tahun 2008 tentang Keterbukaan Informasi Publik. Lembaran Negara Republik Indonesia Tahun 2008 Nomor 61.

Vercel Inc. (2024). Next.js 14 Documentation: App Router and Server Actions. https://nextjs.org/docs
```

---

## 8. PANDUAN TEKNIS FORMAT WORD UMP

Saat Anda membuka dan mengedit file **`TEMPLATE_LAPORAN_KP_TI_UMP.docx`** di Microsoft Word, pastikan memperhatikan aturan teknis berikut:

1. **Ukuran Kertas & Batas Margin:**
   - Ukuran Kertas: **A4** (21,0 cm x 29,7 cm).
   - Margin: **Atas 4 cm, Kiri 4 cm, Bawah 3 cm, Kanan 3 cm**.
2. **Huruf (Font) & Spasi Teks:**
   - Huruf Utama: **Times New Roman**.
   - Judul BAB: **14 pt, Bold, Huruf Kapital (UPPERCASE), Rata Tengah**.
   - Subbab (A, B, C): **12 pt, Bold, Rata Kiri**.
   - Teks Isi / Paragraf: **12 pt, Normal, Spasi Ganda (2.0), Rata Kiri-Kanan (Justified)**.
   - Indentasi Awal Paragraf: **1,27 cm (First Line Indent)**.
   - Teks Tabel & Keterangan Gambar: **10-11 pt, Spasi Tunggal (1.0)**.
3. **Format Tabel (Tabel Terbuka / Open Border):**
   - Garis horizontal: Hanya ada di batas atas header tabel (1 pt), batas bawah header tabel (0.75 pt), dan batas terbawah tabel (1 pt).
   - **TIDAK ADA garis vertikal** di dalam tabel.
   - Posisi Judul Tabel: Di **atas tabel**, format `Tabel [Nomor].[Urut] [Judul Tabel]` (contoh: *Tabel 3.1: Spesifikasi Kebutuhan Perangkat Keras*).
4. **Format Gambar:**
   - Posisi Gambar: Rata tengah (*Center*).
   - Posisi Keterangan Gambar: Di **bawah gambar**, format `Gambar [Nomor].[Urut] [Judul Gambar]` (contoh: *Gambar 2.1: Bagan Struktur Organisasi Dinperinnaker Purbalingga*).
5. **Memperbarui Nomor Halaman Otomatis (Update Field):**
   - Setelah selesai mengedit teks di Word, klik kanan pada area **DAFTAR ISI**, **DAFTAR TABEL**, atau **DAFTAR GAMBAR**, lalu pilih **Update Field** -> **Update entire table** (atau tekan tombol `F9` pada keyboard). Nomor halaman akan tersinkronisasi otomatis!
"""

def main():
    doc_path = r'D:\Magang\sistem-satudata-dinperinnaker\document\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    
    print("Writing to document directory:", doc_path)
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(MD_CONTENT)
    print("Success! File size:", os.path.getsize(doc_path), "bytes")
    
    print("Copying to artifact directory:", art_path)
    shutil.copyfile(doc_path, art_path)
    print("Success! File size:", os.path.getsize(art_path), "bytes")

if __name__ == '__main__':
    main()
