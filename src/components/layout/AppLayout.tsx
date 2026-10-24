'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useData } from '@/context/DataContext';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
}

export default function AppLayout({ children, title }: AppLayoutProps) {
  const router = useRouter();
  const { currentUser, isAuthLoading } = useData();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isAuthLoading && !currentUser) {
      router.replace('/login');
    }
  }, [currentUser, isAuthLoading, router]);

  // Loading state saat verifikasi sesi login
  if (isAuthLoading || !currentUser) {
    return (
      <div className="min-h-screen bg-[#f0f5fa] dark:bg-[#0b1120] flex items-center justify-center p-4">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-[#137367]/20 border-t-[#137367] rounded-full animate-spin" />
          <p className="text-xs font-semibold text-slate-500 tracking-wide">
            Memeriksa autentikasi sesi pengguna...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f0f5fa] dark:bg-[#0b1120] flex relative overflow-x-hidden">
      {/* Background Watermark (Purbalingga Seal) */}
      <div 
        aria-hidden="true" 
        className="fixed inset-0 pointer-events-none z-0 flex items-center justify-center opacity-[0.045] dark:opacity-[0.025]"
      >
        <img 
          src="/images/logo-purbalingga.png" 
          alt="Purbalingga Watermark" 
          className="w-[520px] max-w-[85vw] object-contain select-none"
        />
      </div>

      {/* Sidebar Navigation */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64 relative z-10">
        <Topbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} title={title} />
        
        <main className="flex-1 p-4 lg:p-8 pb-14 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
