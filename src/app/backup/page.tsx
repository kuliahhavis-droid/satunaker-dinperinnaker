'use client';

import React, { useState, useRef } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { Download, Upload, Database, ShieldCheck, Trash2, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import confetti from 'canvas-confetti';
import { toast } from 'sonner';

export default function BackupPage() {
  const { unitKerjas, users, dataRecords, logs, currentUser, clearLogs, addLog, restoreSQLBackup } = useData();
  const [restoreMessage, setRestoreMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isRestoring, setIsRestoring] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isSuperAdmin = currentUser?.role === 'Super Admin';

  // Generate and Download SQL Backup on the fly
  const handleDownloadSQL = () => {
    let sql = `-- ========================================================\n`;
    sql += `-- SISTEM SATUNAKER DINPERINNAKER PURBALINGGA\n`;
    sql += `-- Next.js + Supabase SQL Backup\n`;
    sql += `-- Tanggal Cadangan: ${new Date().toISOString()}\n`;
    sql += `-- ========================================================\n\n`;

    // 1. unit_kerja
    sql += `-- 1. UNIT KERJA\n`;
    sql += `TRUNCATE TABLE unit_kerja CASCADE;\n`;
    unitKerjas.forEach(u => {
      sql += `INSERT INTO unit_kerja (id, nama_unit, tipe) VALUES (${u.id}, '${u.nama_unit.replace(/'/g, "''")}', '${u.tipe}');\n`;
    });
    sql += `\n`;

    // 2. data_records
    sql += `-- 2. DATA RECORDS\n`;
    sql += `TRUNCATE TABLE data_records CASCADE;\n`;
    dataRecords.forEach(d => {
      const gdrive = d.link_gdrive ? `'${d.link_gdrive.replace(/'/g, "''")}'` : 'NULL';
      const desk = d.deskripsi ? `'${d.deskripsi.replace(/'/g, "''")}'` : 'NULL';
      sql += `INSERT INTO data_records (id, unit_kerja_id, nama_data, satuan, tahun_awal, jumlah, link_gdrive, deskripsi, status) VALUES (${d.id}, ${d.unit_kerja_id}, '${d.nama_data.replace(/'/g, "''")}', '${d.satuan.replace(/'/g, "''")}', ${d.tahun_awal}, ${d.jumlah}, ${gdrive}, ${desk}, '${d.status}');\n`;
    });
    sql += `\n`;

    // 3. profiles
    sql += `-- 3. PROFIL PENGGUNA\n`;
    users.forEach(u => {
      const unitVal = u.unit_kerja_id ? u.unit_kerja_id : 'NULL';
      sql += `INSERT INTO profiles (id, nama_lengkap, username, email, role, unit_kerja_id, status) VALUES ('${u.id}', '${u.nama_lengkap.replace(/'/g, "''")}', '${u.username.replace(/'/g, "''")}', '${u.email.replace(/'/g, "''")}', '${u.role}', ${unitVal}, '${u.status}');\n`;
    });
    sql += `\n`;

    // Download blob
    const blob = new Blob([sql], { type: 'application/sql;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Backup_SatuNaker_DINPERINNAKER_${new Date().toISOString().slice(0, 10)}.sql`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    // Confetti effect
    confetti({
      particleCount: 70,
      spread: 60,
      origin: { y: 0.7 }
    });

    toast.success('Berkas cadangan SQL lengkap berhasil dibuat dan diunduh.');
    addLog(`Super Admin mengunduh berkas cadangan database SQL`);
  };

  // Generate and Download JSON Backup
  const handleDownloadJSON = () => {
    const backupData = {
      app: 'SatuNaker DINPERINNAKER Purbalingga',
      version: '2.0',
      exported_at: new Date().toISOString(),
      unitKerjas,
      users: users.map(u => ({ ...u, password: undefined })),
      dataRecords,
      logs: logs.slice(0, 200),
    };

    const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Snapshot_SatuNaker_DINPERINNAKER_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    confetti({
      particleCount: 70,
      spread: 60,
      origin: { y: 0.7 }
    });

    toast.success('Berkas snapshot JSON berhasil dibuat dan diunduh.');
    addLog(`Super Admin mengunduh berkas cadangan format JSON`);
  };

  // Restore File (Supports .sql and .json)
  const handleRestoreFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsRestoring(true);
    setRestoreMessage(null);

    try {
      const text = await file.text();
      const isJson = file.name.toLowerCase().endsWith('.json');

      if (isJson) {
        const json = JSON.parse(text);
        if (!json.unitKerjas && !json.dataRecords) {
          throw new Error('Format berkas JSON bukan cadangan SatuNaker yang valid.');
        }
        if (json.unitKerjas) {
          localStorage.setItem('satudata_units', JSON.stringify(json.unitKerjas));
        }
        if (json.dataRecords) {
          localStorage.setItem('satudata_records', JSON.stringify(json.dataRecords));
        }
        if (json.users) {
          localStorage.setItem('satudata_users', JSON.stringify(json.users));
        }
        window.location.reload();
        return;
      }

      const res = await restoreSQLBackup(text);
      if (res.success) {
        setRestoreMessage({ type: 'success', text: res.message });
        toast.success(res.message);
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      } else {
        setRestoreMessage({ type: 'error', text: res.message });
        toast.error(res.message);
      }
    } catch (err: any) {
      const msg = err.message || 'Gagal memproses file cadangan.';
      setRestoreMessage({ type: 'error', text: msg });
      toast.error(msg);
    } finally {
      setIsRestoring(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleClearLogsKeep5 = () => {
    clearLogs(true);
    toast.success('Log aktivitas dibersihkan, 5 aktivitas terbaru dipertahankan.');
  };

  const handleClearAllLogs = () => {
    if (confirm('Kosongkan seluruh riwayat log audit?')) {
      clearLogs(false);
      toast.success('Seluruh riwayat log audit telah dikosongkan.');
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
    <AppLayout title="Backup & Pemeliharaan Sistem">
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
          <h2 className="text-xl font-bold text-slate-800 dark:text-white tracking-tight">
            Pencadangan Database & Audit Trail
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-1">
            Unduh cadangan data SQL terpadu, pulihkan data, dan pantau seluruh riwayat aktivitas sistem
          </p>
        </div>

        {/* Restore Notification Feedback */}
        {restoreMessage && (
          <div className={`p-4 rounded-2xl flex items-center gap-3 text-xs font-semibold ${
            restoreMessage.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900'
              : 'bg-rose-50 text-rose-800 border border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-900'
          }`}>
            {restoreMessage.type === 'success' ? (
              <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600" />
            ) : (
              <AlertCircle className="w-5 h-5 shrink-0 text-rose-600" />
            )}
            <span>{restoreMessage.text}</span>
          </div>
        )}

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Download SQL & JSON */}
          <div className="bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4">
                <Database className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-800 dark:text-white">Cadangkan Data (SQL & JSON)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
                Menghasilkan berkas skrip SQL atau snapshot JSON terpadu berisikan Unit Kerja, Pengguna, dan Data Sektoral.
              </p>
            </div>

            <div className="pt-6 space-y-2">
              <button
                onClick={handleDownloadSQL}
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-[#0d6b63] hover:bg-[#0a5851] text-white text-xs font-bold transition-all shadow-xs cursor-pointer"
              >
                <Download className="w-4 h-4" />
                <span>Unduh Berkas SQL (.sql)</span>
              </button>
              <button
                onClick={handleDownloadJSON}
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold transition-all cursor-pointer"
              >
                <Download className="w-4 h-4 text-emerald-600" />
                <span>Unduh Snapshot JSON (.json)</span>
              </button>
            </div>
          </div>

          {/* Card 2: Restore SQL / JSON */}
          <div className="bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-sky-50 dark:bg-sky-950/40 text-sky-600 dark:text-sky-400 flex items-center justify-center mb-4">
                <Upload className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-800 dark:text-white">Pulihkan Basis Data (Restore)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
                Pulihkan data unit kerja, pengguna, dan data sektoral dari berkas cadangan SQL atau JSON hasil ekspor.
              </p>
            </div>

            <div className="pt-6">
              <input
                ref={fileInputRef}
                type="file"
                accept=".sql,.json"
                onChange={handleRestoreFile}
                className="hidden"
                id="restore-sql-upload"
              />
              <button
                disabled={isRestoring}
                onClick={() => fileInputRef.current?.click()}
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-700 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-xs cursor-pointer"
              >
                <Upload className="w-4 h-4" />
                <span>{isRestoring ? 'Memproses...' : 'Unggah Berkas (.sql / .json)'}</span>
              </button>
            </div>
          </div>

          {/* Card 3: Log Maintenance */}
          <div className="bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center mb-4">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-800 dark:text-white">Pemeliharaan Log Audit</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
                Sistem mempertahankan 300 log terakhir. Anda dapat membersihkan riwayat lama sewaktu-waktu.
              </p>
            </div>

            <div className="pt-6 flex gap-2">
              <button
                onClick={handleClearLogsKeep5}
                className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 text-amber-800 dark:text-amber-300 text-xs font-bold transition-all cursor-pointer"
              >
                <Clock className="w-4 h-4" />
                <span>Simpan 5 Terbaru</span>
              </button>
              <button
                onClick={handleClearAllLogs}
                className="inline-flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-rose-700 dark:text-rose-300 text-xs font-bold transition-all cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
                <span>Hapus Semua</span>
              </button>
            </div>
          </div>
        </div>

        {/* Audit Trail Table */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200/80 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-800/50 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-800 dark:text-white">Riwayat Aktivitas Sistem (Audit Trail)</h3>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">Menampilkan rekam jejak pengguna terbaru</p>
            </div>
            <span className="text-xs font-semibold text-slate-500">
              Total: <strong className="text-slate-800 dark:text-white">{logs.length}</strong> Aktivitas
            </span>
          </div>

          <div className="overflow-x-auto max-h-[400px]">
            <table className="w-full text-left text-xs">
              <thead className="bg-white dark:bg-[#1e293b] text-slate-500 uppercase font-bold sticky top-0 border-b border-slate-200/80 dark:border-slate-800">
                <tr>
                  <th className="px-4 py-3 w-12 text-center">No</th>
                  <th className="px-4 py-3 w-36">Pengguna</th>
                  <th className="px-4 py-3">Rincian Aktivitas</th>
                  <th className="px-4 py-3 w-44">Waktu</th>
                  <th className="px-4 py-3 w-28 text-center">IP Address</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-medium text-slate-700 dark:text-slate-200">
                {logs.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-8 text-center text-slate-400 italic">
                      Riwayat log audit masih kosong.
                    </td>
                  </tr>
                ) : (
                  logs.map((log, index) => (
                    <tr key={log.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-800/50 transition-colors">
                      <td className="px-4 py-2.5 text-center text-slate-400">{index + 1}</td>
                      <td className="px-4 py-2.5 font-bold text-[#0d6b63]">@{log.user}</td>
                      <td className="px-4 py-2.5">{log.aktivitas}</td>
                      <td className="px-4 py-2.5 text-slate-500">
                        {new Date(log.tanggal).toLocaleString('id-ID')}
                      </td>
                      <td className="px-4 py-2.5 text-center text-slate-400 font-mono text-[11px]">
                        {log.ip_address || '127.0.0.1'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
