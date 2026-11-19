'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  Home, 
  Database, 
  FileText, 
  Building2, 
  Users, 
  ShieldCheck, 
  LogOut
} from 'lucide-react';
import { useData } from '@/context/DataContext';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { currentUser, unitKerjas, logout } = useData();

  const isSuperAdmin = currentUser?.role === 'Super Admin';
  const currentUnit = unitKerjas.find(u => u.id === currentUser?.unit_kerja_id);

  const menuUtama = [
    { label: 'Dashboard', href: '/', icon: Home },
    { label: 'Kelola Data', href: '/kelola-data', icon: Database },
    { label: 'Laporan', href: '/laporan', icon: FileText },
  ];

  const menuAdmin = [
    { label: 'Unit Kerja', href: '/unit-kerja', icon: Building2 },
    { label: 'Pengguna', href: '/users', icon: Users },
    { label: 'Backup & Sistem', href: '/backup', icon: ShieldCheck },
  ];

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/40 z-40 lg:hidden backdrop-blur-xs transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 w-64 bg-white dark:bg-[#1e293b] border-r border-[#eaeff5] dark:border-[#334155] flex flex-col transition-all duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Brand Header */}
        <div className="h-20 flex items-center gap-3 px-6 border-b border-[#eaeff5] dark:border-[#334155]">
          <div className="w-10 h-10 rounded-xl bg-white dark:bg-slate-800 p-0.5 flex items-center justify-center shrink-0">
            <img 
              src="/images/logo-purbalingga.png" 
              alt="Logo Purbalingga"
              className="w-full h-full object-contain"
              onError={(e) => {
                (e.target as HTMLElement).style.display = 'none';
              }}
            />
          </div>
          <div className="overflow-hidden">
            <h1 className="font-extrabold text-[#0d6b63] text-base leading-tight tracking-tight">
              SatuNaker
            </h1>
            <p className="text-[11px] text-[#64748b] font-medium leading-tight mt-0.5">
              DINPERINNAKER Purbalingga
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
          {/* Menu Utama */}
          <div>
            <div className="text-[11px] font-bold text-[#94a3b8] uppercase tracking-wider px-3 mb-2.5">
              MENU UTAMA
            </div>
            <nav className="space-y-1.5">
              {menuUtama.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={onClose}
                    className={`
                      flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150
                      ${isActive 
                        ? 'bg-[#0d6b63] text-white shadow-xs' 
                        : 'text-[#475569] dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-[#0d6b63]'}
                    `}
                  >
                    <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-[#64748b]'}`} />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Menu Administrasi (Super Admin Only) */}
          {isSuperAdmin && (
            <div>
              <div className="text-[11px] font-bold text-[#94a3b8] uppercase tracking-wider px-3 mb-2.5">
                ADMINISTRASI
              </div>
              <nav className="space-y-1.5">
                {menuAdmin.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={onClose}
                      className={`
                        flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150
                        ${isActive 
                          ? 'bg-[#0d6b63] text-white shadow-xs' 
                          : 'text-[#475569] dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-[#0d6b63]'}
                      `}
                    >
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-[#64748b]'}`} />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>
          )}
        </div>

        {/* Footer / Keluar Logout Button */}
        <div className="p-4 border-t border-[#eaeff5] dark:border-[#334155]">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-bold text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:hover:bg-red-900/50 border border-red-200 dark:border-red-900/60 rounded-xl transition-all cursor-pointer shadow-2xs"
          >
            <LogOut className="w-4 h-4" />
            <span>Keluar / Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
