import type { Metadata } from "next";
import "./globals.css";
import { DataProvider } from "@/context/DataContext";
import { ThemeProvider } from "@/context/ThemeContext";
import { LoadingProvider } from "@/context/LoadingContext";
import GlobalPreloader from "@/components/ui/GlobalPreloader";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "SatuNaker - Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga",
  description: "Portal Resmi SatuNaker: Pengelolaan Data Statistik Sektoral dan Pelaporan Kinerja Terpadu Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.",
  keywords: ["SatuNaker", "Satu Data", "DINPERINNAKER", "Purbalingga", "Statistik Sektoral", "Tenaga Kerja", "Perindustrian"],
  authors: [{ name: "DINPERINNAKER Kabupaten Purbalingga" }],
  icons: {
    icon: "/images/logo-satudata.svg",
    shortcut: "/images/logo-purbalingga.png",
    apple: "/images/logo-purbalingga.png",
  },
  openGraph: {
    title: "SatuNaker - Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga",
    description: "Portal Data Terpadu Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.",
    type: "website",
    locale: "id_ID",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id" suppressHydrationWarning>
      <body className="antialiased min-h-screen bg-[#f2f7ff] dark:bg-[#0b1120] text-[#25396e] dark:text-[#f8fafc] transition-colors duration-200">
        <ThemeProvider>
          <LoadingProvider>
            <GlobalPreloader />
            <DataProvider>
              {children}
              <Toaster position="top-right" richColors />
            </DataProvider>
          </LoadingProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
