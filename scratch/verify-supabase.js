const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');

// Parse .env.local manually without external dependencies
let envVars = {};
try {
  const envPath = path.resolve(__dirname, '../.env.local');
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#')) {
        const eqIdx = trimmed.indexOf('=');
        if (eqIdx !== -1) {
          const key = trimmed.slice(0, eqIdx).trim();
          const val = trimmed.slice(eqIdx + 1).trim();
          envVars[key] = val;
        }
      }
    }
  }
} catch (e) {
  // Ignore
}

const supabaseUrl = envVars.NEXT_PUBLIC_SUPABASE_URL || 'https://twfgsuycpikbnxpsrwrk.supabase.co';
const supabaseKey = envVars.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'sb_publishable_rpIXGEz9404NZD_eEXvbbg_AARU16Rr';

console.log('====================================================');
console.log('🔍 MEMERIKSA KONEKSI KE SUPABASE CLOUD...');
console.log('URL:', supabaseUrl);
console.log('Key:', supabaseKey.substring(0, 15) + '...');
console.log('====================================================\n');

const supabase = createClient(supabaseUrl, supabaseKey);

async function testSupabase() {
  const tables = ['unit_kerja', 'profiles', 'data_records', 'log_aktivitas'];
  let allGood = true;

  for (const table of tables) {
    process.stdout.write(`Mengecek tabel [${table}]... `);
    try {
      const { data, error } = await supabase.from(table).select('*').limit(5);

      if (error) {
        allGood = false;
        console.log('❌ GAGAL');
        console.log(`   Pesan error: ${error.message} (Kode: ${error.code})`);
        if (error.code === 'PGRST205') {
          console.log(`   👉 Keterangan: Tabel '${table}' belum dibuat di skema database.`);
        }
      } else {
        console.log(`✅ AKTIF (terdeteksi ${data.length} baris data)`);
      }
    } catch (err) {
      allGood = false;
      console.log('❌ ERROR JARINGAN / KONEKSI:', err.message);
    }
  }

  console.log('\n====================================================');
  if (allGood) {
    console.log('🎉 SEMPURNA! Seluruh tabel Supabase telah aktif dan siap digunakan.');
  } else {
    console.log('⚠️ STATUS: Basis data Supabase belum memiliki tabel skema.');
    console.log('\n👉 CARA MEMBUAT TABEL (1 Langkah Mudah):');
    console.log('1. Buka dashboard Supabase: https://supabase.com/dashboard/project/twfgsuycpikbnxpsrwrk/sql');
    console.log('2. Buka file "supabase_schema.sql" di folder proyek satudata-nextjs');
    console.log('3. Salin seluruh teksnya, tempelkan ke SQL Editor Supabase, lalu klik "Run".');
    console.log('4. Jalankan ulang perintah: node scratch/verify-supabase.js');
  }
  console.log('====================================================');
}

testSupabase().catch(err => {
  console.error('Terjadi kesalahan tidak terduga:', err);
});
