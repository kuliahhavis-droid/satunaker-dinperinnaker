import * as XLSX from 'xlsx';
import { DataRecord, UnitKerja } from '@/types';

export interface ExportExcelOptions {
  records: DataRecord[];
  unitKerjas: UnitKerja[];
  filterUnit?: string;
  filterTahun?: string;
  filterStatus?: string;
  tglAwal?: string;
  tglAkhir?: string;
}

export function formatHttpsUrl(url: string | null | undefined): string | null {
  if (!url || !url.trim()) return null;
  const trimmed = url.trim();
  if (/^https?:\/\//i.test(trimmed)) {
    return trimmed.replace(/^http:\/\//i, 'https://');
  }
  return `https://${trimmed}`;
}

export function generateSatuNakerExcel({
  records,
  unitKerjas,
  filterUnit = 'all',
  filterTahun = 'all',
  filterStatus = 'all',
  tglAwal = '',
  tglAkhir = '',
}: ExportExcelOptions): { workbook: XLSX.WorkBook; filename: string } {
  const selectedUnit = filterUnit === 'all' 
    ? null 
    : unitKerjas.find(u => u.id.toString() === filterUnit);
  
  const unitLabel = selectedUnit ? selectedUnit.nama_unit : 'Semua Unit Kerja';
  const tahunLabel = filterTahun === 'all' ? 'Semua Tahun' : filterTahun;
  const statusLabel = filterStatus === 'all' ? 'Semua Status' : filterStatus;
  
  const rentangLabel = (tglAwal || tglAkhir)
    ? `${tglAwal || 'Awal'} s/d ${tglAkhir || 'Sekarang'}`
    : 'Seluruh Periode';

  const now = new Date();
  const exportDateStr = new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(now) + ' WIB';

  // --- SHEET 1: Data Rekapitulasi ---
  const sheet1Rows: any[][] = [
    ['PEMERINTAH KABUPATEN PURBALINGGA'],
    ['DINAS PERINDUSTRIAN DAN TENAGA KERJA (DINPERINNAKER)'],
    ['LAPORAN REKAPITULASI DATA STATISTIK SEKTORAL - SATUNAKER'],
    [''],
    ['Unit Kerja:', unitLabel, '', '', 'Tanggal Unduh:', exportDateStr],
    ['Tahun Laporan:', tahunLabel, '', '', 'Total Data:', `${records.length} Rekaman`],
    ['Status Data:', statusLabel, '', '', 'Rentang Tanggal:', rentangLabel],
    [''],
    [
      'NO',
      'UNIT KERJA',
      'NAMA DATA / INDIKATOR',
      'SATUAN',
      'TAHUN',
      'JUMLAH CAPAIAN',
      'STATUS',
      'TAUTAN GOOGLE DRIVE',
      'KETERANGAN / DESKRIPSI',
    ],
  ];

  let totalSum = 0;

  records.forEach((item, index) => {
    const unit = unitKerjas.find(u => u.id === item.unit_kerja_id);
    const driveUrl = formatHttpsUrl(item.link_gdrive);
    totalSum += Number(item.jumlah) || 0;

    sheet1Rows.push([
      { t: 'n', v: index + 1 },
      unit?.nama_unit || `Unit #${item.unit_kerja_id}`,
      item.nama_data,
      item.satuan,
      { t: 'n', v: item.tahun_awal },
      { t: 'n', v: item.jumlah, z: '#,##0' },
      item.status,
      driveUrl 
        ? { 
            t: 's', 
            f: `HYPERLINK("${driveUrl}", "${driveUrl}")`, 
            v: driveUrl, 
            l: { Target: driveUrl, Tooltip: 'Buka Tautan Google Drive' } 
          }
        : '-',
      item.deskripsi || '-',
    ]);
  });

  const headerRowIndex = 8; // 0-indexed, row 9 in 1-indexed Excel
  const dataStartRow = headerRowIndex + 1; // row 10 in Excel
  const dataEndRow = headerRowIndex + records.length; // row 9 + N in Excel

  const sheet1Merges: XLSX.Range[] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 8 } },
    { s: { r: 1, c: 0 }, e: { r: 1, c: 8 } },
    { s: { r: 2, c: 0 }, e: { r: 2, c: 8 } },
  ];

  if (records.length > 0) {
    // Add Total Row
    sheet1Rows.push([
      'TOTAL KESELURUHAN',
      '',
      '',
      '',
      '',
      { 
        t: 'n', 
        f: `SUM(F${dataStartRow + 1}:F${dataEndRow + 1})`, 
        v: totalSum, 
        z: '#,##0' 
      },
      '',
      '',
      '',
    ]);

    const totalRowIndex = sheet1Rows.length - 1;
    sheet1Merges.push({
      s: { r: totalRowIndex, c: 0 },
      e: { r: totalRowIndex, c: 4 },
    });
  }

  // Footer note
  sheet1Rows.push(['']);
  sheet1Rows.push([
    'Catatan: Dokumen resmi ini digenerate secara otomatis oleh Sistem SatuNaker DINPERINNAKER Kabupaten Purbalingga.',
  ]);

  const ws1 = XLSX.utils.aoa_to_sheet(sheet1Rows);
  ws1['!merges'] = sheet1Merges;
  ws1['!cols'] = [
    { wch: 6 },   // No
    { wch: 32 },  // Unit Kerja
    { wch: 48 },  // Nama Data / Indikator
    { wch: 18 },  // Satuan
    { wch: 10 },  // Tahun
    { wch: 20 },  // Jumlah Capaian
    { wch: 14 },  // Status
    { wch: 55 },  // Tautan Google Drive
    { wch: 40 },  // Keterangan / Deskripsi
  ];

  // --- SHEET 2: Ringkasan per Unit Kerja ---
  const sheet2Rows: any[][] = [
    ['RINGKASAN DATA STATISTIK SEKTORAL PER UNIT KERJA'],
    ['SatuNaker DINPERINNAKER Kabupaten Purbalingga'],
    [''],
    [
      'NO',
      'NAMA UNIT KERJA',
      'TIPE UNIT',
      'JUMLAH INDIKATOR / DATA',
      'TOTAL AKUMULASI CAPAIAN',
    ],
  ];

  let grandTotalDataCount = 0;
  let grandTotalCapaian = 0;

  unitKerjas.forEach((unit, idx) => {
    const unitRecords = records.filter(r => r.unit_kerja_id === unit.id);
    const count = unitRecords.length;
    const sum = unitRecords.reduce((acc, curr) => acc + (Number(curr.jumlah) || 0), 0);
    grandTotalDataCount += count;
    grandTotalCapaian += sum;

    sheet2Rows.push([
      { t: 'n', v: idx + 1 },
      unit.nama_unit,
      unit.tipe.toUpperCase(),
      { t: 'n', v: count, z: '#,##0' },
      { t: 'n', v: sum, z: '#,##0' },
    ]);
  });

  const sheet2StartRow = 5; // row 5 in Excel
  const sheet2EndRow = 4 + unitKerjas.length;

  sheet2Rows.push([
    'TOTAL KESELURUHAN',
    '',
    '',
    { 
      t: 'n', 
      f: `SUM(D${sheet2StartRow}:D${sheet2EndRow})`, 
      v: grandTotalDataCount, 
      z: '#,##0' 
    },
    { 
      t: 'n', 
      f: `SUM(E${sheet2StartRow}:E${sheet2EndRow})`, 
      v: grandTotalCapaian, 
      z: '#,##0' 
    },
  ]);

  const sheet2Merges: XLSX.Range[] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 4 } },
    { s: { r: 1, c: 0 }, e: { r: 1, c: 4 } },
    { s: { r: sheet2Rows.length - 1, c: 0 }, e: { r: sheet2Rows.length - 1, c: 2 } },
  ];

  const ws2 = XLSX.utils.aoa_to_sheet(sheet2Rows);
  ws2['!merges'] = sheet2Merges;
  ws2['!cols'] = [
    { wch: 6 },   // No
    { wch: 42 },  // Nama Unit Kerja
    { wch: 18 },  // Tipe
    { wch: 26 },  // Jumlah Indikator
    { wch: 28 },  // Total Akumulasi Capaian
  ];

  // Build Workbook
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, ws1, 'Data Rekapitulasi');
  XLSX.utils.book_append_sheet(workbook, ws2, 'Ringkasan Unit Kerja');

  // Dynamic file name
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const cleanUnit = filterUnit === 'all' 
    ? 'SemuaUnit' 
    : (selectedUnit?.nama_unit || 'Unit').replace(/[^a-zA-Z0-9]/g, '_');
  const cleanTahun = filterTahun === 'all' ? 'SemuaTahun' : filterTahun;
  const filename = `Laporan_SatuNaker_${cleanUnit}_${cleanTahun}_${dateStr}.xlsx`;

  return { workbook, filename };
}

export function exportSatuNakerExcel(options: ExportExcelOptions): string {
  const { workbook, filename } = generateSatuNakerExcel(options);
  XLSX.writeFile(workbook, filename);
  return filename;
}
