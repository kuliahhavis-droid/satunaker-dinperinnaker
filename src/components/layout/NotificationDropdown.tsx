'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useData } from '@/context/DataContext';
import { 
  Bell, 
  BellOff, 
  CheckCheck, 
  Database, 
  Plus, 
  Edit3, 
  Trash2, 
  HardDrive, 
  Key, 
  Activity, 
  ArrowRight,
  ExternalLink,
  Radio
} from 'lucide-react';

export default function NotificationDropdown() {
  const { logs, realtimeStatus, currentUser } = useData();
  const isSuperAdmin = currentUser?.role === 'Super Admin';
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const [readIds, setReadIds] = useState<number[]>([]);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Load read notifications from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('satudata_read_notifications');
      if (saved) {
        setReadIds(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Failed to load read notifications', e);
    }
  }, []);

  // Save read notifications to localStorage
  const saveReadIds = (newReadIds: number[]) => {
    setReadIds(newReadIds);
    try {
      localStorage.setItem('satudata_read_notifications', JSON.stringify(newReadIds));
    } catch (e) {
      console.error('Failed to save read notifications', e);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Unread count
  const unreadCount = logs.filter(l => !readIds.includes(l.id)).length;

  // Filtered logs
  const displayLogs = filter === 'unread' 
    ? logs.filter(l => !readIds.includes(l.id))
    : logs;

  // Mark all as read
  const handleMarkAllAsRead = () => {
    const allIds = Array.from(new Set([...readIds, ...logs.map(l => l.id)]));
    saveReadIds(allIds);
  };

  // Mark single as read and navigate
  const handleItemClick = (logId: number, aktivitas: string) => {
    if (!readIds.includes(logId)) {
      saveReadIds([...readIds, logId]);
    }
    setIsOpen(false);

    // Route intelligently based on activity
    const lower = aktivitas.toLowerCase();
    if (lower.includes('data') || lower.includes('indikator') || lower.includes('rekam')) {
      router.push('/kelola-data');
    } else if (isSuperAdmin) {
      if (lower.includes('backup') || lower.includes('restore') || lower.includes('sql') || lower.includes('audit')) {
        router.push('/backup');
      } else if (lower.includes('unit') || lower.includes('bidang') || lower.includes('uptd')) {
        router.push('/unit-kerja');
      } else if (lower.includes('user') || lower.includes('pengguna') || lower.includes('login')) {
        router.push('/users');
      }
    }
  };

  // Format relative time
  const getRelativeTime = (dateStr?: string) => {
    if (!dateStr) return 'Baru saja';
    try {
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) return dateStr;
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffSec = Math.floor(diffMs / 1000);
      const diffMin = Math.floor(diffSec / 60);
      const diffHour = Math.floor(diffMin / 60);
      const diffDay = Math.floor(diffHour / 24);

      if (diffSec < 45) return 'Baru saja';
      if (diffMin < 60) return `${diffMin}m yang lalu`;
      if (diffHour < 24) return `${diffHour}j yang lalu`;
      if (diffDay === 1) return 'Kemarin';
      if (diffDay < 7) return `${diffDay}h yang lalu`;
      return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' });
    } catch {
      return dateStr;
    }
  };

  // Icon & theme helper
  const getLogMeta = (aktivitas: string) => {
    const lower = aktivitas.toLowerCase();
    if (lower.includes('tambah') || lower.includes('input') || lower.includes('create')) {
      return {
        icon: <Plus className="w-3.5 h-3.5" />,
        bgColor: 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800',
        badge: 'Data Baru',
      };
    }
    if (lower.includes('ubah') || lower.includes('edit') || lower.includes('update') || lower.includes('perbarui')) {
      return {
        icon: <Edit3 className="w-3.5 h-3.5" />,
        bgColor: 'bg-amber-50 dark:bg-amber-950/50 text-amber-600 dark:text-amber-400 border-amber-200 dark:border-amber-800',
        badge: 'Pembaruan',
      };
    }
    if (lower.includes('hapus') || lower.includes('delete')) {
      return {
        icon: <Trash2 className="w-3.5 h-3.5" />,
        bgColor: 'bg-rose-50 dark:bg-rose-950/50 text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-800',
        badge: 'Penghapusan',
      };
    }
    if (lower.includes('backup') || lower.includes('restore') || lower.includes('sql')) {
      return {
        icon: <HardDrive className="w-3.5 h-3.5" />,
        bgColor: 'bg-sky-50 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 border-sky-200 dark:border-sky-800',
        badge: 'Sistem',
      };
    }
    if (lower.includes('login') || lower.includes('masuk')) {
      return {
        icon: <Key className="w-3.5 h-3.5" />,
        bgColor: 'bg-purple-50 dark:bg-purple-950/50 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800',
        badge: 'Autentikasi',
      };
    }
    return {
      icon: <Activity className="w-3.5 h-3.5" />,
      bgColor: 'bg-[#e6f4f2] dark:bg-slate-800 text-[#0d6b63] dark:text-teal-300 border-teal-200 dark:border-teal-800',
      badge: 'Aktivitas',
    };
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 transition-colors cursor-pointer"
        title="Notifikasi & Pembaruan Sistem"
        aria-label="Buka Notifikasi"
        aria-expanded={isOpen}
      >
        <Bell className="w-4 h-4" />
        
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-rose-500 text-[10px] font-extrabold text-white flex items-center justify-center shadow-xs ring-2 ring-white dark:ring-slate-800 animate-pulse">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown Popover */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white dark:bg-[#1e293b] border border-[#eaeff5] dark:border-[#334155] rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col">
          {/* Header */}
          <div className="p-4 border-b border-[#eaeff5] dark:border-[#334155] bg-[#f8fafc] dark:bg-slate-800/60">
            <div className="flex items-center justify-between gap-2 mb-2.5">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-[#e6f4f2] dark:bg-teal-950/50 text-[#0d6b63] dark:text-teal-400 flex items-center justify-center">
                  <Bell className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-[#1e293b] dark:text-white leading-tight">
                    Notifikasi Sistem
                  </h3>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className={`w-1.5 h-1.5 rounded-full ${realtimeStatus === 'connected' ? 'bg-emerald-500 animate-ping' : 'bg-amber-500'}`} />
                    <span className="text-[10px] font-medium text-slate-400 dark:text-slate-400">
                      {realtimeStatus === 'connected' ? 'Sinkron Cloud Realtime' : 'Menyambungkan...'}
                    </span>
                  </div>
                </div>
              </div>

              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllAsRead}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#0d6b63] dark:text-teal-400 hover:bg-[#e6f4f2] dark:hover:bg-slate-700 transition-colors cursor-pointer"
                  title="Tandai semua notifikasi sudah dibaca"
                >
                  <CheckCheck className="w-3.5 h-3.5" />
                  <span>Tandai dibaca</span>
                </button>
              )}
            </div>

            {/* Filter Tabs */}
            <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-900/60 p-1 rounded-xl">
              <button
                onClick={() => setFilter('all')}
                className={`flex-1 py-1 px-2 rounded-lg text-[11px] font-bold transition-all cursor-pointer ${
                  filter === 'all'
                    ? 'bg-white dark:bg-slate-800 text-[#0d6b63] dark:text-teal-400 shadow-2xs'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-300'
                }`}
              >
                Semua ({logs.length})
              </button>
              <button
                onClick={() => setFilter('unread')}
                className={`flex-1 py-1 px-2 rounded-lg text-[11px] font-bold transition-all cursor-pointer ${
                  filter === 'unread'
                    ? 'bg-white dark:bg-slate-800 text-[#0d6b63] dark:text-teal-400 shadow-2xs'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-300'
                }`}
              >
                Belum Dibaca ({unreadCount})
              </button>
            </div>
          </div>

          {/* List Content */}
          <div className="max-h-80 overflow-y-auto divide-y divide-[#eaeff5] dark:divide-[#334155]/60">
            {displayLogs.length === 0 ? (
              <div className="py-10 px-4 text-center">
                <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 mx-auto flex items-center justify-center mb-2">
                  <BellOff className="w-6 h-6" />
                </div>
                <p className="text-xs font-bold text-slate-700 dark:text-slate-200">
                  {filter === 'unread' ? 'Semua notifikasi telah dibaca' : 'Belum ada notifikasi'}
                </p>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  Setiap aktivitas penambahan atau perubahan data akan tampil di sini.
                </p>
              </div>
            ) : (
              displayLogs.slice(0, 15).map((log) => {
                const isRead = readIds.includes(log.id);
                const meta = getLogMeta(log.aktivitas);

                return (
                  <div
                    key={log.id}
                    onClick={() => handleItemClick(log.id, log.aktivitas)}
                    className={`p-3.5 transition-colors cursor-pointer flex items-start gap-3 ${
                      !isRead 
                        ? 'bg-teal-50/40 dark:bg-teal-950/20 hover:bg-teal-50/80 dark:hover:bg-teal-950/40' 
                        : 'hover:bg-slate-50 dark:hover:bg-slate-800/60'
                    }`}
                  >
                    {/* Activity Icon */}
                    <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 border ${meta.bgColor}`}>
                      {meta.icon}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1 mb-1">
                        <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                          {log.user || 'Sistem'}
                        </span>
                        <span className="text-[10px] text-slate-400 font-medium">
                          {getRelativeTime(log.tanggal || log.created_at)}
                        </span>
                      </div>

                      <p className="text-xs font-semibold text-slate-800 dark:text-slate-100 leading-snug line-clamp-2">
                        {log.aktivitas}
                      </p>
                    </div>

                    {/* Unread indicator */}
                    {!isRead && (
                      <span className="w-2 h-2 rounded-full bg-teal-500 shrink-0 mt-1.5" />
                    )}
                  </div>
                );
              })
            )}
          </div>

          {/* Footer */}
          <div className="p-2.5 border-t border-[#eaeff5] dark:border-[#334155] bg-[#f8fafc] dark:bg-slate-800/60 flex items-center justify-between text-[11px]">
            {isSuperAdmin ? (
              <Link
                href="/backup"
                onClick={() => setIsOpen(false)}
                className="text-[#0d6b63] dark:text-teal-400 font-bold hover:underline inline-flex items-center gap-1 px-2 py-1"
              >
                <span>Buka Riwayat Audit Trail</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            ) : (
              <span className="text-slate-400 font-medium px-2 py-1">
                Pemberitahuan Sistem Terpadu
              </span>
            )}

            <button
              onClick={() => setIsOpen(false)}
              className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 px-2 py-1 font-semibold cursor-pointer"
            >
              Tutup
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
