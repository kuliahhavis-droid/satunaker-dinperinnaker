'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Menu, Search, Moon, Sun, ChevronDown } from 'lucide-react';
import { useData } from '@/context/DataContext';
import { useTheme } from '@/context/ThemeContext';
import CommandPalette from '@/components/ui/CommandPalette';
import NotificationDropdown from './NotificationDropdown';

interface TopbarProps {
  onToggleSidebar: () => void;
  title?: string;
}

export default function Topbar({ onToggleSidebar }: TopbarProps) {
  const { currentUser, users, setCurrentUser, unitKerjas } = useData();
  const { theme, toggleTheme } = useTheme();
  const [showRoleSwitcher, setShowRoleSwitcher] = useState(false);
  const [isCommandOpen, setIsCommandOpen] = useState(false);
  const roleSwitcherRef = useRef<HTMLDivElement>(null);

  // Group users by category
  const roleGroups = [
    {
      title: '👑 Pimpinan & Master',
      items: users.filter(u => ['Super Admin', 'Kepala Dinas'].includes(u.role)),
    },
    {
      title: '💼 Bidang Teknis',
      items: users.filter(u => u.role === 'Admin Bidang'),
    },
    {
      title: '📋 Sekretariat (Subag)',
      items: users.filter(u => u.role === 'Admin Sekretariat'),
    },
    {
      title: '⚙️ UPTD Dinas',
      items: users.filter(u => u.role === 'Admin UPTD'),
    },
  ];

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

  // Close role switcher when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (roleSwitcherRef.current && !roleSwitcherRef.current.contains(e.target as Node)) {
        setShowRoleSwitcher(false);
      }
    };
    if (showRoleSwitcher) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showRoleSwitcher]);

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
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* User Profile Pill Trigger */}
          <div className="relative" ref={roleSwitcherRef}>
            <button
              onClick={() => setShowRoleSwitcher(!showRoleSwitcher)}
              className="flex items-center gap-2.5 pl-2 py-1 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl transition-colors cursor-pointer"
              title="Ganti Peran / Profil"
            >
              <div className="w-9 h-9 rounded-full bg-[#0d6b63] text-white flex items-center justify-center font-bold text-sm shadow-xs shrink-0">
                {currentUser?.username?.substring(0, 1).toUpperCase() || 'S'}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-xs font-bold text-slate-800 dark:text-slate-100 leading-tight">
                  {currentUser?.nama || currentUser?.username || 'Super Admin'}
                </p>
                <p className="text-[10px] text-slate-400 leading-tight">
                  {currentUser?.role || 'Super Admin'}
                </p>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 ml-0.5" />
            </button>

            {showRoleSwitcher && (
              <div className="absolute right-0 mt-2 w-72 bg-white dark:bg-[#1e293b] border border-[#eaeff5] dark:border-[#334155] rounded-2xl shadow-xl p-2 z-50">
                <div className="px-3 py-2 border-b border-[#eaeff5] dark:border-[#334155]">
                  <p className="text-xs font-bold text-[#1e293b] dark:text-[#f8fafc]">Pilih Peran Pengujian Instan</p>
                  <p className="text-[11px] text-[#64748b]">Uji sudut pandang hak akses dinas</p>
                </div>
                <div className="py-1 max-h-72 overflow-y-auto space-y-2">
                  {roleGroups.map((group, gIdx) => (
                    <div key={gIdx} className="space-y-0.5">
                      <p className="text-[10px] font-bold text-[#64748b] dark:text-slate-400 px-3 pt-1">
                        {group.title}
                      </p>
                      {group.items.map((u) => {
                        const unit = unitKerjas.find(un => un.id === u.unit_kerja_id);
                        return (
                          <button
                            key={u.id}
                            onClick={() => {
                              setCurrentUser(u);
                              setShowRoleSwitcher(false);
                            }}
                            className={`
                              w-full text-left px-3 py-1.5 rounded-xl text-xs flex items-center justify-between transition-colors cursor-pointer
                              ${currentUser?.id === u.id ? 'bg-[#e6f4f2] dark:bg-slate-800 text-[#0d6b63] font-bold' : 'hover:bg-slate-100 dark:hover:bg-slate-800/70 text-slate-700 dark:text-[#f8fafc]'}
                            `}
                          >
                            <div className="truncate pr-2">
                              <p className="font-semibold truncate">{u.nama || u.username}</p>
                              <p className="text-[10px] text-slate-400 truncate">
                                {unit ? unit.nama_unit : u.role}
                              </p>
                            </div>
                            {currentUser?.id === u.id && (
                              <span className="w-2 h-2 rounded-full bg-[#0d6b63] shrink-0" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  ))}
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
