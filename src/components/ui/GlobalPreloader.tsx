'use client';

import React from 'react';
import { usePageLoading } from '@/context/LoadingContext';

export default function GlobalPreloader() {
  const { isLoading, progress } = usePageLoading();

  return (
    <>
      {/* Top Slim Page Progress Bar (Persis seperti #page-progress-bar di Laravel) */}
      <div
        id="page-progress-bar"
        className="fixed top-0 left-0 h-[3px] z-[999999] pointer-events-none transition-all duration-300"
        style={{
          width: `${progress}%`,
          opacity: progress > 0 && progress < 100 ? 1 : progress === 100 ? 1 : 0,
          background: 'linear-gradient(90deg, #2a92a2 0%, #46b3c3 50%, #217784 100%)',
          boxShadow: '0 0 10px rgba(42, 146, 162, 0.8)',
          transitionTimingFunction: 'cubic-bezier(0.16, 1, 0.3, 1)',
        }}
      />

      {/* Global Preloader Fullscreen Overlay (Persis seperti #global-preloader di Laravel) */}
      <div
        id="global-preloader"
        className={`fixed inset-0 w-screen h-screen z-[99999] flex items-center justify-center bg-white dark:bg-[#0b1120] transition-all duration-350 ease-out select-none ${
          isLoading
            ? 'opacity-100 visible pointer-events-auto'
            : 'opacity-0 invisible pointer-events-none'
        }`}
        style={{
          transitionTimingFunction: 'cubic-bezier(0.16, 1, 0.3, 1)',
        }}
      >
        <div className="flex flex-col items-center justify-center text-center">
          {/* Spinner Ring Wrapper (68px) with Logo in the center */}
          <div className="relative w-[68px] h-[68px] flex items-center justify-center mb-3.5">
            {/* Spinning Ring */}
            <div
              className="absolute inset-0 w-[68px] h-[68px] rounded-full border-[3px] border-[#2a92a2]/20 border-t-[#0d6b63] dark:border-t-[#2dd4bf] animate-spin"
              style={{
                animationDuration: '0.8s',
              }}
            />

            {/* Logo in Center */}
            <img
              src="/images/logo-satudata.svg"
              alt="Logo DINPERINNAKER"
              className="w-8 h-8 object-contain relative z-10"
            />
          </div>

          {/* Teks Brand & Subteks */}
          <span className="block font-sans text-[1rem] font-extrabold tracking-tight text-[#154D56] dark:text-[#46b3c3] mt-1">
            DINPERINNAKER
          </span>
          <span className="text-[0.72rem] text-[#64748b] dark:text-slate-400 font-medium mt-0.5">
            Sistem Satu Data Sektoral
          </span>
        </div>
      </div>
    </>
  );
}
