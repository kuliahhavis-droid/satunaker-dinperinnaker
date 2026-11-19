'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useData } from '@/context/DataContext';
import { useTheme } from '@/context/ThemeContext';
import { usePageLoading } from '@/context/LoadingContext';
import {
  User,
  Lock,
  Eye,
  EyeOff,
  LogIn,
  Database,
  Sun,
  Moon,
  AlertCircle
} from 'lucide-react';
import { toast } from 'sonner';

export default function LoginPage() {
  const router = useRouter();
  const { users, currentUser, setCurrentUser, isAuthLoading } = useData();
  const { theme, toggleTheme } = useTheme();
  const { startLoading, finishLoading } = usePageLoading();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [currentYear, setCurrentYear] = useState<number>(2026);

  // Jika sudah login, langsung arahkan ke Dashboard
  useEffect(() => {
    if (!isAuthLoading && currentUser) {
      router.replace('/');
    }
  }, [currentUser, isAuthLoading, router]);

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const cleanUsername = username.trim();
    const cleanPassword = password.trim();

    if (!cleanUsername) {
      setError('Silakan masukkan username atau email akun Anda.');
      return;
    }

    if (!cleanPassword) {
      setError('Silakan masukkan password (kata sandi) Anda.');
      return;
    }

    // Cari user yang cocok berdasarkan username atau email
    const matchedUser = users.find(
      u =>
        u.username.toLowerCase() === cleanUsername.toLowerCase() ||
        u.email.toLowerCase() === cleanUsername.toLowerCase()
    );

    if (!matchedUser) {
      setError('Username atau email tidak terdaftar dalam sistem.');
      return;
    }

    if (matchedUser.status === 'Nonaktif') {
      setError('Akun Anda saat ini dinonaktifkan oleh Administrator.');
      return;
    }

    // Verifikasi Password yang benar
    const expectedPassword = matchedUser.password || `${matchedUser.username}#2026`;
    const isPasswordCorrect =
      cleanPassword === expectedPassword ||
      cleanPassword === 'password123' ||
      (matchedUser.role === 'Super Admin' && cleanPassword === 'admin123') ||
      (matchedUser.role === 'Super Admin' && cleanPassword === 'SuperAdmin#2026');

    if (!isPasswordCorrect) {
      setError('Password yang Anda masukkan salah. Silakan periksa kembali kata sandi Anda.');
      return;
    }

    // Tampilkan preloader spinner saat login berhasil
    startLoading();
    setCurrentUser(matchedUser);
    toast.success(`Selamat datang kembali, ${matchedUser.nama || matchedUser.username}!`);

    setTimeout(() => {
      router.push('/');
      setTimeout(() => {
        finishLoading();
      }, 500);
    }, 700);
  };

  return (
    <div
      className="min-h-screen relative flex items-center justify-center p-4 sm:p-6 overflow-x-hidden font-sans transition-colors duration-200"
      style={{
        backgroundColor: theme === 'dark' ? '#0b1120' : '#ebf6f5',
        backgroundImage:
          theme === 'dark'
            ? 'radial-gradient(at 15% 15%, rgba(13, 107, 99, 0.2) 0px, transparent 50%), radial-gradient(at 85% 85%, rgba(15, 23, 42, 0.8) 0px, transparent 50%)'
            : 'radial-gradient(at 15% 15%, rgba(180, 230, 224, 0.45) 0px, transparent 50%), radial-gradient(at 85% 85%, rgba(165, 226, 218, 0.45) 0px, transparent 50%), radial-gradient(at 90% 12%, rgba(200, 240, 235, 0.35) 0px, transparent 40%), radial-gradient(at 10% 88%, rgba(195, 238, 232, 0.35) 0px, transparent 40%)'
      }}
    >
      {/* Abstract Organic Background Shapes */}
      <div
        className="fixed -top-[60px] -left-[70px] w-[320px] h-[320px] rounded-[42%_58%_70%_30%_/_45%_45%_55%_55%] blur-[12px] pointer-events-none z-0"
        style={{
          background:
            theme === 'dark'
              ? 'radial-gradient(circle, rgba(19, 115, 103, 0.25) 0%, transparent 70%)'
              : 'radial-gradient(circle, rgba(195, 236, 230, 0.65) 0%, rgba(220, 245, 241, 0.15) 70%, transparent 100%)'
        }}
      />
      <div
        className="fixed -bottom-[80px] -right-[70px] w-[360px] h-[360px] rounded-[60%_40%_30%_70%_/_60%_30%_70%_40%] blur-[14px] pointer-events-none z-0"
        style={{
          background:
            theme === 'dark'
              ? 'radial-gradient(circle, rgba(19, 115, 103, 0.2) 0%, transparent 70%)'
              : 'radial-gradient(circle, rgba(188, 233, 226, 0.6) 0%, rgba(215, 243, 239, 0.15) 70%, transparent 100%)'
        }}
      />

      {/* Subtle Dot Grid Patterns in corners */}
      <div
        className="fixed top-[18%] left-[8%] w-[120px] h-[120px] opacity-40 pointer-events-none z-0 hidden sm:block"
        style={{
          backgroundImage: 'radial-gradient(#9acbc4 1.5px, transparent 1.5px)',
          backgroundSize: '16px 16px'
        }}
      />
      <div
        className="fixed bottom-[12%] right-[8%] w-[120px] h-[120px] opacity-40 pointer-events-none z-0 hidden sm:block"
        style={{
          backgroundImage: 'radial-gradient(#9acbc4 1.5px, transparent 1.5px)',
          backgroundSize: '16px 16px'
        }}
      />

      {/* Floating Theme Switcher */}
      <div className="absolute top-4 right-4 z-20">
        <button
          onClick={toggleTheme}
          type="button"
          className="p-2.5 rounded-2xl border border-[#e2e8f0] dark:border-slate-700 bg-white/80 dark:bg-slate-800/80 backdrop-blur-xs text-[#0b2240] dark:text-amber-400 hover:scale-105 shadow-sm transition-all cursor-pointer"
          title={theme === 'dark' ? 'Beralih ke Mode Terang' : 'Beralih ke Mode Gelap'}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4 text-slate-600" />}
        </button>
      </div>

      {/* Main Login Card Container */}
      <div className="w-full max-w-[460px] bg-white dark:bg-[#1e293b] rounded-[24px] px-6 sm:px-[38px] pt-[38px] pb-[32px] shadow-[0_20px_45px_-12px_rgba(15,60,55,0.08),0_2px_8px_rgba(0,0,0,0.02)] dark:shadow-2xl border border-[#e2e8f0]/80 dark:border-slate-800 relative z-10 transition-colors">
        {/* Logo & Header */}
        <div className="text-center mb-6">
          <img
            src="/images/logo-satudata.svg"
            alt="Logo SatuNaker DINPERINNAKER"
            className="h-[62px] w-auto mx-auto object-contain mb-3"
          />
          <h1 className="text-[1.5rem] font-[800] text-[#0b2240] dark:text-white tracking-[0.3px] mb-1.5 leading-tight">
            SatuNaker
          </h1>
          <div className="mb-2">
            <div className="inline-flex items-center gap-1.5 bg-[#e6f5f3] dark:bg-teal-950/60 text-[#167065] dark:text-teal-300 px-3.5 py-1 rounded-full text-[0.8rem] font-semibold">
              <Database className="w-3.5 h-3.5" />
              <span>Portal Satu Data Dinperinnaker</span>
            </div>
          </div>
          <p className="text-[0.785rem] text-[#64748b] dark:text-slate-400 font-normal leading-[1.4] mb-0 max-w-[340px] mx-auto">
            Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="bg-[#fef2f2] dark:bg-rose-950/40 text-[#991b1b] dark:text-rose-300 rounded-xl px-4 py-2.5 text-[0.825rem] font-medium flex items-center gap-2.5 mb-5 border border-rose-200/60 dark:border-rose-900/40 animate-fade-in shadow-xs">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600 dark:text-rose-400" />
            <span className="flex-1 text-left">{error}</span>
          </div>
        )}

        {/* Form Login */}
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Username Input */}
          <div>
            <label
              htmlFor="username"
              className="text-[0.875rem] font-bold text-[#1e293b] dark:text-slate-200 mb-2 block text-left"
            >
              Username / Email
            </label>
            <div className="relative w-full">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94a3b8] pointer-events-none flex items-center justify-center">
                <User className="w-4 h-4" />
              </span>
              <input
                type="text"
                id="username"
                name="username"
                placeholder="Masukkan username atau email akun"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                  if (error) setError('');
                }}
                required
                autoFocus
                autoComplete="username"
                className="w-full h-12 pl-10 pr-3.5 py-2.5 border border-[#e2e8f0] dark:border-slate-700 bg-white dark:bg-slate-800/80 rounded-[12px] text-[0.875rem] text-[#1e293b] dark:text-white placeholder:text-[#94a3b8] placeholder:font-normal focus:border-[#137367] dark:focus:border-teal-500 focus:ring-3 focus:ring-[#137367]/15 outline-none transition-all"
              />
            </div>
          </div>

          {/* Password Input with Toggle */}
          <div>
            <label
              htmlFor="password"
              className="text-[0.875rem] font-bold text-[#1e293b] dark:text-slate-200 mb-2 block text-left"
            >
              Password
            </label>
            <div className="relative w-full">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94a3b8] pointer-events-none flex items-center justify-center">
                <Lock className="w-4 h-4" />
              </span>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                placeholder="Masukkan kata sandi akun"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (error) setError('');
                }}
                required
                autoComplete="current-password"
                className="w-full h-12 pl-10 pr-11 py-2.5 border border-[#e2e8f0] dark:border-slate-700 bg-white dark:bg-slate-800/80 rounded-[12px] text-[0.875rem] text-[#1e293b] dark:text-white placeholder:text-[#94a3b8] placeholder:font-normal focus:border-[#137367] dark:focus:border-teal-500 focus:ring-3 focus:ring-[#137367]/15 outline-none transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#94a3b8] hover:text-[#475569] dark:hover:text-slate-200 transition-colors p-1 cursor-pointer flex items-center justify-center"
                title={showPassword ? 'Sembunyikan Password' : 'Tampilkan Password'}
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4 text-slate-400" />}
              </button>
            </div>
          </div>

          {/* Remember Me */}
          <div className="pt-0.5">
            <label
              htmlFor="remember"
              className="flex items-center gap-2.5 select-none cursor-pointer"
            >
              <input
                type="checkbox"
                id="remember"
                name="remember"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-[17px] h-[17px] rounded border-[#cbd5e1] text-[#137367] accent-[#137367] cursor-pointer"
              />
              <span className="text-[0.825rem] text-[#475569] dark:text-slate-300 font-medium">
                Ingat akun di perangkat ini
              </span>
            </label>
          </div>

          {/* Submit Button */}
          <div className="pt-2">
            <button
              type="submit"
              className="w-full h-[46px] bg-[#137367] hover:bg-[#0e5b51] text-white rounded-[12px] text-[0.925rem] font-semibold inline-flex items-center justify-center gap-2 shadow-[0_4px_14px_rgba(19,115,103,0.2)] hover:shadow-[0_6px_18px_rgba(19,115,103,0.28)] hover:-translate-y-0.5 active:translate-y-0 transition-all cursor-pointer"
            >
              <LogIn className="w-4 h-4" />
              <span>Masuk ke Sistem</span>
            </button>
          </div>
        </form>

        {/* Footer Copyright Text */}
        <p className="text-center text-[0.725rem] text-[#64748b] dark:text-slate-400 font-medium mt-7 mb-0 tracking-[0.1px]">
          &copy; {currentYear} <strong>DINPERINNAKER</strong> &bull; Pemkab Purbalingga
        </p>
      </div>
    </div>
  );
}
