-- ========================================================
-- SKEMA SUPABASE POSTGRESQL (SATU DATA DINPERINNAKER)
-- Salin dan jalankan seluruh isi file ini di:
-- Dashboard Supabase -> SQL Editor -> New Query -> Run
-- ========================================================

-- 1. Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. ENUM TYPES
DO $$ BEGIN
    CREATE TYPE unit_tipe AS ENUM ('bidang', 'sekretariat', 'uptd');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('Super Admin', 'Admin Bidang', 'Admin Sekretariat', 'Admin UPTD', 'Kepala Dinas');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE data_status AS ENUM ('Aktif', 'Tidak Aktif', 'Arsip');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_status AS ENUM ('Aktif', 'Nonaktif');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. TABEL UNIT KERJA
CREATE TABLE IF NOT EXISTS public.unit_kerja (
    id BIGSERIAL PRIMARY KEY,
    nama_unit VARCHAR(255) NOT NULL,
    tipe unit_tipe NOT NULL DEFAULT 'bidang',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. TABEL PROFIL PENGGUNA
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama_lengkap VARCHAR(255) NOT NULL,
    nama VARCHAR(255),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role NOT NULL DEFAULT 'Admin Bidang',
    unit_kerja_id BIGINT REFERENCES public.unit_kerja(id) ON DELETE SET NULL,
    status user_status NOT NULL DEFAULT 'Aktif',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. TABEL DATA RECORDS
CREATE TABLE IF NOT EXISTS public.data_records (
    id BIGSERIAL PRIMARY KEY,
    unit_kerja_id BIGINT NOT NULL REFERENCES public.unit_kerja(id) ON DELETE CASCADE,
    nama_data VARCHAR(255) NOT NULL,
    satuan VARCHAR(100) NOT NULL,
    tahun_awal INT NOT NULL,
    jumlah DOUBLE PRECISION NOT NULL DEFAULT 0,
    link_gdrive TEXT,
    deskripsi TEXT,
    status data_status NOT NULL DEFAULT 'Aktif',
    created_by UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. TABEL LOG AKTIVITAS (AUDIT TRAIL)
CREATE TABLE IF NOT EXISTS public.log_aktivitas (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    aktivitas VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. ENABLE ROW LEVEL SECURITY (RLS)
ALTER TABLE public.unit_kerja ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.log_aktivitas ENABLE ROW LEVEL SECURITY;

-- 8. RLS POLICIES (Allow Public Read & Authenticated Write)
CREATE POLICY "Public read unit_kerja" ON public.unit_kerja FOR SELECT USING (true);
CREATE POLICY "Public read profiles" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "Public read data_records" ON public.data_records FOR SELECT USING (true);
CREATE POLICY "Public read log_aktivitas" ON public.log_aktivitas FOR SELECT USING (true);

CREATE POLICY "Allow all modifications on unit_kerja" ON public.unit_kerja FOR ALL USING (true);
CREATE POLICY "Allow all modifications on profiles" ON public.profiles FOR ALL USING (true);
CREATE POLICY "Allow all modifications on data_records" ON public.data_records FOR ALL USING (true);
CREATE POLICY "Allow all modifications on log_aktivitas" ON public.log_aktivitas FOR ALL USING (true);

-- 9. SEED UNIT KERJA DEFAULT
INSERT INTO public.unit_kerja (id, nama_unit, tipe) VALUES
(1, 'Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK)', 'bidang'),
(2, 'Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK)', 'bidang'),
(3, 'Sub Bagian Perencanaan dan Keuangan (Sekretariat)', 'sekretariat'),
(4, 'Sub Bagian Umum dan Kepegawaian (Sekretariat)', 'sekretariat'),
(5, 'UPTD Balai Latihan Kerja (BLK)', 'uptd'),
(6, 'UPTD Pengembangan Industri Logam (PILOG)', 'uptd')
ON CONFLICT (id) DO NOTHING;

-- 10. SEED PROFIL PENGGUNA DEFAULT
INSERT INTO public.profiles (nama_lengkap, nama, username, email, role, unit_kerja_id, status) VALUES
('Super Administrator Sistem Satu Data', 'Super Admin', 'superadmin', 'superadmin@dinperinnaker.go.id', 'Super Admin', NULL, 'Aktif'),
('Administrator Bidang Hubungan Industrial & Jamsostek', 'Admin HIJTK', 'admin_hijtk', 'hijtk@dinperinnaker.go.id', 'Admin Bidang', 1, 'Aktif'),
('Administrator Bidang Pelatihan dan Penempatan Tenaga Kerja', 'Admin PPTK', 'admin_pptk', 'pptk@dinperinnaker.go.id', 'Admin Bidang', 2, 'Aktif'),
('Administrator Sub Bagian Perencanaan dan Keuangan', 'Admin Renkeu', 'admin_renkeu', 'renkeu@dinperinnaker.go.id', 'Admin Sekretariat', 3, 'Aktif'),
('Administrator Sub Bagian Umum dan Kepegawaian', 'Admin Umpeg', 'admin_umpeg', 'umpeg@dinperinnaker.go.id', 'Admin Sekretariat', 4, 'Aktif'),
('Administrator UPTD Balai Latihan Kerja', 'Admin BLK', 'admin_blk', 'blk@dinperinnaker.go.id', 'Admin UPTD', 5, 'Aktif'),
('Administrator UPTD Pengembangan Industri Logam', 'Admin PILOG', 'admin_pilog', 'pilog@dinperinnaker.go.id', 'Admin UPTD', 6, 'Aktif'),
('Johan Arifin, S.Sos., M.Si.', 'Kepala Dinas', 'kadis', 'kadis@dinperinnaker.go.id', 'Kepala Dinas', NULL, 'Aktif')
ON CONFLICT (username) DO NOTHING;

-- 11. SEED DATA STATISTIK AWAL
INSERT INTO public.data_records (unit_kerja_id, nama_data, satuan, tahun_awal, jumlah, link_gdrive, deskripsi, status) VALUES
(1, 'Jumlah Kasus Perselisihan HI yang Diselesaikan Melalui Mediasi', 'kasus selesai', 2024, 28, 'https://drive.google.com/drive/folders/1exampleHIJTKMediasi2024', 'Penyelesaian perselisihan hak, kepentingan, dan PHK.', 'Aktif'),
(1, 'Jumlah Perusahaan yang Menerapkan Perjanjian Kerja Bersama (PKB) & PP', 'perusahaan', 2025, 142, 'https://drive.google.com/drive/folders/1exampleHIJTKPKB2025', 'Kepatuhan peraturan perusahaan dan PKB sektor formal.', 'Aktif'),
(2, 'Jumlah Pencari Kerja Terdaftar (Kartu AK-1) yang Ditempatkan', 'orang', 2024, 4150, 'https://drive.google.com/drive/folders/1examplePenempatanKerja2024', 'Penyerapan tenaga kerja lokal ke sektor industri padat karya.', 'Aktif'),
(2, 'Jumlah Peserta Pemagangan Dalam Negeri Siap Kerja', 'orang peserta', 2025, 320, 'https://drive.google.com/drive/folders/1examplePemagangan2025', 'Program kemitraan pemagangan kerja sama dinas.', 'Aktif'),
(3, 'Persentase Realisasi Anggaran Belanja Dinas (APBD)', 'persen (%)', 2024, 96.8, 'https://drive.google.com/drive/folders/1exampleRealisasiAPBD2024', 'Akumulasi serapan anggaran tahun 2024.', 'Aktif'),
(3, 'Jumlah Dokumen Perencanaan (Renja, Renstra, DPA) Tersusun', 'dokumen', 2025, 12, 'https://drive.google.com/drive/folders/1exampleDokumenRenja2025', 'Penyusunan dokumen perencanaan dan SAKIP.', 'Aktif'),
(4, 'Jumlah Aparatur Sipil Negara (PNS & PPPK) Terkelola', 'orang pegawai', 2024, 84, 'https://drive.google.com/drive/folders/1exampleKepegawaian2024', 'Data mutasi, pangkat, dan disiplin pegawai.', 'Aktif'),
(4, 'Indeks Kepuasan Pengelolaan Layanan Administrasi & Sarpras', 'skor indeks', 2025, 88.5, 'https://drive.google.com/drive/folders/1exampleIndeksSarpras2025', 'Survei kepuasan internal pengelolaan sarana operasional.', 'Aktif'),
(5, 'Jumlah Lulusan Pelatihan Vokasi Bersertifikat Kompetensi BNSP', 'orang lulusan', 2024, 640, 'https://drive.google.com/drive/folders/1examplePBKBLK2024', 'Pelatihan kejuruan teknik las, otomotif, garmen, digital marketing.', 'Aktif'),
(5, 'Tingkat Keterserapan Kerja Lulusan BLK di Industri & Wirausaha', 'orang', 2025, 512, 'https://drive.google.com/drive/folders/1exampleSerapanBLK2025', 'Tracer study lulusan PBK yang terserap kerja < 6 bulan.', 'Aktif'),
(6, 'Volume Produksi Komponen Logam & Knalpot Terstandarisasi', 'unit produk', 2024, 16500, 'https://drive.google.com/drive/folders/1examplePilogProduksi2024', 'Fasilitasi mesin presisi untuk sentra knalpot Purbalingga.', 'Aktif'),
(6, 'Jumlah Pelaku IKM Logam yang Memanfaatkan Layanan Mesin Uji Emisi / Dyno-Test', 'unit usaha IKM', 2025, 95, 'https://drive.google.com/drive/folders/1exampleDynoTest2025', 'Pengujian desibel dan emisi knalpot standar SNI.', 'Aktif');

-- 12. INDEKS DATABASE UNTUK PERFORMA QUERY CEPAT
CREATE INDEX IF NOT EXISTS idx_data_records_unit_kerja ON public.data_records (unit_kerja_id);
CREATE INDEX IF NOT EXISTS idx_data_records_tahun ON public.data_records (tahun_awal);
CREATE INDEX IF NOT EXISTS idx_data_records_status ON public.data_records (status);
CREATE INDEX IF NOT EXISTS idx_profiles_username ON public.profiles (username);
CREATE INDEX IF NOT EXISTS idx_log_aktivitas_created_at ON public.log_aktivitas (created_at DESC);

-- 13. AUTO-UPDATE TIMESTAMP FUNCTION & TRIGGER
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at_unit_kerja ON public.unit_kerja;
CREATE TRIGGER set_updated_at_unit_kerja
BEFORE UPDATE ON public.unit_kerja
FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

DROP TRIGGER IF EXISTS set_updated_at_data_records ON public.data_records;
CREATE TRIGGER set_updated_at_data_records
BEFORE UPDATE ON public.data_records
FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- 14. COMPATIBILITY VIEWS (Identik 100% dengan nama tabel MySQL Laravel: 'data' dan 'users')
CREATE OR REPLACE VIEW public.data AS SELECT * FROM public.data_records;
CREATE OR REPLACE VIEW public.users AS SELECT * FROM public.profiles;

-- Selesai! Basis data siap digunakan untuk Satu Data DINPERINNAKER.
