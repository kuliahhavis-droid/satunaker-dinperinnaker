import os
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOC_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx"

def set_academic_table_borders(table):
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
            
    tblBorders = OxmlElement('w:tblBorders')
    
    # Table top border (1 pt = 8 eighths of pt)
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '8')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), '000000')
    tblBorders.append(top)
    
    # Table bottom border (1 pt)
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tblBorders.append(bottom)
    
    for side in ['left', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'none')
        tblBorders.append(b)
        
    tblPr.append(tblBorders)
    
    # Header bottom border on each cell of row 0
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for child in list(tcPr):
                if child.tag.endswith('tcBorders'):
                    tcPr.remove(child)
            tcBorders = OxmlElement('w:tcBorders')
            b = OxmlElement('w:bottom')
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '6') # 0.75 pt
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), '000000')
            tcBorders.append(b)
            for side in ['top', 'left', 'right']:
                nb = OxmlElement(f'w:{side}')
                nb.set(qn('w:val'), 'none')
                tcBorders.append(nb)
            tcPr.append(tcBorders)

def format_cell(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=Pt(10)):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def create_table_data(doc, headers, data, col_widths, col_alignments):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for col_idx, h in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        cell.width = col_widths[col_idx]
        format_cell(cell, h, bold=True, align=col_alignments[col_idx], font_size=Pt(10))
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            is_num_col = (col_idx == 0)
            align = col_alignments[col_idx]
            format_cell(cell, str(val), bold=is_num_col, align=align, font_size=Pt(10))
    set_academic_table_borders(table)
    return table

