import type { Metadata } from "next";
import { Plus_Jakarta_Sans, Inter } from "next/font/google";
import "./globals.css";
import { DataProvider } from "@/context/DataContext";
import { ThemeProvider } from "@/context/ThemeContext";
import { LoadingProvider } from "@/context/LoadingContext";
import GlobalPreloader from "@/components/ui/GlobalPreloader";
import { Toaster } from "sonner";

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

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
    <html lang="id" className={`${plusJakartaSans.variable} ${inter.variable}`} suppressHydrationWarning>
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
