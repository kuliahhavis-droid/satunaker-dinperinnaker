'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, 
  Home, 
  Database, 
  FileText, 
  Building2, 
  Users, 
  ShieldCheck, 
  ArrowRight, 
  X,
  ExternalLink
} from 'lucide-react';
import { useData } from '@/context/DataContext';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const router = useRouter();
  const { dataRecords, unitKerjas, currentUser } = useData();
  const [query, setQuery] = useState('');

  const isSuperAdmin = currentUser?.role === 'Super Admin';

  // Navigation Items
  const staticNavs = [
    { name: 'Dashboard Eksekutif', href: '/', icon: Home, desc: 'Ringkasan KPI, grafik sebaran, dan tren' },
    { name: 'Kelola Data Sektoral', href: '/kelola-data', icon: Database, desc: 'Pencatatan data capaian & link Google Drive' },
    { name: 'Laporan Kinerja', href: '/laporan', icon: FileText, desc: 'Pratinjau cetak dinas & ekspor Excel' },
  ];

  if (isSuperAdmin) {
    staticNavs.push(
      { name: 'Manajemen Unit Kerja', href: '/unit-kerja', icon: Building2, desc: 'Kelola Bidang, Sekretariat, dan UPTD' },
      { name: 'Manajemen Pengguna', href: '/users', icon: Users, desc: 'Pengaturan akun pegawai & peran RBAC' },
      { name: 'Pencadangan Database & Log', href: '/backup', icon: ShieldCheck, desc: 'Unduh backup SQL dan audit trail' },
    );
  }

  // Filtered Items
  const filteredNavs = staticNavs.filter(nav => 
    nav.name.toLowerCase().includes(query.toLowerCase()) ||
    nav.desc.toLowerCase().includes(query.toLowerCase())
  );

  const filteredData = query.trim() ? dataRecords.filter(d => 
    d.nama_data.toLowerCase().includes(query.toLowerCase()) ||
    d.satuan.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 5) : [];

  const handleSelectNav = (href: string) => {
    onClose();
    router.push(href);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4">
          {/* Backdrop with Blur */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs"
          />

          {/* Modal Container */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.15 }}
            className="relative w-full max-w-xl bg-white dark:bg-[#1e293b] rounded-2xl shadow-2xl border border-[#eaeff5] dark:border-[#334155] overflow-hidden z-10"
          >
            {/* Search Input Bar */}
            <div className="flex items-center px-4 py-3.5 border-b border-[#eaeff5] dark:border-[#334155]">
              <Search className="w-5 h-5 text-[#7c8db5] shrink-0" />
              <input
                type="text"
                autoFocus
                placeholder="Ketik untuk mencari menu, indikator, atau unit kerja..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full pl-3 pr-2 bg-transparent text-sm text-[#25396e] dark:text-[#f8fafc] font-medium placeholder-[#7c8db5] outline-none"
              />
              <span className="text-[10px] font-bold text-[#7c8db5] bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-md shrink-0">
                ESC
              </span>
            </div>

            {/* Results List */}
            <div className="max-h-96 overflow-y-auto p-2 space-y-4">
              {/* Menu Navigation */}
              {filteredNavs.length > 0 && (
                <div>
                  <div className="px-3 py-1.5 text-[10px] font-bold text-[#7c8db5] uppercase tracking-wider">
                    Navigasi Menu
                  </div>
                  <div className="space-y-1">
                    {filteredNavs.map((nav) => {
                      const Icon = nav.icon;
                      return (
                        <button
                          key={nav.href}
                          onClick={() => handleSelectNav(nav.href)}
                          className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors group cursor-pointer"
                        >
                          <div className="flex items-center gap-3 min-w-0">
                            <div className="w-8 h-8 rounded-lg bg-[#e6f4f6] dark:bg-slate-700 text-[#2a92a2] flex items-center justify-center shrink-0">
                              <Icon className="w-4 h-4" />
                            </div>
                            <div className="truncate">
                              <p className="text-xs font-bold text-[#25396e] dark:text-[#f8fafc] group-hover:text-[#2a92a2]">
                                {nav.name}
                              </p>
                              <p className="text-[11px] text-[#7c8db5] truncate">
                                {nav.desc}
                              </p>
                            </div>
                          </div>
                          <ArrowRight className="w-4 h-4 text-[#7c8db5] group-hover:text-[#2a92a2] group-hover:translate-x-0.5 transition-all shrink-0" />
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Data Items Search Results */}
              {filteredData.length > 0 && (
                <div>
                  <div className="px-3 py-1.5 text-[10px] font-bold text-[#7c8db5] uppercase tracking-wider">
                    Data Capaian Terkait ({filteredData.length})
                  </div>
                  <div className="space-y-1">
                    {filteredData.map((d) => (
                      <button
                        key={d.id}
                        onClick={() => handleSelectNav('/kelola-data')}
                        className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-[#f2f7ff] dark:hover:bg-slate-800 transition-colors group cursor-pointer"
                      >
                        <div className="min-w-0 pr-3">
                          <p className="text-xs font-bold text-[#25396e] dark:text-[#f8fafc] truncate group-hover:text-[#2a92a2]">
                            {d.nama_data}
                          </p>
                          <p className="text-[10px] text-[#7c8db5]">
                            Tahun {d.tahun_awal} • {d.jumlah.toLocaleString('id-ID')} {d.satuan}
                          </p>
                        </div>
                        <span className="text-[10px] font-bold text-[#2a92a2] bg-[#e6f4f6] dark:bg-slate-700 px-2 py-0.5 rounded-md shrink-0">
                          Lihat Data
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {filteredNavs.length === 0 && filteredData.length === 0 && (
                <div className="p-8 text-center text-xs text-[#7c8db5]">
                  Tidak ada menu atau data yang cocok dengan &quot;{query}&quot;
                </div>
              )}
            </div>

            {/* Footer Tips */}
            <div className="px-4 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-t border-[#eaeff5] dark:border-[#334155] flex items-center justify-between text-[11px] text-[#7c8db5]">
              <span>Gunakan tombol panah & ENTER untuk memilih</span>
              <span>SatuNaker Dinperinnaker</span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
