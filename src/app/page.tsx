'use client';

import React, { useState, useMemo } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { motion } from 'framer-motion';
import { 
  Building2, 
  Database, 
  Users, 
  Link2, 
  Plus, 
  FileText, 
  BarChart3, 
  Zap, 
  ChevronRight,
  Printer,
  Calendar,
  ExternalLink,
  ArrowRight,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { unitKerjas, dataRecords, users, currentUser } = useData();
  const [selectedYear, setSelectedYear] = useState<string>('all');

  const isSuperAdmin = currentUser?.role === 'Super Admin';
  const isKadis = currentUser?.role === 'Kepala Dinas';

  const userUnit = useMemo(() => unitKerjas.find(u => u.id === currentUser?.unit_kerja_id), [unitKerjas, currentUser]);
  const userUnitRecords = useMemo(() => dataRecords.filter(d => d.unit_kerja_id === currentUser?.unit_kerja_id), [dataRecords, currentUser]);

  // Available unique years
  const availableYears = useMemo(() => {
    const yrs = Array.from(new Set(dataRecords.map(d => d.tahun_awal))).sort((a, b) => b - a);
    if (!yrs.includes(2026)) yrs.unshift(2026);
    if (!yrs.includes(2025)) yrs.push(2025);
    if (!yrs.includes(2024)) yrs.push(2024);
    return yrs.sort((a, b) => b - a);
  }, [dataRecords]);

  // Filtered records by selected year
  const filteredRecords = useMemo(() => {
    if (selectedYear === 'all') return dataRecords;
    return dataRecords.filter(d => d.tahun_awal.toString() === selectedYear);
  }, [dataRecords, selectedYear]);

  // Dynamic metrics from realtime data
  const totalUnitKerja = unitKerjas.length;
  const totalDataCount = filteredRecords.length;
  const totalPengguna = users.length;
  const totalDriveLinks = filteredRecords.filter(d => Boolean(d.link_gdrive)).length;
  const drivePercentage = totalDataCount > 0 ? Math.round((totalDriveLinks / totalDataCount) * 100) : 0;
  const totalAktif = filteredRecords.filter(d => d.status === 'Aktif').length;

  // Distribution by unit kerja from live data
  const distributionData = useMemo(() => {
    if (!unitKerjas || unitKerjas.length === 0) return [];

    return unitKerjas.map(u => {
      const count = filteredRecords.filter(r => r.unit_kerja_id === u.id).length;
      return {
        id: u.id,
        name: u.nama_unit,
        count,
      };
    }).sort((a, b) => b.count - a.count);
  }, [unitKerjas, filteredRecords]);

  const maxDistributionCount = Math.max(...distributionData.map(d => d.count), 1);

  // 5 Latest Sectoral Records (Sorted newest first)
  const latestRecords = useMemo(() => {
    const list = selectedYear === 'all' ? dataRecords : filteredRecords;
    const sorted = [...list].sort((a, b) => {
      const timeA = a.created_at ? new Date(a.created_at).getTime() : a.id;
      const timeB = b.created_at ? new Date(b.created_at).getTime() : b.id;
      return timeB - timeA;
    });
    return sorted.slice(0, 5);
  }, [dataRecords, filteredRecords, selectedYear]);

  // Alternating bar colors matching reference design
  const barColors = ['#0d6b63', '#ea580c', '#2563eb', '#7c3aed', '#059669'];

  return (
    <AppLayout title="Dashboard SatuNaker">
      <div className="space-y-6">
        
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold text-slate-800 dark:text-white tracking-tight">
                Dashboard SatuNaker
              </h1>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Portal data terpadu Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            {/* Year Selector */}
            <div className="relative">
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
                className="appearance-none bg-white dark:bg-[#1e293b] border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold rounded-xl pl-3 pr-8 py-2 shadow-2xs hover:border-slate-300 dark:hover:border-slate-600 transition-colors cursor-pointer outline-none focus:ring-1 focus:ring-[#0d6b63]"
              >
                <option value="all">Semua Tahun</option>
                {availableYears.map(yr => (
                  <option key={yr} value={yr.toString()}>Tahun {yr}</option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2.5 text-slate-400">
                <Calendar className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Input Data Button */}
            <Link
              href="/kelola-data"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#0d6b63] hover:bg-[#0a5851] text-white text-xs font-bold shadow-xs transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>+ Input Data</span>
            </Link>

            {/* Laporan Button */}
            <Link
              href="/laporan"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white dark:bg-[#1e293b] hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 text-xs font-bold shadow-2xs transition-all cursor-pointer"
            >
              <FileText className="w-3.5 h-3.5 text-slate-500" />
              <span>Laporan</span>
            </Link>
          </div>
        </div>

        {/* Executive Banner for Kepala Dinas */}
        {isKadis && (
          <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-between">
            <div className="text-xs">
              <span className="font-bold text-amber-700 dark:text-amber-400">Mode Pimpinan Eksekutif:</span>
              <span className="text-slate-600 dark:text-slate-300 ml-1.5">{currentUser?.nama_lengkap || 'Johan Arifin, S.Sos., M.Si. (Kepala Dinas)'}</span>
            </div>
            <Link
              href="/laporan/print"
              target="_blank"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold transition-all shadow-xs"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Cetak Rekap</span>
            </Link>
          </div>
        )}

        {/* Unit Kerja Admin Banner */}
        {!isSuperAdmin && !isKadis && userUnit && (
          <div className="p-4 rounded-2xl bg-teal-500/10 border border-teal-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="text-xs">
              <span className="font-bold text-teal-800 dark:text-teal-300">Unit Bertugas:</span>
              <span className="text-slate-700 dark:text-slate-200 font-semibold ml-1.5">{userUnit.nama_unit}</span>
              <span className="text-slate-500 dark:text-slate-400 ml-2">({userUnitRecords.length} indikator tercatat)</span>
            </div>
            <Link
              href="/kelola-data"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0d6b63] hover:bg-[#0a5851] text-white text-xs font-bold transition-all shadow-xs self-start sm:self-auto cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Kelola Data Unit Anda</span>
            </Link>
          </div>
        )}

        {/* 4 Metric Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Card 1: Unit Kerja */}
          <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-2xs">
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-xl bg-[#ecfdf5] dark:bg-emerald-950/40 text-[#10b981] flex items-center justify-center shrink-0">
                <Building2 className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400 truncate">Unit Kerja</p>
                <h3 className="text-2xl font-bold text-slate-800 dark:text-white leading-tight mt-0.5">
                  {totalUnitKerja}
                </h3>
              </div>
            </div>
          </div>

          {/* Card 2: Total Data */}
          <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-2xs">
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-xl bg-[#f0f9ff] dark:bg-sky-950/40 text-[#0284c7] flex items-center justify-center shrink-0">
                <Database className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400 truncate">Total Data</p>
                <div className="flex items-baseline gap-2 mt-0.5">
                  <h3 className="text-2xl font-bold text-slate-800 dark:text-white leading-tight">
                    {totalDataCount}
                  </h3>
                  <span className="text-[10px] text-sky-600 font-semibold bg-sky-50 dark:bg-sky-950/50 px-1.5 py-0.5 rounded-md">
                    {totalAktif} Aktif
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 3: Bukti Drive */}
          <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-2xs">
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-xl bg-[#fffbeb] dark:bg-amber-950/40 text-[#d97706] flex items-center justify-center shrink-0">
                <Link2 className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400 truncate">Tautan Drive</p>
                <div className="flex items-baseline gap-2 mt-0.5">
                  <h3 className="text-2xl font-bold text-slate-800 dark:text-white leading-tight">
                    {totalDriveLinks}
                  </h3>
                  <span className="text-[10px] text-amber-600 font-semibold bg-amber-50 dark:bg-amber-950/50 px-1.5 py-0.5 rounded-md">
                    {drivePercentage}%
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 4: Pengguna */}
          <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-2xs">
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-xl bg-[#faf5ff] dark:bg-purple-950/40 text-[#9333ea] flex items-center justify-center shrink-0">
                <Users className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400 truncate">Pengguna Sistem</p>
                <h3 className="text-2xl font-bold text-slate-800 dark:text-white leading-tight mt-0.5">
                  {totalPengguna}
                </h3>
              </div>
            </div>
          </div>
        </div>

        {/* Two Columns: Distribusi per Unit Kerja (Kiri) & Status Bukti & Akses Cepat (Kanan) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Kolom Kiri: Distribusi Data per Unit Kerja */}
          <div className="lg:col-span-7 bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-2xs space-y-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-teal-50 dark:bg-teal-950/50 text-[#0d6b63] dark:text-teal-400 flex items-center justify-center shrink-0">
                  <BarChart3 className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white leading-tight">
                    Distribusi Data per Unit Kerja
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Jumlah capaian indikator per unit
                  </p>
                </div>
              </div>
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                {totalDataCount} Total
              </span>
            </div>

            <div className="space-y-4 pt-1">
              {distributionData.length === 0 ? (
                <p className="text-xs text-slate-400 py-6 text-center">Belum ada data pada tahun yang dipilih.</p>
              ) : (
                distributionData.map((d, index) => {
                  const percentage = totalDataCount > 0 ? Math.round((d.count / totalDataCount) * 100) : 0;
                  const barColor = barColors[index % barColors.length];

                  return (
                    <div key={d.id} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-medium text-slate-700 dark:text-slate-300 truncate pr-4">
                          {d.name}
                        </span>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className="text-[11px] text-slate-400 font-mono">
                            {percentage}%
                          </span>
                          <span className="font-bold text-slate-800 dark:text-slate-100 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded-md text-xs">
                            {d.count}
                          </span>
                        </div>
                      </div>

                      <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.max(percentage, d.count > 0 ? 6 : 0)}%` }}
                          transition={{ duration: 0.5, ease: 'easeOut', delay: index * 0.04 }}
                          className="h-full rounded-full"
                          style={{ backgroundColor: barColor }}
                        />
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Kolom Kanan: Kelengkapan Bukti & Akses Cepat */}
          <div className="lg:col-span-5 space-y-6">
            
            {/* Box Kepatuhan Bukti Digital */}
            <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-2xs">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/50 text-[#d97706] dark:text-amber-400 flex items-center justify-center shrink-0">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white leading-tight">
                    Bukti Dukung Digital
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Ketersediaan berkas Google Drive
                  </p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-baseline justify-between text-xs">
                  <span className="text-slate-600 dark:text-slate-300 font-medium">Tingkat Kelengkapan:</span>
                  <span className="font-bold text-amber-600 dark:text-amber-400">
                    {drivePercentage}% Lengkap
                  </span>
                </div>

                <div className="w-full h-2.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${drivePercentage}%` }}
                    transition={{ duration: 0.5, ease: 'easeOut' }}
                    className="h-full rounded-full bg-gradient-to-r from-amber-500 to-emerald-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2 pt-2">
                  <div className="p-2.5 rounded-xl bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-100 dark:border-emerald-900/40 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    <div>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400">Ada Bukti</p>
                      <p className="text-xs font-bold text-emerald-700 dark:text-emerald-300">{totalDriveLinks} Data</p>
                    </div>
                  </div>

                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-slate-400 shrink-0" />
                    <div>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400">Belum Ada</p>
                      <p className="text-xs font-bold text-slate-700 dark:text-slate-300">{Math.max(totalDataCount - totalDriveLinks, 0)} Data</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Box Akses Cepat */}
            <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-2xs">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl bg-teal-50 dark:bg-teal-950/50 text-[#0d6b63] dark:text-teal-400 flex items-center justify-center shrink-0">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-800 dark:text-white leading-tight">
                    Akses Cepat
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Navigasi ke menu utama
                  </p>
                </div>
              </div>

              <div className="space-y-2.5">
                <Link 
                  href="/kelola-data"
                  className="flex items-center justify-between p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 hover:bg-slate-100/70 dark:bg-slate-800/40 dark:hover:bg-slate-800 transition-colors group cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 flex items-center justify-center shrink-0">
                      <Database className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="text-xs font-bold text-slate-800 dark:text-white group-hover:text-[#0d6b63] transition-colors">
                        Kelola Data
                      </h3>
                      <p className="text-[11px] text-slate-400">Input & impor data Excel/CSV</p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-[#0d6b63] transition-all" />
                </Link>

                <Link 
                  href="/laporan"
                  className="flex items-center justify-between p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 hover:bg-slate-100/70 dark:bg-slate-800/40 dark:hover:bg-slate-800 transition-colors group cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 flex items-center justify-center shrink-0">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="text-xs font-bold text-slate-800 dark:text-white group-hover:text-blue-600 transition-colors">
                        Laporan & Ekspor
                      </h3>
                      <p className="text-[11px] text-slate-400">Cetak rekap dinas & ekspor Excel</p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-blue-600 transition-all" />
                </Link>

                {isSuperAdmin && (
                  <Link 
                    href="/unit-kerja"
                    className="flex items-center justify-between p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 hover:bg-slate-100/70 dark:bg-slate-800/40 dark:hover:bg-slate-800 transition-colors group cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-purple-50 dark:bg-purple-950/40 text-purple-600 flex items-center justify-center shrink-0">
                        <Building2 className="w-4 h-4" />
                      </div>
                      <div>
                        <h3 className="text-xs font-bold text-slate-800 dark:text-white group-hover:text-purple-600 transition-colors">
                          Manajemen Unit Kerja
                        </h3>
                        <p className="text-[11px] text-slate-400">Bidang, Sekretariat, dan UPTD</p>
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-purple-600 transition-all" />
                  </Link>
                )}
              </div>
            </div>

          </div>

        </div>

        {/* Tabel Ringkas: 5 Dataset Sektoral Terkini */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 sm:p-6 shadow-2xs space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-800 dark:text-white leading-tight">
                Dataset Sektoral Terkini
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                5 indikator data terbaru yang tercatat pada sistem
              </p>
            </div>

            <Link
              href="/kelola-data"
              className="inline-flex items-center gap-1 text-xs font-bold text-[#0d6b63] dark:text-teal-400 hover:underline"
            >
              <span>Lihat Semua</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-100 dark:border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider font-semibold">
                  <th className="py-2.5 px-3">Nama Data / Indikator</th>
                  <th className="py-2.5 px-3">Unit Kerja</th>
                  <th className="py-2.5 px-3 text-right">Capaian</th>
                  <th className="py-2.5 px-3 text-center">Tahun</th>
                  <th className="py-2.5 px-3 text-center">Tautan Drive</th>
                  <th className="py-2.5 px-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">
                {latestRecords.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-slate-400">
                      Tidak ada data untuk tahun yang dipilih.
                    </td>
                  </tr>
                ) : (
                  latestRecords.map((item) => {
                    const unit = unitKerjas.find(u => u.id === item.unit_kerja_id);
                    return (
                      <tr key={item.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors">
                        <td className="py-3 px-3 font-medium text-slate-800 dark:text-slate-200 max-w-xs truncate">
                          {item.nama_data}
                        </td>
                        <td className="py-3 px-3">
                          <span className="inline-block px-2 py-0.5 rounded-md text-[10px] font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 truncate max-w-[190px]">
                            {unit?.nama_unit || `Unit #${item.unit_kerja_id}`}
                          </span>
                        </td>
                        <td className="py-3 px-3 text-right font-bold text-slate-800 dark:text-white font-mono">
                          {item.jumlah.toLocaleString('id-ID')} <span className="text-[10px] font-normal text-slate-400">{item.satuan}</span>
                        </td>
                        <td className="py-3 px-3 text-center font-medium text-slate-600 dark:text-slate-300">
                          {item.tahun_awal}
                        </td>
                        <td className="py-3 px-3 text-center">
                          {item.link_gdrive ? (
                            <a
                              href={item.link_gdrive}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 hover:text-blue-800 dark:text-blue-400 hover:underline"
                            >
                              <span>Drive</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          ) : (
                            <span className="text-slate-300 dark:text-slate-600">-</span>
                          )}
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                            item.status === 'Aktif'
                              ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400'
                              : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                          }`}>
                            {item.status}
                          </span>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </AppLayout>
  );
}
