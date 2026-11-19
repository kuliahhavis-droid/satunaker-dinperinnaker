'use client';

import React, { useState, useMemo } from 'react';
import AppLayout from '@/components/layout/AppLayout';
import { useData } from '@/context/DataContext';
import { Printer, Download, Filter, FileSpreadsheet, FileText, ExternalLink } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { exportSatuNakerExcel } from '@/lib/exportExcel';

export default function LaporanPage() {
  const router = useRouter();
  const { dataRecords, unitKerjas } = useData();

  // Filters state
  const [filterUnit, setFilterUnit] = useState('all');
  const [filterTahun, setFilterTahun] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [tglAwal, setTglAwal] = useState('');
  const [tglAkhir, setTglAkhir] = useState('');

  // Available years
  const availableYears = useMemo(() => {
    const defaultYears = [2026, 2025, 2024];
    const yrs = Array.from(new Set([...defaultYears, ...dataRecords.map(d => d.tahun_awal)])).sort((a, b) => b - a);
    return yrs;
  }, [dataRecords]);

  // Filtered dataset
  const filteredData = useMemo(() => {
    return dataRecords.filter(item => {
      const matchUnit = filterUnit === 'all' || item.unit_kerja_id.toString() === filterUnit;
      const matchTahun = filterTahun === 'all' || item.tahun_awal.toString() === filterTahun;
      const matchStatus = filterStatus === 'all' || item.status === filterStatus;
      
      const itemDate = item.created_at ? new Date(item.created_at) : null;
      const matchTglAwal = !tglAwal || (itemDate && itemDate >= new Date(tglAwal));
      const matchTglAkhir = !tglAkhir || (itemDate && itemDate <= new Date(tglAkhir + 'T23:59:59'));

      return matchUnit && matchTahun && matchStatus && matchTglAwal && matchTglAkhir;
    });
  }, [dataRecords, filterUnit, filterTahun, filterStatus, tglAwal, tglAkhir]);

  const totalItem = filteredData.length;
  const totalNilai = filteredData.reduce((acc, curr) => acc + (curr.jumlah || 0), 0);
  const totalAktif = filteredData.filter(d => d.status === 'Aktif').length;

  // Handle Print Action
  const handlePrint = () => {
    const params = new URLSearchParams();
    if (filterUnit !== 'all') params.set('unit', filterUnit);
    if (filterTahun !== 'all') params.set('tahun', filterTahun);
    if (filterStatus !== 'all') params.set('status', filterStatus);
    if (tglAwal) params.set('tgl_awal', tglAwal);
    if (tglAkhir) params.set('tgl_akhir', tglAkhir);

    router.push(`/laporan/print?${params.toString()}`);
  };

  // Handle Excel Export (.xlsx)
  const handleExportExcel = () => {
    try {
      if (filteredData.length === 0) {
        toast.info('Tidak ada data yang sesuai dengan kriteria filter untuk diekspor.');
        return;
      }

      const filename = exportSatuNakerExcel({
        records: filteredData,
        unitKerjas,
        filterUnit,
        filterTahun,
        filterStatus,
        tglAwal,
        tglAkhir,
      });

      toast.success(`Berkas Excel berhasil diunduh: ${filename}`);
    } catch (err: any) {
      toast.error(err?.message || 'Gagal mengekspor berkas Excel.');
    }
  };

  return (
    <AppLayout title="Laporan Kinerja Sektoral">
      <div className="space-y-6">
        {/* Header Action Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-[#1e293b] p-6 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs">
          <div>
            <h2 className="text-xl font-extrabold text-[#25396e] dark:text-white tracking-tight">
              Laporan Terpadu SatuNaker DINPERINNAKER
            </h2>
            <p className="text-xs text-[#7c8db5] font-medium mt-1">
              Pratinjau data kinerja, cetak format dinas resmi, dan unduh berkas spreadsheet Excel
            </p>
          </div>

          <div className="flex items-center gap-2.5 self-start sm:self-auto">
            {/* Print Button */}
            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] hover:border-[#2a92a2] text-[#25396e] dark:text-slate-200 hover:text-[#2a92a2] text-xs font-bold transition-all shadow-xs cursor-pointer"
            >
              <Printer className="w-4 h-4 text-[#2a92a2]" />
              <span>Cetak / PDF Resmi</span>
            </button>

            {/* Export Excel Button */}
            <button
              onClick={handleExportExcel}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition-all shadow-xs cursor-pointer"
            >
              <FileSpreadsheet className="w-4 h-4" />
              <span>Ekspor Excel (.xlsx)</span>
            </button>
          </div>
        </div>

        {/* Filter Panel */}
        <div className="bg-white dark:bg-[#1e293b] p-5 rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold text-[#25396e] dark:text-white">
            <Filter className="w-4 h-4 text-[#2a92a2]" />
            <span>Kriteria Penyaringan Laporan</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-[#7c8db5] mb-1">Unit Kerja:</label>
              <select
                value={filterUnit}
                onChange={(e) => setFilterUnit(e.target.value)}
                className="w-full bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2]"
              >
                <option value="all">Semua Unit Kerja</option>
                {unitKerjas.map(u => (
                  <option key={u.id} value={u.id.toString()}>{u.nama_unit}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-[#7c8db5] mb-1">Tahun Laporan:</label>
              <select
                value={filterTahun}
                onChange={(e) => setFilterTahun(e.target.value)}
                className="w-full bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2]"
              >
                <option value="all">Semua Tahun</option>
                {availableYears.map(yr => (
                  <option key={yr} value={yr.toString()}>{yr}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-[#7c8db5] mb-1">Status Data:</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 outline-none focus:border-[#2a92a2]"
              >
                <option value="all">Semua Status</option>
                <option value="Aktif">Aktif</option>
                <option value="Tidak Aktif">Tidak Aktif</option>
                <option value="Arsip">Arsip</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-[#7c8db5] mb-1">Tanggal Awal:</label>
              <input
                type="date"
                value={tglAwal}
                onChange={(e) => setTglAwal(e.target.value)}
                className="w-full bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-1.5 outline-none focus:border-[#2a92a2]"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-[#7c8db5] mb-1">Tanggal Akhir:</label>
              <input
                type="date"
                value={tglAkhir}
                onChange={(e) => setTglAkhir(e.target.value)}
                className="w-full bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-[#25396e] dark:text-slate-200 text-xs font-semibold rounded-xl px-3 py-1.5 outline-none focus:border-[#2a92a2]"
              />
            </div>
          </div>

          {/* Quick Metrics of filtered data */}
          <div className="pt-3 border-t border-[#eaeff5] dark:border-[#334155] flex flex-wrap gap-4 text-xs font-semibold">
            <span className="text-[#7c8db5]">
              Jumlah Data: <strong className="text-[#25396e] dark:text-white">{totalItem}</strong>
            </span>
            <span className="text-[#7c8db5]">
              Data Aktif: <strong className="text-emerald-600">{totalAktif}</strong>
            </span>
            <span className="text-[#7c8db5]">
              Akumulasi Capaian: <strong className="text-[#2a92a2]">{totalNilai.toLocaleString('id-ID')}</strong>
            </span>
          </div>
        </div>

        {/* Report Preview Table */}
        <div className="bg-white dark:bg-[#1e293b] rounded-2xl border border-[#eaeff5] dark:border-[#334155] shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#f2f7ff] dark:bg-slate-800/80 text-[#25396e] dark:text-slate-200 uppercase tracking-wider font-bold border-b border-[#eaeff5] dark:border-[#334155]">
                <tr>
                  <th className="px-4 py-3.5 w-12 text-center">No</th>
                  <th className="px-4 py-3.5 min-w-[200px]">Unit Kerja</th>
                  <th className="px-4 py-3.5 min-w-[280px]">Nama Data / Indikator</th>
                  <th className="px-4 py-3.5 text-center">Satuan</th>
                  <th className="px-4 py-3.5 text-center">Tahun</th>
                  <th className="px-4 py-3.5 text-right">Jumlah</th>
                  <th className="px-4 py-3.5 text-center">Status</th>
                  <th className="px-4 py-3.5 text-center">Dokumen Rincian</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#eaeff5] dark:divide-[#334155] font-medium text-[#25396e] dark:text-slate-200">
                {filteredData.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-12 text-center text-[#7c8db5]">
                      <FileText className="w-10 h-10 mx-auto text-[#cbd5e1] mb-2" />
                      Tidak ada rekaman data yang cocok dengan kriteria filter.
                    </td>
                  </tr>
                ) : (
                  filteredData.map((item, index) => {
                    const unit = unitKerjas.find(u => u.id === item.unit_kerja_id);
                    return (
                      <tr key={item.id} className="hover:bg-[#f2f7ff]/50 dark:hover:bg-slate-800/50 transition-colors">
                        <td className="px-4 py-3 text-center text-[#7c8db5] font-semibold">{index + 1}</td>
                        <td className="px-4 py-3 font-bold text-[#25396e] dark:text-white">{unit?.nama_unit}</td>
                        <td className="px-4 py-3 font-semibold">{item.nama_data}</td>
                        <td className="px-4 py-3 text-center text-[#7c8db5]">{item.satuan}</td>
                        <td className="px-4 py-3 text-center font-bold text-[#2a92a2]">{item.tahun_awal}</td>
                        <td className="px-4 py-3 text-right font-black">{item.jumlah.toLocaleString('id-ID')}</td>
                        <td className="px-4 py-3 text-center">
                          <span className={`
                            inline-block px-2 py-0.5 rounded-full text-[10px] font-bold
                            ${item.status === 'Aktif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'}
                          `}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center">
                          {item.link_gdrive ? (
                            <a
                              href={item.link_gdrive.startsWith('http') ? item.link_gdrive : `https://${item.link_gdrive}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#e6f4f6] dark:bg-slate-800 text-[#2a92a2] hover:bg-[#2a92a2] hover:text-white dark:hover:bg-[#2a92a2] dark:hover:text-white text-[11px] font-bold transition-all shadow-2xs group"
                              title={item.link_gdrive}
                            >
                              <ExternalLink className="w-3.5 h-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                              <span>Buka Berkas</span>
                            </a>
                          ) : (
                            <span className="text-[#cbd5e1] dark:text-slate-600 font-semibold">-</span>
                          )}
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
