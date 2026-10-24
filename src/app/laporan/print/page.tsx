'use client';

import React, { useMemo, Suspense, useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useData } from '@/context/DataContext';
import { Printer, ArrowLeft } from 'lucide-react';

function PrintContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { dataRecords, unitKerjas, users } = useData();
  const [formattedDate, setFormattedDate] = useState('21 Oktober 2026');

  useEffect(() => {
    try {
      setFormattedDate(new Intl.DateTimeFormat('id-ID', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      }).format(new Date()));
    } catch (e) {
      // fallback
    }
  }, []);

  const unitParam = searchParams.get('unit') || 'all';
  const tahunParam = searchParams.get('tahun') || 'all';
  const statusParam = searchParams.get('status') || 'all';
  const tglAwalParam = searchParams.get('tgl_awal') || '';
  const tglAkhirParam = searchParams.get('tgl_akhir') || '';

  const selectedUnit = useMemo(() => {
    if (unitParam === 'all') return null;
    return unitKerjas.find(u => u.id.toString() === unitParam);
  }, [unitKerjas, unitParam]);

  const kadis = useMemo(() => {
    return users.find(u => u.role === 'Kepala Dinas') || {
      nama_lengkap: 'Johan Arifin, S.Sos., M.Si.',
      role: 'Kepala Dinas',
    };
  }, [users]);

  // Filtered dataset
  const filteredData = useMemo(() => {
    return dataRecords.filter(item => {
      const matchUnit = unitParam === 'all' || item.unit_kerja_id.toString() === unitParam;
      const matchTahun = tahunParam === 'all' || item.tahun_awal.toString() === tahunParam;
      const matchStatus = statusParam === 'all' || item.status === statusParam;

      // Filter tanggal Laravel identik
      let matchTglAwal = true;
      if (tglAwalParam && item.created_at) {
        matchTglAwal = new Date(item.created_at) >= new Date(tglAwalParam);
      }
      let matchTglAkhir = true;
      if (tglAkhirParam && item.created_at) {
        const dEnd = new Date(tglAkhirParam);
        dEnd.setHours(23, 59, 59, 999);
        matchTglAkhir = new Date(item.created_at) <= dEnd;
      }

      return matchUnit && matchTahun && matchStatus && matchTglAwal && matchTglAkhir;
    });
  }, [dataRecords, unitParam, tahunParam, statusParam, tglAwalParam, tglAkhirParam]);

  return (
    <div className="min-h-screen bg-[#f2f7ff] dark:bg-[#0b1120] text-black p-4 sm:p-8 font-sans print:p-0 print:bg-white print:text-black transition-colors">
      {/* Action Toolbar (Hidden during print) */}
      <div className="no-print max-w-5xl mx-auto mb-6 p-4 rounded-2xl bg-white dark:bg-[#1e293b] border border-[#eaeff5] dark:border-[#334155] flex items-center justify-between shadow-xs">
        <button
          onClick={() => router.push('/laporan')}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#f2f7ff] dark:bg-slate-800 border border-[#eaeff5] dark:border-[#334155] text-xs font-bold text-[#25396e] dark:text-slate-200 hover:bg-[#e6f4f6] transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Kembali ke Laporan</span>
        </button>

        <button
          onClick={() => window.print()}
          className="inline-flex items-center gap-2 px-5 py-2 rounded-xl bg-[#2a92a2] hover:bg-[#217784] text-white text-xs font-bold shadow-xs transition-all cursor-pointer"
        >
          <Printer className="w-4 h-4" />
          <span>Cetak Sekarang / Simpan PDF</span>
        </button>
      </div>

      {/* Official Government Document Paper */}
      <div className="max-w-5xl mx-auto bg-white p-6 sm:p-12 rounded-2xl shadow-lg border border-[#eaeff5] dark:border-slate-800 print:shadow-none print:border-none print:p-0 print:rounded-none">
        {/* Kop Surat Resmi */}
        <div className="flex items-center gap-5 pb-4 border-b-4 border-black border-double text-center mb-6">
          <div className="w-20 h-24 shrink-0 flex items-center justify-center">
            <img 
              src="/images/logo-purbalingga.png" 
              alt="Logo Purbalingga" 
              className="max-h-24 max-w-full object-contain"
            />
          </div>
          <div className="flex-1 text-center pr-12">
            <h3 className="text-base font-bold tracking-wider uppercase m-0 leading-tight">
              PEMERINTAH KABUPATEN PURBALINGGA
            </h3>
            <h2 className="text-xl font-black tracking-wide uppercase m-0 leading-tight mt-1">
              DINAS PERINDUSTRIAN DAN TENAGA KERJA
            </h2>
            <p className="text-xs m-0 mt-1 leading-snug">
              Jl. Letnan Kusni No. 06, Kedung Menjangan, Purbalingga, Jawa Tengah 53315
            </p>
            <p className="text-[11px] m-0 text-slate-700">
              Telepon: (0281) 891044 | Pos-el: dinperinnaker@purbalinggakab.go.id | Laman: dinperinnaker.purbalinggakab.go.id
            </p>
          </div>
        </div>

        {/* Document Title */}
        <div className="text-center mb-6">
          <h4 className="text-sm font-extrabold uppercase underline tracking-wider">
            LAPORAN REKAPITULASI DATA STATISTIK SEKTORAL
          </h4>
          <p className="text-xs text-slate-700 mt-1">
            Sistem Informasi Satu Data DINPERINNAKER Kabupaten Purbalingga
          </p>
        </div>

        {/* Metadata Filter */}
        <div className="text-xs mb-4 space-y-1 bg-slate-50 print:bg-transparent p-3 rounded-xl border border-slate-200 print:border-none print:p-0">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div>
              <span className="font-semibold text-slate-600 block">Unit Kerja:</span>
              <span className="font-bold">{selectedUnit ? selectedUnit.nama_unit : 'Seluruh Unit Kerja'}</span>
            </div>
            <div>
              <span className="font-semibold text-slate-600 block">Tahun Laporan:</span>
              <span className="font-bold">{tahunParam === 'all' ? 'Semua Tahun' : tahunParam}</span>
            </div>
            <div>
              <span className="font-semibold text-slate-600 block">Status Data:</span>
              <span className="font-bold">{statusParam === 'all' ? 'Semua Status' : statusParam}</span>
            </div>
            <div>
              <span className="font-semibold text-slate-600 block">
                {tglAwalParam || tglAkhirParam ? 'Rentang Tanggal:' : 'Tanggal Cetak:'}
              </span>
              <span className="font-bold">
                {tglAwalParam || tglAkhirParam 
                  ? `${tglAwalParam || 'Awal'} s/d ${tglAkhirParam || 'Sekarang'}`
                  : formattedDate}
              </span>
            </div>
          </div>
        </div>

        {/* Official Report Table */}
        <table className="w-full text-left text-xs border-collapse border border-black mb-8">
          <thead>
            <tr className="bg-slate-100 print:bg-slate-200 text-center font-bold">
              <th className="border border-black px-2 py-2.5 w-10">NO</th>
              <th className="border border-black px-3 py-2.5 w-44">UNIT KERJA</th>
              <th className="border border-black px-3 py-2.5">NAMA DATA / INDIKATOR</th>
              <th className="border border-black px-2 py-2.5 w-24">SATUAN</th>
              <th className="border border-black px-2 py-2.5 w-16">TAHUN</th>
              <th className="border border-black px-3 py-2.5 w-28 text-right">TOTAL DATA</th>
              <th className="border border-black px-2 py-2.5 w-20">STATUS</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.length === 0 ? (
              <tr>
                <td colSpan={7} className="border border-black px-4 py-8 text-center text-slate-500 italic">
                  Tidak ada data yang tersedia untuk parameter laporan ini.
                </td>
              </tr>
            ) : (
              filteredData.map((item, index) => {
                const unit = unitKerjas.find(u => u.id === item.unit_kerja_id);
                return (
                  <tr key={item.id} className="align-top">
                    <td className="border border-black px-2 py-2 text-center">{index + 1}</td>
                    <td className="border border-black px-3 py-2 font-semibold">{unit?.nama_unit}</td>
                    <td className="border border-black px-3 py-2">
                      <span className="font-bold block">{item.nama_data}</span>
                      {item.deskripsi && (
                        <span className="text-[10px] text-slate-600 block mt-0.5">{item.deskripsi}</span>
                      )}
                    </td>
                    <td className="border border-black px-2 py-2 text-center">{item.satuan}</td>
                    <td className="border border-black px-2 py-2 text-center font-bold">{item.tahun_awal}</td>
                    <td className="border border-black px-3 py-2 text-right font-black">
                      {item.jumlah.toLocaleString('id-ID')}
                    </td>
                    <td className="border border-black px-2 py-2 text-center font-semibold">{item.status}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>

        {/* Signature Section */}
        <div className="flex justify-end pt-4 break-inside-avoid">
          <div className="w-72 text-center text-xs">
            <p className="m-0">Purbalingga, {formattedDate}</p>
            <p className="font-bold m-0 mt-0.5">Kepala Dinas Perindustrian dan Tenaga Kerja</p>
            <p className="font-bold m-0">Kabupaten Purbalingga</p>

            <div className="h-24 flex items-center justify-center">
              {/* Official digital stamp/signature placeholder */}
              <span className="text-[10px] text-slate-400 italic print:hidden">[ Ruang Tanda Tangan & Cap Dinas ]</span>
            </div>

            <p className="font-black text-sm underline m-0 uppercase tracking-wide">
              {kadis.nama_lengkap}
            </p>
            <p className="m-0 text-slate-800">Pembina Utama Muda</p>
            <p className="m-0 text-slate-800">NIP. 19740510 199311 1 001</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LaporanPrintPage() {
  return (
    <Suspense fallback={<div className="p-10 text-center font-bold text-slate-500">Memuat Dokumen Cetak...</div>}>
      <PrintContent />
    </Suspense>
  );
}
