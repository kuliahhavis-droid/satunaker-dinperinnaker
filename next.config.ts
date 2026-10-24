import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async redirects() {
    return [
      { source: '/input-data', destination: '/kelola-data', permanent: true },
      { source: '/monitoring', destination: '/', permanent: true },
      { source: '/bidang', destination: '/unit-kerja', permanent: true },
      { source: '/indikator', destination: '/kelola-data', permanent: true },
      { source: '/statistik', destination: '/', permanent: true },
      { source: '/dashboard', destination: '/', permanent: true },
    ];
  },
};

export default nextConfig;
