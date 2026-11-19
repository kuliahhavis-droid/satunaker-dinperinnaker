# -*- coding: utf-8 -*-
"""
Full updater script for BAB I across Bank Materi, Master Docx, and Template Docx.
"""
import os
import re
import shutil
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{top.get("val", "none") if top else "none"}" w:sz="{top.get("sz", "0") if top else "0"}" w:space="0" w:color="{top.get("color", "auto") if top else "auto"}"/>
            <w:left w:val="{left.get("val", "none") if left else "none"}" w:sz="{left.get("sz", "0") if left else "0"}" w:space="0" w:color="{left.get("color", "auto") if left else "auto"}"/>
            <w:bottom w:val="{bottom.get("val", "none") if bottom else "none"}" w:sz="{bottom.get("sz", "0") if bottom else "0"}" w:space="0" w:color="{bottom.get("color", "auto") if bottom else "auto"}"/>
            <w:right w:val="{right.get("val", "none") if right else "none"}" w:sz="{right.get("sz", "0") if right else "0"}" w:space="0" w:color="{right.get("color", "auto") if right else "auto"}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def set_paragraph_runs(p, text, bold_prefix="", indent=0.5, line_spacing=2.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.text = "" # clear runs
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    if indent > 0:
        p.paragraph_format.first_line_indent = Inches(indent)
    else:
        p.paragraph_format.first_line_indent = Inches(0)
        
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
        
    tokens = re.split(r'(\*[^*]+\*)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('*') and tok.endswith('*'):
            r = p.add_run(tok[1:-1])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.italic = True
        else:
            r = p.add_run(tok)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.italic = False

def update_master_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    print("Updating Master Docx:", path)
    doc = docx.Document(path)
    
    # 1. Update Abstract paragraph (P137)
    p137 = doc.paragraphs[137]
    abstrak_text = (
        "Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga menaungi 7 (tujuh) unit kerja strategis penghasil "
        "data statistik sektoral, yaitu Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja, Bidang Pelatihan dan Penempatan "
        "Tenaga Kerja, Bidang Industri, Subbagian Perencanaan dan Keuangan, Subbagian Umum dan Kepegawaian, UPTD Balai Latihan Kerja, "
        "serta UPTD Pengembangan Industri Logam. Pengelolaan data sebelumnya terfragmentasi (*data silo*) pada berkas lembar sebar mandiri "
        "dan arsip fisik belum terindeks terpusat, sehingga pimpinan mengalami keterlambatan dalam memantau kinerja secara holistik dan "
        "rekapitulasi tahunan membutuhkan koordinasi berhari-hari. Proyek Kerja Praktik ini bertujuan merancang dan membangun Website "
        "Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker) sebagai portal integrasi data sektoral terpusat (*Single Source of Truth*). "
        "Sistem dikembangkan menggunakan metode *System Development Life Cycle* (SDLC) model *Waterfall*, memanfaatkan teknologi modern "
        "berbasis *Next.js 16 (App Router)*, *TypeScript*, *Tailwind CSS v4*, dan basis data awan *PostgreSQL Supabase*. Fitur utama mencakup "
        "*Role-Based Access Control* (RBAC) multi-peran dengan proteksi *auto-lock* unit kerja bagi admin operator, integrasi tautan Google Drive "
        "untuk penelusuran bukti fisik digital tanpa membebani penyimpanan server, dasbor eksekutif interaktif dengan filter tahun dinamis, "
        "modul ekspor spreadsheet Microsoft Excel (.xlsx), modul pencadangan mandiri (*backup snapshot* JSON), serta mesin cetak dokumen "
        "ber-kop resmi Pemerintah Kabupaten Purbalingga. Pengujian fungsionalitas sistem menggunakan metode *Black-Box Testing* pada 13 tabel "
        "kasus uji dengan 22 butir skenario menghasilkan tingkat keberhasilan 100% valid, memangkas waktu rekapitulasi laporan sektoral dari "
        "3–5 hari kerja menjadi kurang dari lima detik, serta mendukung penerapan prinsip Satu Data Indonesia di tingkat daerah."
    )
    set_paragraph_runs(p137, abstrak_text, indent=0.5, line_spacing=1.0)
    
    # 2. Update BAB I Deskripsi Proyek paragraphs
    p142 = doc.paragraphs[142]
    t142 = (
        "Dalam era transformasi digital kepemerintahan menuju penerapan *Electronic Government* (*E-Government*) yang terintegrasi, "
        "ketersediaan data statistik sektoral yang valid, akurat, mutakhir, dan mudah diakses merupakan fondasi esensial bagi perumusan "
        "kebijakan publik yang tepat sasaran. Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga sebagai unsur "
        "pelaksana urusan pemerintahan daerah di bidang perindustrian dan transmigrasi tenaga kerja menaungi 7 (tujuh) unit kerja "
        "operasional yang setiap periodenya memproduksi ratusan rekaman data strategis. Unit kerja tersebut meliputi Bidang Hubungan "
        "Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK), Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK), Bidang Industri, "
        "Subbagian Perencanaan dan Keuangan (Renkeu), Subbagian Umum dan Kepegawaian (Umpeg), UPTD Balai Latihan Kerja (BLK), "
        "serta UPTD Pengembangan Industri Logam (PILOG)."
    )
    set_paragraph_runs(p142, t142, indent=0.5, line_spacing=2.0)
    
    p143 = doc.paragraphs[143]
    t143 = (
        "Berdasarkan observasi lapangan dan wawancara mendalam yang dilakukan selama pelaksanaan Kerja Praktik, pengelolaan data di "
        "lingkungan DINPERINNAKER Kabupaten Purbalingga masih menghadapi hambatan struktural yang signifikan. Setiap bidang mengelola "
        "data operasionalnya secara mandiri menggunakan berkas lembar sebar (*spreadsheet*) lokal seperti Microsoft Excel tanpa standardisasi "
        "struktur kolom yang seragam. Kondisi ini menciptakan fenomena pulau-pulau data (*data silo*) di mana pertukaran informasi "
        "antar-bidang sangat terhambat (Hidayat & Rahmawati, 2022). Ketika pimpinan dinas atau instansi vertikal seperti Badan Pusat "
        "Statistik (BPS Kabupaten Purbalingga, 2024) dan Bappelitbangda memerlukan laporan rekapitulasi tahunan atau evaluasi Laporan "
        "Kinerja Instansi Pemerintah (LKjIP), staf dinas harus melakukan kompilasi manual berulang kali yang memakan waktu hingga "
        "berhari-hari kerja dan memiliki kerentanan tinggi terhadap kesalahan pengetikan ganda (*human error*)."
    )
    set_paragraph_runs(p143, t143, indent=0.5, line_spacing=2.0)
    
    p144 = doc.paragraphs[144]
    t144 = (
        "Selain permasalahan pada data numerik tabular, kendala mendasar lainnya terletak pada verifikasi berkas bukti fisik data "
        "dukung operasional. Dokumen penting seperti berkas Perjanjian Kerja Bersama (PKB), risalah mediasi perselisihan ketenagakerjaan, "
        "dokumen penempatan pencari kerja (kartu AK-1), sertifikat kelulusan pelatihan vokasi BLK, hingga dokumen uji emisi knalpot PILOG "
        "seringkali masih diarsipkan dalam bentuk fisik di lemari berkas masing-masing seksi. Akibatnya, proses validasi keabsahan data "
        "membutuhkan pencarian dokumen fisik secara konvensional yang tidak efisien dan rentan terhadap risiko kerusakan fisik maupun "
        "kehilangan dokumen historis."
    )
    set_paragraph_runs(p144, t144, indent=0.5, line_spacing=2.0)
    
    p145 = doc.paragraphs[145]
    t145 = (
        "Menjawab permasalahan tersebut, proyek Kerja Praktik ini difokuskan pada perancangan dan pembangunan sistem portal data "
        "terpadu berbasis web modern yang diberi nama Website Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker). Sistem SatuNaker "
        "dirancang sebagai simpul sentral (*Single Source of Truth*) yang menyatukan seluruh aliran pencatatan data sektoral dari 7 unit "
        "kerja ke dalam satu basis data terpusat. Dengan arsitektur berbasis web modern, sistem ini memungkinkan staf admin bidang melakukan "
        "input data secara terstruktur, pimpinan dinas memantau indikator kinerja melalui dasbor eksekutif secara waktu-nyata (*real-time*), "
        "penelusuran bukti fisik terintegrasi melalui tautan penyimpanan awan Google Drive dinas, serta laporan resmi dinas dapat dicetak "
        "seketika lengkap dengan kop resmi Pemerintah Kabupaten Purbalingga selaras dengan amanat Peraturan Presiden Nomor 39 Tahun 2019 "
        "tentang Satu Data Indonesia (Republik Indonesia, 2019)."
    )
    set_paragraph_runs(p145, t145, indent=0.5, line_spacing=2.0)
    
    # 3. Update Subbab B Ruang Lingkup
    p147 = doc.paragraphs[147]
    t147 = (
        "Guna memastikan proses perancangan dan pembangunan sistem perangkat lunak berjalan terarah, terukur, dan selesai tepat waktu "
        "dalam batasan durasi 33 hari kerja aktif (1 Oktober 2026 sampai dengan 13 November 2026), ruang lingkup dan batasan sistem "
        "SatuNaker didefinisikan sebagai berikut:"
    )
    set_paragraph_runs(p147, t147, indent=0.5, line_spacing=2.0)
    
    # 4. Update Subbab C Tahapan Pelaksanaan
    p156 = doc.paragraphs[156]
    t156 = (
        "Metodologi pengembangan perangkat lunak yang diterapkan dalam rekayasa sistem SatuNaker adalah metode *System Development Life "
        "Cycle* (SDLC) model sekuensial linier atau yang umum dikenal dengan istilah *Waterfall Model* (Pressman & Maxim, 2020). Pendekatan "
        "klasik ini dipilih karena kebutuhan fungsional sistem tata kelola data sektoral di instansi pemerintah telah terdefinisi secara "
        "terstruktur dan stabil berdasarkan regulasi serta format formulir baku dinas yang berlaku (Saputra & Handayani, 2023). "
        "Tahapan metodologi *Waterfall* yang dilalui digambarkan pada Gambar 1.1."
    )
    set_paragraph_runs(p156, t156, indent=0.5, line_spacing=2.0)
    
    # 5. Update 5 Waterfall Steps
    steps = [
        ("1. Perencanaan (*Planning*): ", "Mendefinisikan sasaran proyek, mengkaji permasalahan fragmentasi data dinas, dan menetapkan jadwal kerja praktik."),
        ("2. Analisis Kebutuhan (*Requirement Analysis*): ", "Mengumpulkan data kebutuhan fungsional dan non-fungsional melalui wawancara dan telaah dokumen."),
        ("3. Perancangan Sistem (*System Design*): ", "Memodelkan relasi basis data (ERD), diagram perilaku sistem (UML *Use Case* dan *Activity Diagram*), serta antarmuka visual."),
        ("4. Implementasi (*Implementation*): ", "Mengembangkan kode program sistem web SatuNaker menggunakan teknologi Next.js 16 (*App Router*), TypeScript, Tailwind CSS v4, dan PostgreSQL Supabase."),
        ("5. Pengujian (*Testing*): ", "Menguji seluruh fungsionalitas sistem secara menyeluruh menggunakan metode *Black-Box Testing* pada 13 tabel guna memastikan keandalan sistem.")
    ]
    for idx, (pre, body) in enumerate(steps):
        p_step = doc.paragraphs[160 + idx]
        set_paragraph_runs(p_step, body, bold_prefix=pre, indent=0.5, line_spacing=2.0)
        
    # 6. Update Subbab D Jadwal Pelaksanaan
    p166 = doc.paragraphs[166]
    t166 = (
        "Kegiatan Kerja Praktik dilaksanakan selama 33 hari kerja aktif terhitung sejak tanggal 1 Oktober 2026 sampai dengan "
        "tanggal 13 November 2026 bertempat di Kantor DINPERINNAKER Kabupaten Purbalingga. Matriks pelaksanaan tahapan proyek disajikan "
        "pada Tabel 1.1."
    )
    set_paragraph_runs(p166, t166, indent=0.5, line_spacing=2.0)
    
    # 7. Update Table 5 (Tabel 1.1) in Master Docx
    t1_1 = doc.tables[5]
    print("Found Tabel 1.1:", len(t1_1.rows), "x", len(t1_1.columns))
    
    # Set headers
    headers = ['No.', 'Tahapan Aktivitas Proyek', 'Minggu 1-2', 'Minggu 3-4', 'Minggu 5-6', 'Status']
    for col_idx, h_text in enumerate(headers):
        cell = t1_1.cell(0, col_idx)
        cell.text = h_text
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.bold = True
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        set_cell_borders(cell, 
                         top={'val': 'single', 'sz': '8', 'color': '000000'},
                         bottom={'val': 'single', 'sz': '6', 'color': '000000'})
        
    # Set row data with clean checkmarks
    row_data = [
        ['1', 'Observasi, Wawancara, & Analisis Masalah', '✓', '', '', 'Selesai'],
        ['2', 'Spesifikasi Kebutuhan & Desain UML/ERD', '✓', '✓', '', 'Selesai'],
        ['3', 'Pengodean Front-End & Integrasi Supabase', '', '✓', '✓', 'Selesai'],
        ['4', 'Pengujian Sistem (Black-Box Testing)', '', '', '✓', 'Selesai'],
        ['5', 'Penyusunan Laporan & Serah Terima Sistem', '', '', '✓', 'Selesai']
    ]
    
    for row_idx, data in enumerate(row_data, start=1):
        is_last = (row_idx == len(row_data))
        for col_idx, val in enumerate(data):
            cell = t1_1.cell(row_idx, col_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Inches(0)
            if col_idx in [0, 2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.5)
            set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
            if is_last:
                set_cell_borders(cell, bottom={'val': 'single', 'sz': '8', 'color': '000000'})
            else:
                set_cell_borders(cell)
                
    doc.save(path)
    print("Master Docx updated and saved successfully!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

def update_template_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\TEMPLATE_LAPORAN_KP_TI_UMP.docx'
    print("Updating Template Docx:", path)
    doc = docx.Document(path)
    
    t = doc.tables[2]
    headers = ['No.', 'Tahapan Aktivitas Proyek', 'Minggu 1-2', 'Minggu 3-4', 'Minggu 5-6', 'Status']
    row_data = [
        ['1', 'Observasi, Wawancara, & Analisis Masalah', '✓', '', '', 'Selesai'],
        ['2', 'Spesifikasi Kebutuhan & Desain UML/ERD', '✓', '✓', '', 'Selesai'],
        ['3', 'Pengodean Front-End & Integrasi Supabase', '', '✓', '✓', 'Selesai'],
        ['4', 'Pengujian Sistem (Black-Box Testing)', '', '', '✓', 'Selesai'],
        ['5', 'Penyusunan Laporan & Serah Terima Sistem', '', '', '✓', 'Selesai']
    ]
    
    while len(t.columns) < 6:
        t.add_column(Inches(1.0))
        
    while len(t.rows) > 6:
        tr = t.rows[-1]._tr
        t._tbl.remove(tr)
        
    for col_idx, h_text in enumerate(headers):
        cell = t.cell(0, col_idx)
        cell.text = h_text
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.bold = True
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        set_cell_borders(cell, 
                         top={'val': 'single', 'sz': '8', 'color': '000000'},
                         bottom={'val': 'single', 'sz': '6', 'color': '000000'})
        
    for row_idx, data in enumerate(row_data, start=1):
        is_last = (row_idx == len(row_data))
        for col_idx, val in enumerate(data):
            cell = t.cell(row_idx, col_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Inches(0)
            if col_idx in [0, 2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.5)
            set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
            if is_last:
                set_cell_borders(cell, bottom={'val': 'single', 'sz': '8', 'color': '000000'})
            else:
                set_cell_borders(cell)
                
    doc.save(path)
    print("Template Docx updated and saved successfully!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\TEMPLATE_LAPORAN_KP_TI_UMP.docx'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

def update_bank_materi_md():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    print("Updating Bank Materi MD:", path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace("durasi 40 hari kerja", "durasi 33 hari kerja aktif (1 Oktober 2026 sampai dengan 13 November 2026)")
    content = content.replace("15 September 2026 sampai dengan tanggal 31 Oktober 2026", "1 Oktober 2026 sampai dengan tanggal 13 November 2026")
    content = content.replace("selama 40 hari kerja aktif", "selama 33 hari kerja aktif")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Bank Materi MD saved!")
    
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

if __name__ == '__main__':
    update_master_docx()
    update_template_docx()
    update_bank_materi_md()
    print("ALL UPDATES COMPLETED SUCCESSFULLY!")