def add_heading_p(doc, text, bold=True, space_before=Pt(8), space_after=Pt(4)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = space_before
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 2.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = bold
    return p

def add_caption_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.first_line_indent = Cm(1.0)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    return p

def main():
    print("Loading document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. Locate paragraph: 2. Analisis Kebutuhan (Analysis)
    p_analisis_idx = None
    p_rbac_idx = None
    for idx, p in enumerate(doc.paragraphs):
        if "2. Analisis Kebutuhan (Analysis)" in p.text:
            p_analisis_idx = idx
        elif "c. Matriks Kebutuhan Hak Akses Pengguna (RBAC)" in p.text:
            p_rbac_idx = idx
            break

    print(f"Found Analisis Kebutuhan at p={p_analisis_idx}, RBAC at p={p_rbac_idx}")
    target_p = doc.paragraphs[p_rbac_idx]

    # Delete the old hardware table (Table 8) and old software table (Table 9)
    # Let's find them by header text
    t_hw = None
    t_sw = None
    for t in doc.tables:
        header = [c.text.strip() for c in t.rows[0].cells]
        if "Komponen Perangkat" in header:
            t_hw = t
        elif "Perangkat Lunak" in header:
            t_sw = t

    if t_hw:
        t_hw._element.getparent().remove(t_hw._element)
        print("Removed old Hardware table.")
    if t_sw:
        t_sw._element.getparent().remove(t_sw._element)
        print("Removed old Software table.")

    # Delete old paragraphs between p_analisis_idx and target_p
    # Check paragraphs to remove
    paras_to_del = []
    for p in doc.paragraphs[p_analisis_idx + 1:p_rbac_idx]:
        paras_to_del.append(p)
    for p in paras_to_del:
        p._element.getparent().remove(p._element)
        print(f"Deleted old paragraph: {p.text[:40]}")

    # Now create the new 5 tables and text, and insert before target_p
    # Introduction to Analisis Kebutuhan
    p_intro = add_body_p(doc, "Pada fase analisis kebutuhan, dilakukan eksplorasi terperinci terhadap kebutuhan non-fungsional (mencakup spesifikasi perangkat keras, perangkat lunak, teknologi website, arsitektur penyimpanan data, dan katalog aset visual) serta kebutuhan fungsional otorisasi peran pengguna (Role-Based Access Control) di lingkungan DINPERINNAKER Kabupaten Purbalingga.")
    target_p._p.addprevious(p_intro._p)

    # 1. Kebutuhan Hardware
    p_h1 = add_heading_p(doc, "a. Spesifikasi Kebutuhan Perangkat Keras (Hardware)")
    p_b1 = add_body_p(doc, "Spesifikasi kebutuhan perangkat keras mencakup lingkungan komputasi pengembang sistem serta spesifikasi minimal perangkat pengguna (klien dinas) baik melalui komputer desktop, laptop, maupun telepon pintar (smartphone) sebagaimana disajikan pada Tabel 3.1.")
    p_c1 = add_caption_p(doc, "Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)")
    
    hw_headers = ["No.", "Kategori Perangkat", "Spesifikasi Teknis Minimal"]
    hw_widths = [Cm(1.2), Cm(4.8), Cm(10.0)]
    hw_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    hw_data = [
        ["1", "Komputer Pengembang (Developer PC/Laptop)", "Prosesor AMD Ryzen 5 5500U / Intel Core i5 Generasi ke-11 (Base Clock 2.1 GHz, 6 Core, 12 Thread), Memori RAM 16 GB DDR4 Dual Channel 3200 MHz, Media Penyimpanan 512 GB SSD M.2 NVMe PCIe 3.0, Layar 14 Inci Full HD (1920x1080 piksel), Keyboard & Touchpad terintegrasi, Koneksi Internet Kecepatan Stabil."],
        ["2", "Perangkat Klien / Pengguna Dinas (Desktop / Laptop)", "Prosesor Dual Core 2.0 GHz (Intel Pentium Gold / Celeron / Core i3 setara), Memori RAM Minimal 2 GB (Disarankan 4 GB untuk kelancaran multitasking), Ruang Kosong Penyimpanan 500 MB untuk Cache Browser, Resolusi Layar Minimal 1366x768 piksel, Koneksi Jaringan Intranet / Internet Wi-Fi Dinas."],
        ["3", "Perangkat Klien Mobile (Smartphone / Tablet)", "Prosesor Quad-Core 1.5 GHz, Memori RAM Minimal 2 GB, Layar Sentuh dengan Resolusi Minimal 360x640 piksel (Mendukung Tampilan Responsif Mobile PWA), Jaringan Seluler 4G LTE / Wi-Fi."],
        ["4", "Perangkat Keras Input dan Output", "Keyboard Standar QWERTY, Mouse Optik / Touchpad, Monitor Eksternal Resolusi Minimal 1920x1080 piksel (Opsional untuk Analisis Dasbor), Printer Laserjet / Inkjet Berwarna untuk Pencetakan Laporan Ber-Kop Resmi."]
    ]
    t1 = create_table_data(doc, hw_headers, hw_data, hw_widths, hw_aligns)
    
    target_p._p.addprevious(p_h1._p)
    target_p._p.addprevious(p_b1._p)
    target_p._p.addprevious(p_c1._p)
    target_p._p.addprevious(t1._tbl)

    # 2. Kebutuhan Software
    p_h2 = add_heading_p(doc, "b. Spesifikasi Kebutuhan Perangkat Lunak (Software)")
    p_b2 = add_body_p(doc, "Spesifikasi lingkungan perangkat lunak pengembangan dan operasional mencakup sistem operasi, perangkat lunak editor program, pengelola paket pustaka, platform basis data awan, serta piranti peramban web modern sebagaimana disajikan pada Tabel 3.2.")
    p_c2 = add_caption_p(doc, "Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)")
    
    sw_headers = ["No.", "Perangkat Lunak", "Deskripsi dan Versi Perangkat"]
    sw_widths = [Cm(1.2), Cm(4.5), Cm(10.3)]
    sw_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    sw_data = [
        ["1", "Sistem Operasi", "Microsoft Windows 11 Home/Pro 64-bit sebagai lingkungan pengembangan utama; kompatibel dengan Windows 10/11, macOS, Linux, Android, dan iOS pada peramban pengguna."],
        ["2", "Lingkungan Pengembangan (IDE)", "Visual Studio Code v1.95+ / Antigravity IDE dilengkapi ekstensi Tailwind CSS IntelliSense, ESLint, Prettier Code Formatter, dan Prisma/PostgreSQL Client Tools."],
        ["3", "Runtime & Package Manager", "Node.js LTS v20.18.0 / v22.11.0 sebagai runtime engine JavaScript sisi server dan Node Package Manager (NPM) v10.8.2 untuk manajemen dependensi pustaka."],
        ["4", "Platform Basis Data & Backend", "Supabase Cloud Console berbasis PostgreSQL 15+ yang mendukung Row Level Security (RLS), Realtime WebSocket broadcasting, serta manajemen otentikasi."],
        ["5", "Peramban Web (Web Browser)", "Google Chrome v130+, Microsoft Edge v130+, dan Mozilla Firefox v132+ yang mendukung Chrome DevTools, Network Throttling, dan mode uji tampilan responsif."],
        ["6", "Desain Antarmuka & Wireframe", "Figma Desktop & Web Application untuk perancangan hierarki tata letak visual antarmuka pengguna (UI), wireframing, dan prototipe desain interaktif."],
        ["7", "Pengendali Versi (Version Control)", "Git v2.45+ dan GitHub Cloud Repository untuk pelacakan riwayat versi kode sumber, kolaborasi tim, dan sinkronisasi repositori cadangan."]
    ]
    t2 = create_table_data(doc, sw_headers, sw_data, sw_widths, sw_aligns)
    
    target_p._p.addprevious(p_h2._p)
    target_p._p.addprevious(p_b2._p)
    target_p._p.addprevious(p_c2._p)
    target_p._p.addprevious(t2._tbl)

    # 3. Teknologi Website
    p_h3 = add_heading_p(doc, "c. Spesifikasi Teknologi Website (Web Technology Stack)")
    p_b3 = add_body_p(doc, "Sistem SatuNaker dikembangkan dengan memanfaatkan tumpukan teknologi modern (modern web stack) berbasis kerangka kerja Next.js 16 App Router dan pustaka reaktif React 19 guna menghadirkan performa tinggi, efisiensi kompilasi Turbopack, serta keandalan antarmuka sebagaimana disajikan pada Tabel 3.3.")
    p_c3 = add_caption_p(doc, "Tabel 3.3 Spesifikasi Teknologi Website (Web Technology Stack)")
    
    web_headers = ["No.", "Teknologi / Pustaka", "Peran dan Spesifikasi Teknis"]
    web_widths = [Cm(1.2), Cm(4.8), Cm(10.0)]
    web_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    web_data = [
        ["1", "Next.js 16.4.2", "Kerangka kerja (framework) utama React berbasis App Router dengan mesin bundling Turbopack berkecepatan tinggi, mendukung Server Components dan Client Components."],
        ["2", "React 19.3.0", "Pustaka dasar pengembangan antarmuka pengguna berbasis komponen deklaratif reaktif dengan performa optimalisasi rendering DOM tingkat tinggi."],
        ["3", "TypeScript 5.x", "Bahasa pemrograman superset JavaScript dengan sistem tipe statis ketat (static typing) guna mencegah galat pada masa kompilasi (compile-time safety)."],
        ["4", "Tailwind CSS v4.0", "Mesin utilitas CSS modern (utility-first) untuk penataan antarmuka responsif, konsistensi token warna kedinasan, dan performa pemuatan gaya yang sangat cepat."],
        ["5", "Lucide React v1.60.0", "Pustaka ikon grafis vektor berbasis SVG yang ringan, konsisten, dan mencakup lebih dari 500 ikon fungsional navigasi sistem."],
        ["6", "Framer Motion v14.5.0", "Pustaka animasi tingkat lanjut untuk transisi modal interaktif, transisi halaman, dan efek mikro-interaksi antarmuka yang halus dan elegan."],
        ["7", "Sonner v2.0.8", "Pustaka sistem notifikasi toast interaktif yang ringan dan reaktif untuk memberikan umpan balik langsung saat aksi data berhasil atau gagal diproses."],
        ["8", "SheetJS (xlsx v0.18.5)", "Pustaka pemroses spreadsheet tingkat lanjut untuk parsing, pembuatan struktur tabel dinamis, dan ekspor berkas Microsoft Excel (.xlsx) otomatis."],
        ["9", "Chart.js v4.5.1 & React-Chartjs-2", "Pustaka pembuat grafik data interaktif untuk visualisasi grafik batang dan grafik garis agregat data capaian kinerja dinas."],
        ["10", "Canvas-Confetti v1.9.4", "Pustaka efek visual perayaan berbasis kanvas saat proses ekspor laporan selesai dilakukan secara sukses oleh pengguna."]
    ]
    t3 = create_table_data(doc, web_headers, web_data, web_widths, web_aligns)
    
    target_p._p.addprevious(p_h3._p)
    target_p._p.addprevious(p_b3._p)
    target_p._p.addprevious(p_c3._p)
    target_p._p.addprevious(t3._tbl)

    # 4. Penyimpanan Data
    p_h4 = add_heading_p(doc, "d. Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)")
    p_b4 = add_body_p(doc, "Mekanisme penyimpanan data pada sistem SatuNaker dirancang secara hibrida multi-tier guna menjamin integritas data relasional, pembaruan waktu nyata (real-time), serta efisiensi penyimpanan fisik dokumen sebagaimana disajikan pada Tabel 3.4.")
    p_c4 = add_caption_p(doc, "Tabel 3.4 Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)")
    
    st_headers = ["No.", "Komponen Penyimpanan", "Arsitektur dan Mekanisme Kerja"]
    st_widths = [Cm(1.2), Cm(4.8), Cm(10.0)]
    st_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    st_data = [
        ["1", "Basis Data Relasional Cloud", "Supabase Cloud PostgreSQL 15+ sebagai media penyimpanan relasional terpusat dengan integritas referensial antar tabel unit_kerja, profiles, data_records, dan log_aktivitas."],
        ["2", "Engine Sinkronisasi Realtime", "Supabase Realtime Hub berbasis protokol WebSocket untuk penyiaran pembaruan data secara langsung ke antarmuka pengguna tanpa perlu refresh halaman."],
        ["3", "Penyimpanan Sisi Klien (Local Cache)", "Browser Web Storage (localStorage) dilengkapi mekanisme pembersihan otomatis satudata_clean_reset_v2 untuk menjaga performa rendering antarmuka pengguna."],
        ["4", "Repositori Bukti Fisik Digital", "Google Drive Cloud Storage resmi DINPERINNAKER untuk menyimpan berkas bukti fisik (PDF, PPT, DOCX, XLSX) yang dihubungkan melalui tautan URL aman."],
        ["5", "Mekanisme Pemulihan Bencana", "Modul cadangan mandiri (backup & restore) yang mengekspor skema dan data ke format SQL Dump (.sql) dan JSON Data Snapshot (.json)."]
    ]
    t4 = create_table_data(doc, st_headers, st_data, st_widths, st_aligns)
    
    target_p._p.addprevious(p_h4._p)
    target_p._p.addprevious(p_b4._p)
    target_p._p.addprevious(p_c4._p)
    target_p._p.addprevious(t4._tbl)

    # 5. Aset Visual
    p_h5 = add_heading_p(doc, "e. Katalog Aset Visual dan Desain Antarmuka")
    p_b5 = add_body_p(doc, "Guna menghadirkan citra profesional kedinasan dan konsistensi antarmuka pengguna, sistem SatuNaker menggunakan aset visual resmi, palet warna branding DINPERINNAKER, serta standarisasi tata letak laporan kedinasan sebagaimana disajikan pada Tabel 3.5.")
    p_c5 = add_caption_p(doc, "Tabel 3.5 Katalog Aset Visual dan Desain Antarmuka")
    
    av_headers = ["No.", "Komponen Aset Visual", "Spesifikasi dan Penerapan Desain"]
    av_widths = [Cm(1.2), Cm(4.8), Cm(10.0)]
    av_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    av_data = [
        ["1", "Lambang Resmi Daerah", "Logo Pemerintah Kabupaten Purbalingga dalam format vektor resolusi tinggi, digunakan pada halaman login, sidebar navigasi, dan kop surat resmi cetak."],
        ["2", "Identitas Branding Sistem", "Logo dan Favicon resmi SatuNaker dengan tipografi tegas dan simbol grafis berbasis gradien Teal yang merepresentasikan keterbukaan data dinas."],
        ["3", "Palet Warna Utama Kedinasan", "Tema warna dinas terdiri dari Dinperinnaker Teal (#0d6b63, #2a92a2) sebagai warna aksen primer, Biru Navy (#25396e) untuk teks, dan Slate (#0f172a, #1e293b) untuk mode gelap."],
        ["4", "Indikator Status (Badges)", "Skema warna semantik: Emerald-500 (#10b981) untuk status Aktif, Amber-500 (#f59e0b) untuk Arsip, dan Rose-500 (#f43f5e) untuk status Tidak Aktif."],
        ["5", "Standar Tipografi", "Font sans-serif modern Inter dan Plus Jakarta Sans yang dioptimalkan untuk keterbacaan tinggi pada tampilan tabel numerik dan dashboard eksekutif."],
        ["6", "Aset Diagram Teknis", "Diagram alir Waterfall, Use Case Diagram, Activity Diagram Login, Activity Diagram Tambah Data, dan Entity Relationship Diagram (ERD)."],
        ["7", "Format Kop Dokumen Resmi", "Standardisasi Kop Surat Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga lengkap dengan garis ganda pemisah dan format pengesahan Kepala Dinas."]
    ]
    t5 = create_table_data(doc, av_headers, av_data, av_widths, av_aligns)
    
    target_p._p.addprevious(p_h5._p)
    target_p._p.addprevious(p_b5._p)
    target_p._p.addprevious(p_c5._p)
    target_p._p.addprevious(t5._tbl)

    # 6. Update RBAC Heading & Caption to Tabel 3.6
    target_p.text = "f. Matriks Kebutuhan Hak Akses Pengguna (RBAC)"
    target_p.runs[0].font.name = "Times New Roman"
    target_p.runs[0].font.size = Pt(12)
    target_p.runs[0].font.bold = True
    
    for p in doc.paragraphs:
        if "Tabel 3.3 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)" in p.text:
            p.text = "Tabel 3.6 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
            break

    # 7. Renumber Database Kamus Data Tables
    # In paragraph text: "Kamus data spesifikasi kolom untuk masing-masing tabel relasional disajikan pada Tabel 3.4 sampai dengan Tabel 3.7."
    # -> "disajikan pada Tabel 3.7 sampai dengan Tabel 3.10."
    for p in doc.paragraphs:
        if "disajikan pada Tabel 3.4 sampai dengan Tabel 3.7" in p.text:
            p.text = p.text.replace("Tabel 3.4 sampai dengan Tabel 3.7", "Tabel 3.7 sampai dengan Tabel 3.10")
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)
        elif "Tabel 3.4 Spesifikasi Struktur Tabel Basis Data unit_kerja" in p.text:
            p.text = "Tabel 3.7 Spesifikasi Struktur Tabel Basis Data unit_kerja"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
        elif "Tabel 3.5 Spesifikasi Struktur Tabel Basis Data profiles" in p.text:
            p.text = "Tabel 3.8 Spesifikasi Struktur Tabel Basis Data profiles"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
        elif "Tabel 3.6 Spesifikasi Struktur Tabel Basis Data data_records" in p.text:
            p.text = "Tabel 3.9 Spesifikasi Struktur Tabel Basis Data data_records"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
        elif "Tabel 3.7 Spesifikasi Struktur Tabel Basis Data log_aktivitas" in p.text:
            p.text = "Tabel 3.10 Spesifikasi Struktur Tabel Basis Data log_aktivitas"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True

    # 8. Renumber Testing Tables (Tabel 3.8 to 3.20 -> Tabel 3.11 to 3.23)
    # Intro paragraph:
    for p in doc.paragraphs:
        if "Rincian hasil pengujian disajikan pada Tabel 3.8 sampai dengan Tabel 3.20" in p.text:
            p.text = p.text.replace("Tabel 3.8 sampai dengan Tabel 3.20", "Tabel 3.11 sampai dengan Tabel 3.23")
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)
            
    renumber_map = [
        ("Tabel 3.8 Pengujian Autentikasi Pengguna (Login & Logout)", "Tabel 3.11 Pengujian Autentikasi Pengguna (Login & Logout)"),
        ("Tabel 3.9 Pengujian Dashboard Eksekutif & Pemantauan Data", "Tabel 3.12 Pengujian Dashboard Eksekutif & Pemantauan Data"),
        ("Tabel 3.10 Pengujian Tambah Data Sektoral oleh Admin Bidang", "Tabel 3.13 Pengujian Tambah Data Sektoral oleh Admin Bidang"),
        ("Tabel 3.11 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja", "Tabel 3.14 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja"),
        ("Tabel 3.12 Pengujian Akses Tautan Data Dukung Google Drive", "Tabel 3.15 Pengujian Akses Tautan Data Dukung Google Drive"),
        ("Tabel 3.13 Pengujian Ubah dan Hapus Data Sektoral", "Tabel 3.16 Pengujian Ubah dan Hapus Data Sektoral"),
        ("Tabel 3.14 Pengujian Pencarian dan Penyaringan Data (Filter)", "Tabel 3.17 Pengujian Pencarian dan Penyaringan Data (Filter)"),
        ("Tabel 3.15 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)", "Tabel 3.18 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)"),
        ("Tabel 3.16 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga", "Tabel 3.19 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga"),
        ("Tabel 3.17 Pengujian Manajemen Master Unit Kerja (Super Admin)", "Tabel 3.20 Pengujian Manajemen Master Unit Kerja (Super Admin)"),
        ("Tabel 3.18 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)", "Tabel 3.21 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)"),
        ("Tabel 3.19 Pengujian Backup & Restore Basis Data (Super Admin)", "Tabel 3.23 Pengujian Backup & Restore Basis Data (Super Admin)"),
        ("Tabel 3.20 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)", "Tabel 3.22 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)"),
        ("Tabel 3.21 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa", "Tabel 3.24 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa")
    ]
    for old_cap, new_cap in renumber_map:
        for p in doc.paragraphs:
            if old_cap in p.text:
                p.text = new_cap
                p.runs[0].font.name = "Times New Roman"
                p.runs[0].font.size = Pt(11)
                p.runs[0].font.bold = True
                print(f"Renumbered caption: {new_cap[:50]}")
                break

    # Paragraph text in Kendala:
    for p in doc.paragraphs:
        if "disajikan pada Tabel 3.21." in p.text:
            p.text = p.text.replace("disajikan pada Tabel 3.21.", "disajikan pada Tabel 3.24.")
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)

    # 9. Update DAFTAR TABEL section
    print("Updating DAFTAR TABEL...")
    p_dft_start = None
    p_dft_end = None
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip() == "DAFTAR TABEL":
            p_dft_start = idx
        elif p.text.strip() == "DAFTAR GAMBAR":
            p_dft_end = idx
            break

    # Remove all paragraphs between DAFTAR TABEL heading and DAFTAR GAMBAR heading
    paras_to_del_dft = doc.paragraphs[p_dft_start + 1:p_dft_end]
    for p in paras_to_del_dft:
        p._element.getparent().remove(p._element)

    target_dg = doc.paragraphs[p_dft_end]
    
    # 24 tables list for DAFTAR TABEL
    daftar_tabel_items = [
        ("Tabel 1.1 Matriks Jadwal Rencana dan Realisasi Kerja Praktik", "6"),
        ("Tabel 2.1 Informasi Lokasi dan Kontak Resmi DINPERINNAKER Kabupaten Purbalingga", "12"),
        ("Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)", "15"),
        ("Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)", "15"),
        ("Tabel 3.3 Spesifikasi Teknologi Website (Web Technology Stack)", "16"),
        ("Tabel 3.4 Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)", "17"),
        ("Tabel 3.5 Katalog Aset Visual dan Desain Antarmuka", "18"),
        ("Tabel 3.6 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)", "19"),
        ("Tabel 3.7 Spesifikasi Struktur Tabel Basis Data unit_kerja", "20"),
        ("Tabel 3.8 Spesifikasi Struktur Tabel Basis Data profiles", "20"),
        ("Tabel 3.9 Spesifikasi Struktur Tabel Basis Data data_records", "21"),
        ("Tabel 3.10 Spesifikasi Struktur Tabel Basis Data log_aktivitas", "21"),
        ("Tabel 3.11 Pengujian Autentikasi Pengguna (Login & Logout)", "33"),
        ("Tabel 3.12 Pengujian Dashboard Eksekutif & Pemantauan Data", "33"),
        ("Tabel 3.13 Pengujian Tambah Data Sektoral oleh Admin Bidang", "33"),
        ("Tabel 3.14 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja", "34"),
        ("Tabel 3.15 Pengujian Akses Tautan Data Dukung Google Drive", "34"),
        ("Tabel 3.16 Pengujian Ubah dan Hapus Data Sektoral", "34"),
        ("Tabel 3.17 Pengujian Pencarian dan Penyaringan Data (Filter)", "35"),
        ("Tabel 3.18 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)", "35"),
        ("Tabel 3.19 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga", "35"),
        ("Tabel 3.20 Pengujian Manajemen Master Unit Kerja (Super Admin)", "36"),
        ("Tabel 3.21 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)", "36"),
        ("Tabel 3.22 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)", "36"),
        ("Tabel 3.23 Pengujian Backup & Restore Basis Data (Super Admin)", "37"),
        ("Tabel 3.24 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa", "38")
    ]

    for title, page_no in daftar_tabel_items:
        p_item = doc.add_paragraph()
        p_item.style = 'toc 1'
        p_item.paragraph_format.space_before = Pt(2)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.0
        run_title = p_item.add_run(f"{title}\t{page_no}")
        run_title.font.name = "Times New Roman"
        run_title.font.size = Pt(11)
        target_dg._p.addprevious(p_item._p)

    # 10. Apply standard academic borders (3 horizontal borders, 0 vertical) to ALL tables in document
    print("Applying academic open-border style to all tables...")
    for t in doc.tables:
        set_academic_table_borders(t)

    doc.save(DOC_PATH)
    print("Phase 2 update completed and saved successfully!")

if __name__ == "__main__":
    main()
