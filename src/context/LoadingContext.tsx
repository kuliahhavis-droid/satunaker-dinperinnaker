'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

interface LoadingContextType {
  isLoading: boolean;
  progress: number;
  startLoading: () => void;
  finishLoading: () => void;
}

const LoadingContext = createContext<LoadingContextType>({
  isLoading: false,
  progress: 0,
  startLoading: () => {},
  finishLoading: () => {},
});

export function LoadingProvider({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const startLoading = useCallback(() => {
    setIsLoading(true);
    setProgress(35);
    setTimeout(() => {
      setProgress(75);
    }, 150);
  }, []);

  const finishLoading = useCallback(() => {
    setProgress(100);
    setTimeout(() => {
      setIsLoading(false);
      setTimeout(() => {
        setProgress(0);
      }, 350);
    }, 200);
  }, []);

  // Preloader pada awal masuk web (initial mount / refresh)
  useEffect(() => {
    // Animasi progress bar awal
    const t1 = setTimeout(() => {
      setProgress(75);
    }, 150);

    const t2 = setTimeout(() => {
      finishLoading();
    }, 600);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [finishLoading]);

  return (
    <LoadingContext.Provider
      value={{
        isLoading,
        progress,
        startLoading,
        finishLoading,
      }}
    >
      {children}
    </LoadingContext.Provider>
  );
}

export const usePageLoading = () => useContext(LoadingContext);
