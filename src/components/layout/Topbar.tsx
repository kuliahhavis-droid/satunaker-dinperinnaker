'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { 
  Menu, 
  Search, 
  Moon, 
  Sun, 
  ChevronDown, 
  Database, 
  FileText, 
  Users, 
  ShieldCheck, 
  Shield, 
  LogOut 
} from 'lucide-react';
import { useData } from '@/context/DataContext';
import { useTheme } from '@/context/ThemeContext';
import CommandPalette from '@/components/ui/CommandPalette';
import NotificationDropdown from './NotificationDropdown';
import { toast } from 'sonner';

interface TopbarProps {
  onToggleSidebar: () => void;
  title?: string;
}

export default function Topbar({ onToggleSidebar }: TopbarProps) {
  const router = useRouter();
  const { currentUser, unitKerjas, logout } = useData();
  const { theme, toggleTheme } = useTheme();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isCommandOpen, setIsCommandOpen] = useState(false);
  const userMenuRef = useRef<HTMLDivElement>(null);

  const currentUserUnit = unitKerjas.find(un => un.id === currentUser?.unit_kerja_id);

  // Keyboard shortcut Ctrl + K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(e.target as Node)) {
        setShowUserMenu(false);
      }
    };
    if (showUserMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showUserMenu]);

  const handleLogout = () => {
    setShowUserMenu(false);
    logout();
    toast.info('Anda telah keluar dari akun.');
    router.push('/login');
  };

  return (
    <>
      <header className="h-16 lg:h-18 bg-white dark:bg-[#1e293b] border-b border-[#eaeff5] dark:border-[#334155] px-4 lg:px-8 flex items-center justify-between sticky top-0 z-30 shadow-2xs transition-colors">
        {/* Left: Mobile Hamburger */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl text-[#64748b] hover:text-[#0d6b63] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
            aria-label="Buka Menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>

        {/* Center: Search Bar Pill */}
        <div className="flex-1 max-w-md mx-auto px-4 hidden md:block">
          <div 
            onClick={() => setIsCommandOpen(true)}
            className="flex items-center justify-between w-full pl-4 pr-3 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-full text-xs text-slate-500 hover:border-[#0d6b63] transition-all cursor-pointer shadow-2xs"
          >
            <div className="flex items-center gap-2.5">
              <Search className="w-4 h-4 text-slate-400" />
              <span>Cari data, indikator, menu...</span>
            </div>
            <kbd className="text-[10px] bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 px-2 py-0.5 rounded-md font-mono text-slate-400 shadow-2xs">
              Ctrl K
            </kbd>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center gap-2 lg:gap-3">
          {/* Mobile Search button */}
          <button
            onClick={() => setIsCommandOpen(true)}
            className="md:hidden p-2 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50 transition-colors cursor-pointer"
            title="Cari..."
          >
            <Search className="w-4 h-4" />
          </button>

          {/* Notification Dropdown */}
          <NotificationDropdown />

          {/* Dark Mode Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-50 transition-colors cursor-pointer"
            title={theme === 'dark' ? 'Beralih ke Mode Terang' : 'Beralih ke Mode Gelap'}
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4 text-slate-600" />}
          </button>

          {/* User Profile Pill Trigger */}
          <div className="relative" ref={userMenuRef}>
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2.5 pl-2 py-1 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl transition-colors cursor-pointer"
              title="Profil Pengguna & Akun"
            >
              <div className="w-9 h-9 rounded-full bg-[#0d6b63] text-white flex items-center justify-center font-bold text-sm shadow-xs shrink-0">
                {currentUser?.username?.substring(0, 1).toUpperCase() || 'U'}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-xs font-bold text-slate-800 dark:text-slate-100 leading-tight">
                  {currentUser?.nama || currentUser?.username || 'Pengguna'}
                </p>
                <p className="text-[10px] text-slate-400 leading-tight">
                  {currentUser?.role || 'Pengguna'}
                </p>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 ml-0.5" />
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-[#1e293b] border border-[#eaeff5] dark:border-[#334155] rounded-2xl shadow-xl z-50 overflow-hidden animate-in fade-in duration-150">
                {/* Header Profil Pengguna Aktif */}
                <div className="p-4 bg-gradient-to-br from-[#f8fafc] to-[#eef7f6] dark:from-slate-800 dark:to-slate-800/80 border-b border-[#eaeff5] dark:border-[#334155]">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-[#0d6b63] text-white flex items-center justify-center font-extrabold text-base shadow-sm shrink-0">
                      {currentUser?.username?.substring(0, 1).toUpperCase() || 'U'}
                    </div>
                    <div className="overflow-hidden">
                      <p className="text-sm font-bold text-slate-800 dark:text-white truncate">
                        {currentUser?.nama_lengkap || currentUser?.nama || currentUser?.username}
                      </p>
                      <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
                        {currentUser?.email || `@${currentUser?.username}`}
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-1.5 flex-wrap">
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#e6f4f2] text-[#0d6b63] dark:bg-teal-950/70 dark:text-teal-300">
                      <Shield className="w-3 h-3" />
                      {currentUser?.role || 'Pengguna'}
                    </span>
                    {currentUserUnit && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300 truncate max-w-[190px]" title={currentUserUnit.nama_unit}>
                        {currentUserUnit.nama_unit}
                      </span>
                    )}
                  </div>
                </div>

                {/* Menu Tautan */}
                <div className="p-2 space-y-1 text-xs">
                  <Link
                    href="/kelola-data"
                    onClick={() => setShowUserMenu(false)}
                    className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    <Database className="w-4 h-4 text-[#0d6b63]" />
                    <span>Kelola Data Sektoral</span>
                  </Link>

                  <Link
                    href="/laporan"
                    onClick={() => setShowUserMenu(false)}
                    className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    <FileText className="w-4 h-4 text-[#0d6b63]" />
                    <span>Laporan Kinerja</span>
                  </Link>

                  {currentUser?.role === 'Super Admin' && (
                    <>
                      <Link
                        href="/users"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      >
                        <Users className="w-4 h-4 text-[#0d6b63]" />
                        <span>Manajemen Pengguna</span>
                      </Link>
                      <Link
                        href="/backup"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      >
                        <ShieldCheck className="w-4 h-4 text-[#0d6b63]" />
                        <span>Cadangan & Keamanan</span>
                      </Link>
                    </>
                  )}
                </div>

                {/* Footer Logout */}
                <div className="p-2 border-t border-[#eaeff5] dark:border-[#334155] bg-slate-50/50 dark:bg-slate-800/40">
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs font-bold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors cursor-pointer"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Keluar dari Akun</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Command Palette Modal */}
      <CommandPalette isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} />
    </>
  );
}
