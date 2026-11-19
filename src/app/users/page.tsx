'use client';

import React, { useState } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { UserProfile, UserRole } from '@/types';
import { Users, Plus, Key, ToggleLeft, ToggleRight, Trash2, X, Pencil } from 'lucide-react';
import { toast } from 'sonner';

export default function UsersPage() {
  const { users, unitKerjas, currentUser, addUser, updateUser, deleteUser, toggleUserStatus, resetPassword } = useData();

  const isSuperAdmin = currentUser?.role === 'Super Admin';

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isResetModalOpen, setIsResetModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserProfile | null>(null);
  const [editUser, setEditUser] = useState<UserProfile | null>(null);
  const [newPassword, setNewPassword] = useState('');

  // Form State
  const [formData, setFormData] = useState({
    nama_lengkap: '',
    nama: '',
    username: '',
    email: '',
    role: 'Admin Bidang' as UserRole,
    unit_kerja_id: 1 as number | null,
    status: 'Aktif' as const,
    password: '',
  });

  const [editFormData, setEditFormData] = useState({
    nama_lengkap: '',
    username: '',
    email: '',
    role: 'Admin Bidang' as UserRole,
    unit_kerja_id: 1 as number | null,
    status: 'Aktif' as 'Aktif' | 'Nonaktif',
  });

  const handleOpenAdd = () => {
    setFormData({
      nama_lengkap: '',
      nama: '',
      username: '',
      email: '',
      role: 'Admin Bidang',
      unit_kerja_id: unitKerjas[0]?.id || 1,
      status: 'Aktif',
      password: '',
    });
    setIsAddModalOpen(true);
  };

  const handleOpenEdit = (user: UserProfile) => {
    setEditUser(user);
    setEditFormData({
      nama_lengkap: user.nama_lengkap || user.nama,
      username: user.username,
      email: user.email || '',
      role: user.role,
      unit_kerja_id: user.unit_kerja_id || (unitKerjas[0]?.id ?? 1),
      status: (user.status as 'Aktif' | 'Nonaktif') || 'Aktif',
    });
    setIsEditModalOpen(true);
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editUser || !editFormData.username.trim()) return;

    if (['Admin Bidang', 'Admin Sekretariat', 'Admin UPTD'].includes(editFormData.role) && !editFormData.unit_kerja_id) {
      toast.error('Unit kerja wajib dipilih untuk Admin Bidang, Sekretariat, atau UPTD.');
      return;
    }

    try {
      await updateUser(editUser.id, {
        nama_lengkap: editFormData.nama_lengkap,
        nama: editFormData.nama_lengkap,
        username: editFormData.username,
        email: editFormData.email,
        role: editFormData.role,
        unit_kerja_id: ['Super Admin', 'Kepala Dinas'].includes(editFormData.role) ? null : Number(editFormData.unit_kerja_id),
        status: editFormData.status,
      });
      toast.success(`Data akun "${editFormData.username}" berhasil diperbarui.`);
      setIsEditModalOpen(false);
    } catch (err: any) {
      toast.error(err.message || 'Gagal memperbarui data pengguna.');
    }
  };

  const handleOpenReset = (user: UserProfile) => {
    setSelectedUser(user);
    setNewPassword('');
    setIsResetModalOpen(true);
  };

  const handleAddSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.username.trim() || !formData.password.trim()) return;

    if (['Admin Bidang', 'Admin Sekretariat', 'Admin UPTD'].includes(formData.role) && !formData.unit_kerja_id) {
      toast.error('Unit kerja wajib dipilih untuk Admin Bidang, Sekretariat, atau UPTD.');
      return;
    }

    try {
      await addUser({
        ...formData,
        nama: formData.nama_lengkap,
        unit_kerja_id: ['Super Admin', 'Kepala Dinas'].includes(formData.role) ? null : Number(formData.unit_kerja_id),
      });
      toast.success(`Pengguna ${formData.username} berhasil ditambahkan.`);
      setIsAddModalOpen(false);
    } catch (err: any) {
      toast.error(err.message || 'Gagal menambahkan pengguna.');
    }
  };

  const handleResetSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUser || !newPassword.trim()) return;
    try {
      await resetPassword(selectedUser.id, newPassword);
      toast.success(`Password untuk ${selectedUser.username} berhasil diatur ulang.`);
      setIsResetModalOpen(false);
    } catch (err: any) {
      toast.error(err.message || 'Gagal mereset kata sandi.');
    }
  };

  const handleToggleStatus = async (user: UserProfile) => {
    try {
      await toggleUserStatus(user.id);
      toast.success(`Status akun ${user.username} berhasil diperbarui.`);
    } catch (err: any) {
      toast.error(err.message || 'Gagal mengubah status akun.');
    }
  };

  const handleDelete = async (user: UserProfile) => {
    if (confirm(`Apakah Anda yakin ingin menghapus akun "${user.username}"?`)) {
      try {
        await deleteUser(user.id);
        toast.success(`Akun "${user.username}" berhasil dihapus.`);
      } catch (err: any) {
        toast.error(err.message || 'Gagal menghapus akun pengguna.');
      }
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
    <AppLayout title="Manajemen Pengguna">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs">
          <div>
            <h2 className="text-xl font-extrabold text-[#25396e] dark:text-white tracking-tight">
              Manajemen Akun Pengguna & Hak Akses (RBAC)
            </h2>
            <p className="text-xs text-[#7c8db5] font-medium mt-1">
              Atur hak akses Super Admin, Admin Bidang, Admin Sekretariat, Admin UPTD, dan Kepala Dinas
            </p>
          </div>

          <button
            onClick={handleOpenAdd}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#2a92a2] hover:bg-[#217784] text-white text-xs font-bold transition-all shadow-xs cursor-pointer self-start sm:self-auto"
          >
            <Plus className="w-4 h-4" />
            <span>Tambah Pengguna Baru</span>
          </button>
        </div>

        {/* Users Table */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#f2f7ff] dark:bg-slate-800/80 text-[#25396e] dark:text-slate-200 uppercase tracking-wider font-bold border-b border-[#eaeff5] dark:border-[#334155]">
                <tr>
                  <th className="px-4 py-3.5 w-12 text-center">No</th>
                  <th className="px-4 py-3.5">Nama & Username</th>
                  <th className="px-4 py-3.5">Email</th>
                  <th className="px-4 py-3.5">Peran / Role</th>
                  <th className="px-4 py-3.5">Unit Kerja Terikat</th>
                  <th className="px-4 py-3.5 text-center w-28">Status</th>
                  <th className="px-4 py-3.5 text-center w-32">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#eaeff5] dark:divide-[#334155] font-medium text-[#25396e] dark:text-slate-200">
                {users.map((u, index) => {
                  const unit = unitKerjas.find(item => item.id === u.unit_kerja_id);
                  return (
                    <tr key={u.id} className="hover:bg-[#f2f7ff]/50 dark:hover:bg-slate-800/50 transition-colors">
                      <td className="px-4 py-3 text-center text-[#7c8db5] font-semibold">{index + 1}</td>
                      <td className="px-4 py-3">
                        <span className="font-bold text-[#25396e] dark:text-white block">{u.nama_lengkap || u.nama}</span>
                        <span className="text-[11px] text-[#7c8db5] block font-mono">@{u.username}</span>
                      </td>
                      <td className="px-4 py-3 text-[#7c8db5]">{u.email}</td>
                      <td className="px-4 py-3">
                        <span className="inline-block px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#e6f4f6] dark:bg-slate-800 text-[#2a92a2]">
                          {u.role}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-semibold text-slate-700 dark:text-slate-300">
                        {unit ? unit.nama_unit : <span className="text-[#cbd5e1] italic">Semua Unit (Pusat)</span>}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <button
                          onClick={() => handleToggleStatus(u)}
                          className={`
                            inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold cursor-pointer transition-colors
                            ${u.status === 'Aktif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800' : 'bg-rose-50 text-rose-700 border border-rose-200'}
                          `}
                          title="Klik untuk mengubah status aktif/nonaktif"
                        >
                          {u.status === 'Aktif' ? <ToggleRight className="w-3.5 h-3.5 text-emerald-600" /> : <ToggleLeft className="w-3.5 h-3.5 text-rose-600" />}
                          <span>{u.status}</span>
                        </button>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <div className="flex items-center justify-center gap-1.5">
                          <button
                            onClick={() => handleOpenEdit(u)}
                            className="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                            title="Edit Data Pengguna"
                          >
                            <Pencil className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleOpenReset(u)}
                            className="p-1.5 rounded-lg text-amber-600 hover:bg-amber-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                            title="Reset Password"
                          >
                            <Key className="w-4 h-4" />
                          </button>
                          {currentUser && u.id !== currentUser.id && (
                            <button
                              onClick={() => handleDelete(u)}
                              className="p-1.5 rounded-lg text-rose-600 hover:bg-rose-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                              title="Hapus Pengguna"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Tambah User */}
        {isAddModalOpen && (
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-[#1e293b] w-full max-w-lg rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden">
              <div className="px-6 py-4 border-b border-[#eaeff5] dark:border-[#334155] flex items-center justify-between bg-[#f2f7ff] dark:bg-slate-800">
                <h3 className="font-extrabold text-[#25396e] dark:text-white text-base">Tambah Pengguna Baru</h3>
                <button
                  onClick={() => setIsAddModalOpen(false)}
                  className="p-1 rounded-lg text-[#7c8db5] hover:text-[#25396e] dark:hover:text-white cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleAddSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Nama Lengkap <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Contoh: Budi Santoso, S.Kom."
                    value={formData.nama_lengkap}
                    onChange={(e) => setFormData({ ...formData, nama_lengkap: e.target.value })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Username <span className="text-rose-500">*</span>
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="admin_nama"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Email Dinas
                    </label>
                    <input
                      type="email"
                      placeholder="nama@dinperinnaker.go.id"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Peran (Role) <span className="text-rose-500">*</span>
                    </label>
                    <select
                      value={formData.role}
                      onChange={(e) => setFormData({ ...formData, role: e.target.value as UserRole })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    >
                      <option value="Super Admin">Super Admin</option>
                      <option value="Admin Bidang">Admin Bidang</option>
                      <option value="Admin Sekretariat">Admin Sekretariat</option>
                      <option value="Admin UPTD">Admin UPTD</option>
                      <option value="Kepala Dinas">Kepala Dinas</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Unit Kerja Terkait
                    </label>
                    <select
                      disabled={['Super Admin', 'Kepala Dinas'].includes(formData.role)}
                      value={formData.unit_kerja_id || ''}
                      onChange={(e) => setFormData({ ...formData, unit_kerja_id: Number(e.target.value) })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2] disabled:opacity-50"
                    >
                      {unitKerjas.map(u => (
                        <option key={u.id} value={u.id}>{u.nama_unit}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Password Akun <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="password"
                    required
                    minLength={6}
                    placeholder="Minimal 6 karakter"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  />
                </div>

                <div className="pt-3 border-t border-[#eaeff5] dark:border-[#334155] flex items-center justify-end gap-2.5">
                  <button
                    type="button"
                    onClick={() => setIsAddModalOpen(false)}
                    className="px-4 py-2 rounded-xl text-xs font-bold text-[#7c8db5] hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors cursor-pointer"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl text-xs font-bold bg-[#2a92a2] hover:bg-[#217784] text-white shadow-xs transition-all cursor-pointer"
                  >
                    Buat Akun
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal Edit User */}
        {isEditModalOpen && editUser && (
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-[#1e293b] w-full max-w-lg rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden">
              <div className="px-6 py-4 border-b border-[#eaeff5] dark:border-[#334155] flex items-center justify-between bg-[#f2f7ff] dark:bg-slate-800">
                <div>
                  <h3 className="font-extrabold text-[#25396e] dark:text-white text-base">Edit Data Pengguna</h3>
                  <p className="text-xs text-[#7c8db5] mt-0.5">Perbarui profil, peran hak akses, atau unit kerja pengguna</p>
                </div>
                <button
                  onClick={() => setIsEditModalOpen(false)}
                  className="p-1 rounded-lg text-[#7c8db5] hover:text-[#25396e] dark:hover:text-white cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleEditSubmit} className="p-6 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Nama Lengkap <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Contoh: Budi Santoso, S.Kom."
                    value={editFormData.nama_lengkap}
                    onChange={(e) => setEditFormData({ ...editFormData, nama_lengkap: e.target.value })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Username <span className="text-rose-500">*</span>
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="admin_nama"
                      value={editFormData.username}
                      onChange={(e) => setEditFormData({ ...editFormData, username: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Email Dinas
                    </label>
                    <input
                      type="email"
                      placeholder="nama@dinperinnaker.go.id"
                      value={editFormData.email}
                      onChange={(e) => setEditFormData({ ...editFormData, email: e.target.value })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Peran (Role) <span className="text-rose-500">*</span>
                    </label>
                    <select
                      value={editFormData.role}
                      onChange={(e) => setEditFormData({ ...editFormData, role: e.target.value as UserRole })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                    >
                      <option value="Super Admin">Super Admin</option>
                      <option value="Admin Bidang">Admin Bidang</option>
                      <option value="Admin Sekretariat">Admin Sekretariat</option>
                      <option value="Admin UPTD">Admin UPTD</option>
                      <option value="Kepala Dinas">Kepala Dinas</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                      Unit Kerja Terkait
                    </label>
                    <select
                      disabled={['Super Admin', 'Kepala Dinas'].includes(editFormData.role)}
                      value={editFormData.unit_kerja_id || ''}
                      onChange={(e) => setEditFormData({ ...editFormData, unit_kerja_id: Number(e.target.value) })}
                      className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2] disabled:opacity-50"
                    >
                      {unitKerjas.map(u => (
                        <option key={u.id} value={u.id}>{u.nama_unit}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Status Akun <span className="text-rose-500">*</span>
                  </label>
                  <select
                    value={editFormData.status}
                    onChange={(e) => setEditFormData({ ...editFormData, status: e.target.value as 'Aktif' | 'Nonaktif' })}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  >
                    <option value="Aktif">Aktif</option>
                    <option value="Nonaktif">Nonaktif</option>
                  </select>
                </div>

                <div className="pt-3 border-t border-[#eaeff5] dark:border-[#334155] flex items-center justify-end gap-2.5">
                  <button
                    type="button"
                    onClick={() => setIsEditModalOpen(false)}
                    className="px-4 py-2 rounded-xl text-xs font-bold text-[#7c8db5] hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors cursor-pointer"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl text-xs font-bold bg-[#2a92a2] hover:bg-[#217784] text-white shadow-xs transition-all cursor-pointer"
                  >
                    Simpan Perubahan
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal Reset Password */}
        {isResetModalOpen && selectedUser && (
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-[#1e293b] w-full max-w-sm rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden">
              <div className="px-6 py-4 border-b border-[#eaeff5] dark:border-[#334155] flex items-center justify-between bg-[#f2f7ff] dark:bg-slate-800">
                <h3 className="font-extrabold text-[#25396e] dark:text-white text-base">Reset Password Akun</h3>
                <button
                  onClick={() => setIsResetModalOpen(false)}
                  className="p-1 rounded-lg text-[#7c8db5] hover:text-[#25396e] dark:hover:text-white cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleResetSubmit} className="p-6 space-y-4">
                <p className="text-xs text-[#7c8db5]">
                  Mengatur ulang kata sandi untuk pengguna <strong>{selectedUser.username}</strong> ({selectedUser.nama_lengkap}).
                </p>

                <div>
                  <label className="block text-xs font-bold text-[#25396e] dark:text-slate-200 mb-1">
                    Password Baru <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="password"
                    required
                    minLength={6}
                    placeholder="Minimal 6 karakter"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-3 py-2 bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] rounded-xl text-xs font-semibold text-[#25396e] dark:text-white outline-none focus:border-[#2a92a2]"
                  />
                </div>

                <div className="pt-3 border-t border-[#eaeff5] dark:border-[#334155] flex items-center justify-end gap-2.5">
                  <button
                    type="button"
                    onClick={() => setIsResetModalOpen(false)}
                    className="px-4 py-2 rounded-xl text-xs font-bold text-[#7c8db5] hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors cursor-pointer"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl text-xs font-bold bg-[#2a92a2] hover:bg-[#217784] text-white shadow-xs transition-all cursor-pointer"
                  >
                    Simpan Password
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
