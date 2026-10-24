'use client';

import React, { useState } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { UnitKerja, UnitTipe } from '@/types';
import { Plus, Edit3, Trash2, X, FileText, Users as UsersIcon } from 'lucide-react';
import { toast } from 'sonner';

export default function UnitKerjaPage() {
  const { unitKerjas, dataRecords, users, currentUser, addUnitKerja, updateUnitKerja, deleteUnitKerja } = useData();

  const isSuperAdmin = currentUser?.role === 'Super Admin';

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUnit, setEditingUnit] = useState<UnitKerja | null>(null);
  const [formData, setFormData] = useState({
    nama_unit: '',
    tipe: 'bidang' as UnitTipe,
  });


  const handleOpenAdd = () => {
    setEditingUnit(null);
    setFormData({ nama_unit: '', tipe: 'bidang' });
    setIsModalOpen(true);
  };

  const handleOpenEdit = (unit: UnitKerja) => {
    setEditingUnit(unit);
    setFormData({ nama_unit: unit.nama_unit, tipe: unit.tipe });
    setIsModalOpen(true);
  };

  const handleDelete = async (unit: UnitKerja) => {
    if (confirm(`Apakah Anda yakin ingin menghapus unit kerja "${unit.nama_unit}"?`)) {
      try {
        await deleteUnitKerja(unit.id);
        toast.success(`Unit kerja "${unit.nama_unit}" berhasil dihapus.`);
      } catch (err: any) {
        toast.error(err.message || 'Gagal menghapus unit kerja.');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.nama_unit.trim()) return;

    try {
      if (editingUnit) {
        await updateUnitKerja(editingUnit.id, formData);
        toast.success('Unit kerja berhasil diperbarui.');
      } else {
        await addUnitKerja(formData);
        toast.success('Unit kerja baru berhasil ditambahkan.');
      }
      setIsModalOpen(false);
    } catch (err: any) {
      toast.error(err.message || 'Gagal menyimpan unit kerja.');
    }
  };

  if (!isSuperAdmin) {
    return (
      <AppLayout title="Akses Ditolak">
        <div className="bg-white dark:bg-[#1e293b] p-8 rounded-2xl border border-rose-200 dark:border-rose-900 text-center max-w-lg mx-auto">
          <p className="text-sm font-bold text-rose-600 dark:text-rose-400">
            Halaman ini khusus untuk pengguna dengan peran Super Admin.
          </p>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout title="Manajemen Unit Kerja">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs">
          <div>
            <h2 className="text-xl font-extrabold text-[#25396e] dark:text-white tracking-tight">
              Manajemen Unit Kerja Dinas
            </h2>
            <p className="text-xs text-[#7c8db5] font-medium mt-1">
              Kelola klasifikasi Bidang, Unit Sekretariat, dan Balai Pelaksana Teknis (UPTD)
            </p>
          </div>

          <button
            onClick={handleOpenAdd}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#2a92a2] hover:bg-[#217784] text-white text-xs font-bold transition-all shadow-xs cursor-pointer self-start sm:self-auto"
          >
            <Plus className="w-4 h-4" />
            <span>Tambah Unit Kerja</span>
          </button>
        </div>


        {/* Unit Kerja Table */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#f2f7ff] dark:bg-slate-800/80 text-[#25396e] dark:text-slate-200 uppercase tracking-wider font-bold border-b border-[#eaeff5] dark:border-[#334155]">
                <tr>
                  <th className="px-4 py-3.5 w-12 text-center">No</th>
                  <th className="px-4 py-3.5">Nama Unit Kerja / Bidang</th>
                  <th className="px-4 py-3.5 text-center w-36">Tipe Struktur</th>
                  <th className="px-4 py-3.5 text-center w-28">Total Data</th>
                  <th className="px-4 py-3.5 text-center w-28">Pengguna</th>
                  <th className="px-4 py-3.5 text-center w-28">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#eaeff5] dark:divide-[#334155] font-medium text-[#25396e] dark:text-slate-200">
                {unitKerjas.map((u, index) => {
                  const recordCount = dataRecords.filter(d => d.unit_kerja_id === u.id).length;
                  const userCount = users.filter(usr => usr.unit_kerja_id === u.id).length;
                  const hasRelations = recordCount > 0 || userCount > 0;

                  return (
                    <tr key={u.id} className="hover:bg-[#f2f7ff]/50 dark:hover:bg-slate-800/50 transition-colors">
                      <td className="px-4 py-3 text-center text-[#7c8db5] font-semibold">{index + 1}</td>
                      <td className="px-4 py-3 font-bold text-[#25396e] dark:text-white">{u.nama_unit}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`
                          inline-block px-2.5 py-1 rounded-full text-[10px] font-bold uppercase
                          ${u.tipe === 'bidang' ? 'bg-sky-50 text-sky-700 dark:bg-sky-950/60 dark:text-sky-400' : 
                            u.tipe === 'sekretariat' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400' : 
                            'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400'}
                        `}>
                          {u.tipe}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-flex items-center gap-1 text-xs font-bold text-[#25396e] dark:text-slate-300">
                          <FileText className="w-3.5 h-3.5 text-[#2a92a2]" />
                          <span>{recordCount}</span>
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-flex items-center gap-1 text-xs font-bold text-[#25396e] dark:text-slate-300">
                          <UsersIcon className="w-3.5 h-3.5 text-amber-500" />
                          <span>{userCount}</span>
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <div className="flex items-center justify-center gap-1.5">
                          <button
                            onClick={() => handleOpenEdit(u)}
                            className="p-1.5 rounded-lg text-[#2a92a2] hover:bg-[#e6f4f6] dark:hover:bg-slate-700 transition-colors cursor-pointer"
                            title="Edit"
                          >
                            <Edit3 className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(u)}
                            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                              hasRelations 
                                ? 'text-slate-400 hover:text-rose-600 hover:bg-slate-100 dark:hover:bg-slate-700' 
                                : 'text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40'
                            }`}
                            title={hasRelations ? `Memiliki ${recordCount} data & ${userCount} pengguna (dilarang dihapus di Laravel)` : 'Hapus Unit Kerja'}
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Tambah/Edit */}
        {isModalOpen && (
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-[#1e293b] w-full max-w-md rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden">
              <div className="px-6 py-4 border-b border-[#eaeff5] dark:border-[#334155] flex items-center justify-between bg-[#f2f7ff] dark:bg-slate-800">
                <h3 className="font-extrabold text-[#25396e] dark:text-white text-base">
                  {editingUnit ? 'Edit Unit Kerja' : 'Tambah Unit Kerja'}
                </h3>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-1 rounded-lg text-[#7c8db5] hover:text-[#25396e] dark:hover:text-white cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Nama Unit Kerja <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Contoh: Bidang Hubungan Industrial..."
                    value={formData.nama_unit}
                    onChange={(e) => setFormData({ ...formData, nama_unit: e.target.value })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Tipe Klasifikasi <span className="text-rose-500">*</span>
                  </label>
                  <select
                    value={formData.tipe}
                    onChange={(e) => setFormData({ ...formData, tipe: e.target.value as UnitTipe })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  >
                    <option value="bidang">Bidang Dinas</option>
                    <option value="sekretariat">Unit Sekretariat</option>
                    <option value="uptd">Unit Pelaksana Teknis (UPTD)</option>
                  </select>
                </div>

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
                    {editingUnit ? 'Simpan Perubahan' : 'Tambahkan'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
