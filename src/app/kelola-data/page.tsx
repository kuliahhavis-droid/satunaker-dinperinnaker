'use client';

import React, { useState, useMemo } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { DataRecord, DataStatus } from '@/types';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, 
  Search, 
  ExternalLink, 
  Edit3, 
  Trash2, 
  X, 
  FileText,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Lock,
  Shield,
  FileSpreadsheet
} from 'lucide-react';
import { toast } from 'sonner';
import { exportSatuNakerExcel } from '@/lib/exportExcel';

export default function KelolaDataPage() {
  const { 
    dataRecords, 
    unitKerjas, 
    currentUser, 
    addDataRecord, 
    updateDataRecord, 
    deleteDataRecord 
  } = useData();

  const isSuperAdmin = currentUser?.role === 'Super Admin';
  const isKadis = currentUser?.role === 'Kepala Dinas';

  // Filters state
  const [search, setSearch] = useState('');
  const [filterUnit, setFilterUnit] = useState(
    currentUser?.unit_kerja_id && !isSuperAdmin && !isKadis 
      ? currentUser.unit_kerja_id.toString() 
      : 'all'
  );
  const [filterTahun, setFilterTahun] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<DataRecord | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    unit_kerja_id: 1,
    nama_data: '',
    satuan: '',
    tahun_awal: 2026,
    jumlah: 0,
    link_gdrive: '',
    deskripsi: '',
    status: 'Aktif' as DataStatus,
  });

  // Auto-switch filter when user switches
  React.useEffect(() => {
    if (currentUser?.unit_kerja_id && !isSuperAdmin && !isKadis) {
      setFilterUnit(currentUser.unit_kerja_id.toString());
    }
  }, [currentUser, isSuperAdmin, isKadis]);

  // Available years
  const availableYears = useMemo(() => {
    const defaultYears = [2026, 2025, 2024];
    const yrs = Array.from(new Set([...defaultYears, ...dataRecords.map(d => d.tahun_awal)])).sort((a, b) => b - a);
    return yrs;
  }, [dataRecords]);

  // Filtered records
  const filteredData = useMemo(() => {
    return dataRecords.filter(item => {
      const matchSearch = 
        item.nama_data.toLowerCase().includes(search.toLowerCase()) ||
        (item.deskripsi && item.deskripsi.toLowerCase().includes(search.toLowerCase())) ||
        item.satuan.toLowerCase().includes(search.toLowerCase());
      
      const matchUnit = filterUnit === 'all' || item.unit_kerja_id.toString() === filterUnit;
      const matchTahun = filterTahun === 'all' || item.tahun_awal.toString() === filterTahun;
      const matchStatus = filterStatus === 'all' || item.status === filterStatus;

      return matchSearch && matchUnit && matchTahun && matchStatus;
    });
  }, [dataRecords, search, filterUnit, filterTahun, filterStatus]);

  // Open Add Modal
  const handleOpenAdd = () => {
    if (isKadis) {
      toast.error('Kepala Dinas hanya memiliki akses read-only.');
      return;
    }
    setEditingRecord(null);
    setFormData({
      unit_kerja_id: currentUser?.unit_kerja_id || (unitKerjas[0]?.id || 1),
      nama_data: '',
      satuan: '',
      tahun_awal: 2026,
      jumlah: 0,
      link_gdrive: '',
      deskripsi: '',
      status: 'Aktif',
    });
    setIsModalOpen(true);
  };

  // Open Edit Modal
  const handleOpenEdit = (record: DataRecord) => {
    if (isKadis) {
      toast.error('Kepala Dinas hanya memiliki akses read-only.');
      return;
    }
    if (!isSuperAdmin && record.unit_kerja_id !== currentUser?.unit_kerja_id) {
      toast.error('Anda hanya dapat mengubah data unit kerja Anda sendiri.');
      return;
    }
    setEditingRecord(record);
    setFormData({
      unit_kerja_id: record.unit_kerja_id,
      nama_data: record.nama_data,
      satuan: record.satuan,
      tahun_awal: record.tahun_awal,
      jumlah: record.jumlah,
      link_gdrive: record.link_gdrive || '',
      deskripsi: record.deskripsi || '',
      status: record.status,
    });
    setIsModalOpen(true);
  };

  // Delete handler
  const handleDelete = async (record: DataRecord) => {
    if (isKadis) {
      toast.error('Kepala Dinas hanya memiliki akses read-only.');
      return;
    }
    if (!isSuperAdmin && record.unit_kerja_id !== currentUser?.unit_kerja_id) {
      toast.error('Anda hanya dapat menghapus data unit kerja Anda sendiri.');
      return;
    }
    if (confirm(`Apakah Anda yakin ingin menghapus data "${record.nama_data}"?`)) {
      try {
        await deleteDataRecord(record.id);
        toast.success(`Data '${record.nama_data}' berhasil dihapus dari sistem!`);
      } catch (err: any) {
        toast.error(err.message || 'Gagal menghapus data.');
      }
    }
  };

  // Submit handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.nama_data.trim() || !formData.satuan.trim()) {
      toast.error('Nama Data dan Satuan Data wajib diisi.');
      return;
    }

    // URL validation for link_gdrive if filled
    if (formData.link_gdrive && formData.link_gdrive.trim() !== '') {
      if (!/^https?:\/\//i.test(formData.link_gdrive.trim())) {
        toast.error('Format Link Google Drive harus berupa URL yang valid (misal: https://drive.google.com/...).');
        return;
      }
    }

    try {
      if (editingRecord) {
        await updateDataRecord(editingRecord.id, {
          ...formData,
          unit_kerja_id: isSuperAdmin ? Number(formData.unit_kerja_id) : (currentUser?.unit_kerja_id || Number(formData.unit_kerja_id)),
          tahun_awal: Number(formData.tahun_awal),
          jumlah: Number(formData.jumlah),
        });
        toast.success(`Data '${formData.nama_data}' berhasil diperbarui!`);
      } else {
        await addDataRecord({
          ...formData,
          unit_kerja_id: isSuperAdmin ? Number(formData.unit_kerja_id) : (currentUser?.unit_kerja_id || Number(formData.unit_kerja_id)),
          tahun_awal: Number(formData.tahun_awal),
          jumlah: Number(formData.jumlah),
          created_by: currentUser?.id || null,
        });
        toast.success(`Data '${formData.nama_data}' berhasil disimpan ke sistem!`);
      }
      setIsModalOpen(false);
    } catch (err: any) {
      toast.error(err.message || 'Gagal menyimpan data.');
    }
  };

  // Handle Export Excel
  const handleExportExcel = () => {
    try {
      if (filteredData.length === 0) {
        toast.info('Tidak ada data yang sesuai dengan filter untuk diekspor.');
        return;
      }
      const filename = exportSatuNakerExcel({
        records: filteredData,
        unitKerjas,
        filterUnit,
        filterTahun,
        filterStatus,
      });
      toast.success(`Berkas Excel berhasil diunduh: ${filename}`);
    } catch (err: any) {
      toast.error(err?.message || 'Gagal mengekspor berkas Excel.');
    }
  };

  return (
    <AppLayout title="Kelola Data Sektoral">
      <div className="space-y-6">
        {/* Header Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs">
          <div>
            <h2 className="text-xl font-extrabold text-[#25396e] dark:text-white tracking-tight">
              Manajemen Data Statistik Sektoral
            </h2>
            <p className="text-xs text-[#7c8db5] font-medium mt-1">
              Pencatatan data capaian indikator dinas terhubung Google Drive
            </p>
          </div>

          <div className="flex items-center gap-2.5 self-start sm:self-auto flex-wrap">
            {/* Export Excel Button */}
            <button
              onClick={handleExportExcel}
              className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] hover:border-emerald-500 text-[#25396e] dark:text-slate-200 hover:text-emerald-600 text-xs font-bold transition-all shadow-xs cursor-pointer"
              title="Ekspor data hasil filter ke file Excel (.xlsx)"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
              <span>Ekspor Excel</span>
            </button>

            {isKadis ? (
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300 text-xs font-bold">
                <Shield className="w-4 h-4 text-amber-600" />
                <span>Mode Eksekutif: Hanya Baca</span>
              </div>
            ) : (
              <button
                onClick={handleOpenAdd}
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-[#2a92a2] hover:bg-[#217784] text-white text-xs font-bold transition-all shadow-xs cursor-pointer"
              >
                <Plus className="w-4 h-4" />
                <span>Tambah Data</span>
              </button>
            )}
          </div>
        </div>

        {/* Filter Controls */}
        <div className="bg-white dark:bg-[#1e293b] p-4 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs flex flex-wrap gap-3 items-center justify-between">
          {/* Search Bar */}
          <div className="relative min-w-[240px] flex-1">
            <Search className="w-4 h-4 text-[#7c8db5] absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Cari nama data, satuan, rincian..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-medium text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2] transition-colors"
            />
          </div>

          <div className="flex flex-wrap gap-2 items-center">
            {/* Unit Kerja Filter */}
            <select
              value={filterUnit}
              onChange={(e) => setFilterUnit(e.target.value)}
              className="bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2] transition-colors cursor-pointer"
            >
              <option value="all">Semua Unit Kerja</option>
              {unitKerjas.map(u => (
                <option key={u.id} value={u.id.toString()}>{u.nama_unit}</option>
              ))}
            </select>

            {/* Tahun Filter */}
            <select
              value={filterTahun}
              onChange={(e) => setFilterTahun(e.target.value)}
              className="bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2] transition-colors cursor-pointer"
            >
              <option value="all">Semua Tahun</option>
              {availableYears.map(yr => (
                <option key={yr} value={yr.toString()}>{yr}</option>
              ))}
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2] transition-colors cursor-pointer"
            >
              <option value="all">Semua Status</option>
              <option value="Aktif">Aktif</option>
              <option value="Tidak Aktif">Tidak Aktif</option>
              <option value="Arsip">Arsip</option>
            </select>
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#f2f7ff] dark:bg-slate-800/80 text-[#25396e] dark:text-slate-200 uppercase tracking-wider font-bold border-b border-[#eaeff5] dark:border-[#334155]">
                <tr>
                  <th className="px-4 py-3.5 w-12 text-center">No</th>
                  <th className="px-4 py-3.5 min-w-[200px]">Unit Kerja</th>
                  <th className="px-4 py-3.5 min-w-[260px]">Nama Data</th>
                  <th className="px-4 py-3.5 text-center">Satuan</th>
                  <th className="px-4 py-3.5 text-center">Tahun</th>
                  <th className="px-4 py-3.5 text-right">Jumlah</th>
                  <th className="px-4 py-3.5 text-center">Status</th>
                  <th className="px-4 py-3.5 text-center">Dokumen Drive</th>
                  {!isKadis && <th className="px-4 py-3.5 text-center w-24">Aksi</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-[#eaeff5] dark:divide-[#334155] font-medium text-[#25396e] dark:text-slate-200">
                {filteredData.length === 0 ? (
                  <tr>
                    <td colSpan={isKadis ? 8 : 9} className="px-4 py-12 text-center text-[#7c8db5]">
                      <FileText className="w-10 h-10 mx-auto text-[#cbd5e1] mb-2" />
                      Tidak ada data yang sesuai dengan filter pencarian.
                    </td>
                  </tr>
                ) : (
                  filteredData.map((item, index) => {
                    const unit = unitKerjas.find(u => u.id === item.unit_kerja_id);
                    const canEdit = isSuperAdmin || (item.unit_kerja_id === currentUser?.unit_kerja_id);

                    return (
                      <tr key={item.id} className="hover:bg-[#f2f7ff]/50 dark:hover:bg-slate-800/50 transition-colors">
                        <td className="px-4 py-3 text-center text-[#7c8db5] font-semibold">{index + 1}</td>
                        <td className="px-4 py-3">
                          <span className="font-bold text-[#25396e] dark:text-white block leading-tight">
                            {unit?.nama_unit || `Unit #${item.unit_kerja_id}`}
                          </span>
                          {item.unit_kerja_id === currentUser?.unit_kerja_id ? (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-md mt-1 border border-emerald-200 dark:border-emerald-800">
                              ✓ Milik Unit Anda
                            </span>
                          ) : (
                            <span className="inline-block text-[10px] font-medium text-[#7c8db5] mt-1">
                              Unit Lain
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-3">
                          <span className="font-semibold block leading-snug">{item.nama_data}</span>
                          {item.deskripsi && (
                            <span className="text-[11px] text-[#7c8db5] line-clamp-1 mt-0.5">
                              {item.deskripsi}
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-center text-[#7c8db5] font-semibold">{item.satuan}</td>
                        <td className="px-4 py-3 text-center font-bold text-[#2a92a2]">{item.tahun_awal}</td>
                        <td className="px-4 py-3 text-right font-black">
                          {item.jumlah.toLocaleString('id-ID')}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className={`
                            inline-block px-2.5 py-1 rounded-full text-[10px] font-bold
                            ${item.status === 'Aktif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800' : 
                              item.status === 'Arsip' ? 'bg-amber-50 text-amber-700 border border-amber-200' : 
                              'bg-rose-50 text-rose-700 border border-rose-200'}
                          `}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center">
                          {item.link_gdrive ? (
                            <a
                              href={item.link_gdrive}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#e6f4f6] dark:bg-slate-800 text-[#2a92a2] hover:bg-[#2a92a2] hover:text-white text-[11px] font-bold transition-all"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                              <span>Buka File</span>
                            </a>
                          ) : (
                            <span className="text-[#cbd5e1] font-semibold">-</span>
                          )}
                        </td>
                        {!isKadis && (
                          <td className="px-4 py-3 text-center">
                            {canEdit ? (
                              <div className="flex items-center justify-center gap-1.5">
                                <button
                                  onClick={() => handleOpenEdit(item)}
                                  className="p-1.5 rounded-lg text-[#2a92a2] hover:bg-[#e6f4f6] dark:hover:bg-slate-700 transition-colors cursor-pointer"
                                  title="Edit Data"
                                >
                                  <Edit3 className="w-4 h-4" />
                                </button>
                                <button
                                  onClick={() => handleDelete(item)}
                                  className="p-1.5 rounded-lg text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors cursor-pointer"
                                  title="Hapus Data"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </div>
                            ) : (
                              <div className="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-[#7c8db5] text-[10px] font-medium" title={`Hanya dapat diubah oleh ${unit?.nama_unit || 'unit pemilik'}`}>
                                <Lock className="w-3 h-3 text-slate-400" />
                                <span>Terkunci</span>
                              </div>
                            )}
                          </td>
                        )}
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Tambah / Edit Data */}
        <AnimatePresence>
          {isModalOpen && (
            <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="bg-white dark:bg-[#1e293b] w-full max-w-xl rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden"
              >
                <div className="px-6 py-4 border-b border-[#eaeff5] dark:border-[#334155] flex items-center justify-between bg-[#f2f7ff] dark:bg-slate-800">
                  <h3 className="font-extrabold text-[#25396e] dark:text-white text-base">
                    {editingRecord ? 'Perbarui Data Sektoral' : 'Tambah Data Sektoral Baru'}
                  </h3>
                  <button
                    onClick={() => setIsModalOpen(false)}
                    className="p-1 rounded-lg text-[#7c8db5] hover:text-[#25396e] dark:hover:text-white cursor-pointer"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
                  {/* Unit Kerja Selection */}
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Unit Kerja / Bidang <span className="text-rose-500">*</span>
                    </label>
                    <select
                      value={formData.unit_kerja_id}
                      disabled={!isSuperAdmin}
                      onChange={(e) => setFormData({ ...formData, unit_kerja_id: Number(e.target.value) })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2] disabled:opacity-75 disabled:cursor-not-allowed"
                    >
                      {unitKerjas.map(u => (
                        <option key={u.id} value={u.id}>{u.nama_unit}</option>
                      ))}
                    </select>
                    {!isSuperAdmin && (
                      <p className="text-[10px] text-[#7c8db5] mt-1">
                        Unit kerja otomatis terkunci sesuai akun tugas Anda.
                      </p>
                    )}
                  </div>

                  {/* Nama Data */}
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Nama Data Capaian / Indikator <span className="text-rose-500">*</span>
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="Contoh: Jumlah Peserta Pelatihan Vokasi BNSP"
                      value={formData.nama_data}
                      onChange={(e) => setFormData({ ...formData, nama_data: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>

                  {/* Satuan & Tahun */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                        Satuan Data <span className="text-rose-500">*</span>
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="Orang, Perusahaan, Kasus..."
                        value={formData.satuan}
                        onChange={(e) => setFormData({ ...formData, satuan: e.target.value })}
                        className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                        Tahun Data <span className="text-rose-500">*</span>
                      </label>
                      <input
                        type="number"
                        required
                        min={2000}
                        max={2100}
                        value={formData.tahun_awal}
                        onChange={(e) => setFormData({ ...formData, tahun_awal: Number(e.target.value) })}
                        className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                      />
                    </div>
                  </div>

                  {/* Jumlah & Status */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                        Jumlah Capaian <span className="text-rose-500">*</span>
                        Jumlah Data <span className="text-rose-500">*</span>
                      </label>
                      <input
                        type="number"
                        step="any"
                        required
                        min={0}
                        value={formData.jumlah}
                        onChange={(e) => setFormData({ ...formData, jumlah: Number(e.target.value) })}
                        className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                        Status Publikasi <span className="text-rose-500">*</span>
                      </label>
                      <select
                        value={formData.status}
                        onChange={(e) => setFormData({ ...formData, status: e.target.value as DataStatus })}
                        className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                      >
                        <option value="Aktif">Aktif</option>
                        <option value="Tidak Aktif">Tidak Aktif</option>
                        <option value="Arsip">Arsip</option>
                      </select>
                    </div>
                  </div>

                  {/* Link Google Drive */}
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Tautan Google Drive (Berkas Rincian / Bukti Fisik)
                    </label>
                    <input
                      type="url"
                      placeholder="https://drive.google.com/drive/folders/..."
                      value={formData.link_gdrive}
                      onChange={(e) => setFormData({ ...formData, link_gdrive: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                    <p className="text-[10px] text-[#7c8db5] mt-1">
                      Pastikan tautan Google Drive disetel ke &quot;Siapa saja yang memiliki link dapat melihat&quot;.
                    </p>
                  </div>

                  {/* Deskripsi */}
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Deskripsi / Catatan Tambahan
                    </label>
                    <textarea
                      rows={3}
                      placeholder="Keterangan metodologi, dasar hukum, atau rincian sumber data..."
                      value={formData.deskripsi}
                      onChange={(e) => setFormData({ ...formData, deskripsi: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-medium text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>

                  {/* Form Buttons */}
                  <div className="pt-3 border-t border-[#eaeff5] dark:border-[#334155] flex items-center justify-end gap-2.5">
                    <button
                      type="button"
                      onClick={() => setIsModalOpen(false)}
                      className="px-4 py-2 rounded-xl text-xs font-bold text-[#7c8db5] hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors cursor-pointer"
                    >
                      Batal
                    </button>
                    <button
                      type="submit"
                      className="px-5 py-2 rounded-xl text-xs font-bold bg-[#2a92a2] hover:bg-[#217784] text-white shadow-xs transition-all cursor-pointer"
                    >
                      {editingRecord ? 'Simpan Perubahan' : 'Tambahkan Data'}
                    </button>
                  </div>
                </form>
              </motion.div>
            </div>
          )}
        </AnimatePresence>

      </div>
    </AppLayout>
  );
}
