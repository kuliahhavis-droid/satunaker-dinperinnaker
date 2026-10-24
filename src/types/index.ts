export type UnitTipe = 'bidang' | 'sekretariat' | 'uptd';

export type UserRole = 
  | 'Super Admin' 
  | 'Admin Bidang' 
  | 'Admin Sekretariat' 
  | 'Admin UPTD' 
  | 'Kepala Dinas';

export type DataStatus = 'Aktif' | 'Tidak Aktif' | 'Arsip';
export type UserStatus = 'Aktif' | 'Nonaktif';

export interface UnitKerja {
  id: number;
  nama_unit: string;
  tipe: UnitTipe;
  created_at?: string;
  updated_at?: string;
  data_count?: number;
}

export interface UserProfile {
  id: string | number;
  nama_lengkap: string;
  nama: string;
  username: string;
  email: string;
  role: UserRole;
  unit_kerja_id: number | null;
  status: UserStatus;
  password?: string;
  unitKerja?: UnitKerja;
  created_at?: string;
  updated_at?: string;
}

export interface DataRecord {
  id: number;
  unit_kerja_id: number;
  nama_data: string;
  satuan: string;
  tahun_awal: number;
  jumlah: number;
  link_gdrive: string | null;
  deskripsi: string | null;
  status: DataStatus;
  created_by: string | number | null;
  created_at?: string;
  updated_at?: string;
  unitKerja?: UnitKerja;
  creator?: UserProfile;
}

export interface LogAktivitas {
  id: number;
  user: string;
  aktivitas: string;
  tanggal: string;
  ip_address: string | null;
  created_at?: string;
}
