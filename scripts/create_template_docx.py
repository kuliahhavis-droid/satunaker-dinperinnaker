import os
import shutil
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\TEMPLATE_LAPORAN_KP_TI_UMP.docx"
ARTIFACT_PATH = r"C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\TEMPLATE_LAPORAN_KP_TI_UMP.docx"
LOGO_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\satudata-nextjs\public\images\logo-ump.png"

def set_page_margins(section):
    section.top_margin = Cm(4.0)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(4.0)
    section.right_margin = Cm(3.0)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)

def set_academic_table_borders(table):
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
    tblBorders = OxmlElement('w:tblBorders')
    
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '8')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), '000000')
    tblBorders.append(top)
    
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
    
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for child in list(tcPr):
                if child.tag.endswith('tcBorders'):
                    tcPr.remove(child)
            tcBorders = OxmlElement('w:tcBorders')
            b = OxmlElement('w:bottom')
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '6')
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), '000000')
            tcBorders.append(b)
            for side in ['top', 'left', 'right']:
                nb = OxmlElement(f'w:{side}')
                nb.set(qn('w:val'), 'none')
                tcBorders.append(nb)
            tcPr.append(tcBorders)

def format_cell(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=Pt(10), color=None):
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
    if color:
        run.font.color.rgb = color
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def add_academic_table(doc, headers, data, col_widths, col_aligns):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for col_idx, h in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        cell.width = col_widths[col_idx]
        format_cell(cell, h, bold=True, align=col_aligns[col_idx], font_size=Pt(10))
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            is_num_col = (col_idx == 0)
            align = col_aligns[col_idx]
            format_cell(cell, str(val), bold=is_num_col, align=align, font_size=Pt(10))
    set_academic_table_borders(table)
    return table

def add_para(doc, text="", style='Normal', bold=False, italic=False, size=Pt(12), align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=Pt(0), space_after=Pt(6), line_spacing=2.0, first_line_indent=Cm(1.0), color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = space_before
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = line_spacing
    if first_line_indent:
        p.paragraph_format.first_line_indent = first_line_indent
    if text:
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = size
        run.font.bold = bold
        run.font.italic = italic
        if color:
            run.font.color.rgb = color
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 2.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 2.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    return p

def add_caption_table(doc, text):
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

def add_caption_figure(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    return p

def add_guidance_box(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    run = p.add_run(f"👉 [Petunjuk Pengisian]: {text}")
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(90, 90, 90)
    return p

def add_image_placeholder(doc, caption_text):
    p_box = doc.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(6)
    p_box.paragraph_format.space_after = Pt(4)
    p_box.paragraph_format.line_spacing = 1.0
    r = p_box.add_run("[ TEMPAT MENYISIPKAN GAMBAR / TANGKAPAN LAYAR DI SINI ]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(120, 120, 120)
    add_caption_figure(doc, caption_text)

def main():
    print("Creating clean Template Docx...")
    doc = docx.Document()
    set_page_margins(doc.sections[0])
    
    # ----------------------------------------------------
    # COVER / HALAMAN JUDUL
    # ----------------------------------------------------
    p_cov_1 = add_para(doc, "LAPORAN KERJA PRAKTIK", bold=True, size=Pt(14), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(14), line_spacing=1.5, first_line_indent=None)
    p_cov_2 = add_para(doc, "RANCANG BANGUN WEBSITE SATU DATA DINAS PERINDUSTRIAN DAN TENAGA KERJA KABUPATEN PURBALINGGA\n(SATUNAKER)", bold=True, size=Pt(14), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(20), line_spacing=1.5, first_line_indent=None)
    
    p_cov_3 = add_para(doc, "Disusun sebagai Salah Satu Syarat\nKelengkapan Kurikulum pada Prodi Teknik Informatika\nFakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(24), line_spacing=1.5, first_line_indent=None)
    
    # Embed Logo UMP
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(24)
        run_logo = p_logo.add_run()
        run_logo.add_picture(LOGO_PATH, width=Cm(5.5))
        
    p_cov_4 = add_para(doc, "Disusun oleh:\n\nNama : Havisda Mei Khairil\nNIM : 2303040113", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(10), space_after=Pt(36), line_spacing=1.5, first_line_indent=None)
    
    p_cov_5 = add_para(doc, "PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS TEKNIK DAN SAINS\nUNIVERSITAS MUHAMMADIYAH PURWOKERTO\nNOVEMBER, 2026", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(20), space_after=Pt(0), line_spacing=1.5, first_line_indent=None)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # LEMBAR PERSETUJUAN (HALAMAN ii)
    # ----------------------------------------------------
    add_heading_1(doc, "LEMBAR PERSETUJUAN LAPORAN\nKERJA PRAKTIK")
    add_para(doc, "RANCANG BANGUN WEBSITE SATU DATA DINAS PERINDUSTRIAN DAN TENAGA KERJA KABUPATEN PURBALINGGA (SATUNAKER)", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(10), space_after=Pt(16), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Disusun Oleh:\nNama : Havisda Mei Khairil\nNIM : 2303040113", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(20), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Laporan Kerja Praktik Mahasiswa tersebut di Atas Dinyatakan Telah Memenuhi Syarat untuk Diseminarkan", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(10), space_after=Pt(20), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Disetujui : di Purwokerto\nTanggal : [Tanggal Persetujuan, contoh: 2 November 2026]", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(10), space_after=Pt(20), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Oleh :", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(10), line_spacing=1.5, first_line_indent=None)
    
    # Signature table for Persetujuan
    t_persetujuan = doc.add_table(rows=2, cols=2)
    t_persetujuan.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t_persetujuan.rows[0].cells[0], "Pembimbing Kerja Praktik,", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(11))
    format_cell(t_persetujuan.rows[0].cells[1], "Pembimbing Lapangan / Mitra,", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(11))
    
    c_p1 = t_persetujuan.rows[1].cells[0]
    c_p1.text = ""
    p_p1 = c_p1.paragraphs[0]
    p_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_p1.paragraph_format.space_before = Pt(50)
    r_p1 = p_p1.add_run("Elindra Ambar Pambudi, S.T., M.Kom.\nNIK. 2160766")
    r_p1.font.name = "Times New Roman"
    r_p1.font.size = Pt(11)
    r_p1.font.bold = True
    
    c_p2 = t_persetujuan.rows[1].cells[1]
    c_p2.text = ""
    p_p2 = c_p2.paragraphs[0]
    p_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_p2.paragraph_format.space_before = Pt(50)
    r_p2 = p_p2.add_run("Johan Arifin, S.Sos., M.Si.\nNIP. 19730514 199303 1 002")
    r_p2.font.name = "Times New Roman"
    r_p2.font.size = Pt(11)
    r_p2.font.bold = True
    
    set_academic_table_borders(t_persetujuan)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # HALAMAN PENGESAHAN (HALAMAN iii)
    # ----------------------------------------------------
    add_heading_1(doc, "HALAMAN PENGESAHAN")
    add_para(doc, "RANCANG BANGUN WEBSITE SATU DATA DINAS PERINDUSTRIAN DAN TENAGA KERJA KABUPATEN PURBALINGGA\n(SATUNAKER)", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(6), space_after=Pt(14), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Telah Diseminarkan dan Dipertahankan\ndalam Seminar Kerja Praktik Program Studi Teknik Informatika\nUniversitas Muhammadiyah Purwokerto", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(6), space_after=Pt(16), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Pada:\nHari : [Hari Seminar, contoh: Senin]\nTanggal : [Tanggal Seminar, contoh: 11 November 2026]", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(16), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Disetujui :\nDi : Purwokerto\nTanggal : [Tanggal Pengesahan, contoh: 11 November 2026]", size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(16), line_spacing=1.5, first_line_indent=None)
    
    add_para(doc, "Oleh:", bold=True, size=Pt(12), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(0), space_after=Pt(8), line_spacing=1.5, first_line_indent=None)
    
    # Signatures Table (Pembimbing & Penguji)
    t_pengesahan = doc.add_table(rows=3, cols=2)
    t_pengesahan.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t_pengesahan.rows[0].cells[0], "Pembimbing,", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(11))
    format_cell(t_pengesahan.rows[0].cells[1], "Penguji,", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(11))
    
    c_s1 = t_pengesahan.rows[1].cells[0]
    p_s1 = c_s1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s1.paragraph_format.space_before = Pt(45)
    r_s1 = p_s1.add_run("Elindra Ambar Pambudi, S.T., M.Kom.\nNIK. 2160766")
    r_s1.font.name = "Times New Roman"
    r_s1.font.size = Pt(11)
    r_s1.font.bold = True
    
    c_s2 = t_pengesahan.rows[1].cells[1]
    p_s2 = c_s2.paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s2.paragraph_format.space_before = Pt(45)
    r_s2 = p_s2.add_run("......................................................\nNIK. ........................")
    r_s2.font.name = "Times New Roman"
    r_s2.font.size = Pt(11)
    r_s2.font.bold = True
    
    # Row 2: Mengetahui Kaprodi
    cell_kaprodi_label = t_pengesahan.rows[2].cells[0]
    cell_kaprodi_label.merge(t_pengesahan.rows[2].cells[1])
    p_kp = cell_kaprodi_label.paragraphs[0]
    p_kp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kp.paragraph_format.space_before = Pt(16)
    r_kpl = p_kp.add_run("Mengetahui,\nKetua Program Studi Teknik Informatika\n\n\n\n\nAgung Purwo Wicaksono, S.T., M.Kom.\nNIK. 2160518")
    r_kpl.font.name = "Times New Roman"
    r_kpl.font.size = Pt(11)
    r_kpl.font.bold = True
    
    set_academic_table_borders(t_pengesahan)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # HALAMAN PERSEMBAHAN (HALAMAN iv)
    # ----------------------------------------------------
    add_heading_1(doc, "HALAMAN PERSEMBAHAN")
    add_para(doc, "Alhamdulillah puji syukur kepada Allah Subhanahu Wa Ta’ala, yang telah memberikan kesehatan, rahmat dan hidayah-Nya sehingga penulis diberikan kemudahan dan kelancaran untuk menyelesaikan kegiatan dan Laporan Kerja Praktik ini. Naskah laporan ini saya persembahkan dengan segenap kerendahan hati dan rasa hormat kepada:")
    
    persembahan_points = [
        "1. Allah Subhanahu Wa Ta’ala, atas segala nikmat iman, kesehatan, dan kelancaran yang senantiasa dilimpahkan dalam setiap langkah penulis.",
        "2. Kedua orang tua tercinta dan segenap keluarga besar yang senantiasa mendukung, memotivasi, dan mendoakan tanpa henti di setiap saat.",
        "3. Bapak Elindra Ambar Pambudi, S.T., M.Kom., selaku dosen pembimbing KP yang telah meluangkan waktu, memberikan arahan, serta bimbingan berharga bagi penulis.",
        "4. Bapak Agung Purwo Wicaksono, S.T., M.Kom., selaku Ketua Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto.",
        "5. Bapak Johan Arifin, S.Sos., M.Si., selaku Kepala Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga yang telah memberikan izin tempat dan fasilitas magang.",
        "6. Segenap pejabat struktural, pembimbing lapangan, dan staf pegawai di lingkungan DINPERINNAKER Kabupaten Purbalingga yang telah membantu dalam kelancaran kerja praktik.",
        "7. Rekan-rekan mahasiswa seperjuangan Teknik Informatika angkatan 2023 atas kebersamaan dan dukungannya.",
        "8. Serta semua pihak yang tidak dapat penulis sebutkan satu persatu yang telah membantu hingga terselesaikannya laporan ini."
    ]
    for pt_text in persembahan_points:
        add_para(doc, pt_text, space_before=Pt(2), space_after=Pt(4), line_spacing=1.5, first_line_indent=Cm(0.5))
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # KATA PENGANTAR (HALAMAN v)
    # ----------------------------------------------------
    add_heading_1(doc, "KATA PENGANTAR")
    add_para(doc, "Puji syukur atas kehadirat Allah Subhanahu Wa Ta’ala yang telah memberikan rahmat dan karunia-Nya, sehingga penyusun dapat menyelesaikan Laporan Kerja Praktik dengan judul \"Rancang Bangun Website Satu Data Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga (SatuNaker)\". Kerja Praktik ini merupakan salah satu persyaratan kurikulum untuk menyelesaikan pendidikan sarjana pada Program Studi Teknik Informatika Fakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto.")
    add_para(doc, "Pelaksanaan kerja praktik ini dimaksudkan agar mahasiswa memperoleh pengalaman, wawasan di dunia kerja nyata kepemerintahan daerah, sekaligus mengaplikasikan ilmu rekayasa perangkat lunak dalam memecahkan permasalahan pengelolaan data sektoral. Melalui kegiatan ini, mahasiswa dituntut untuk selalu belajar, berinovasi, dan meningkatkan kualitas kompetensi pribadi.")
    add_para(doc, "Laporan ini disusun dengan keterbukaan dan kesadaran bahwa masih terdapat kekurangan, baik dari segi bahasa maupun teknik penyajian. Oleh karena itu, dengan kerendahan hati penulis mengharapkan kritik dan saran yang konstruktif dari pembaca demi penyempurnaan di masa mendatang. Akhir kata, semoga laporan kerja praktik ini dapat memberikan manfaat nyata bagi instansi mitra serta pembaca sekalian.")
    
    add_para(doc, "Purwokerto, November 2026\n\n\n\nHavisda Mei Khairil\nNIM. 2303040113", align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=Pt(16), space_after=Pt(0), line_spacing=1.5, first_line_indent=None)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # DAFTAR ISI (HALAMAN vi)
    # ----------------------------------------------------
    add_heading_1(doc, "DAFTAR ISI")
    daftar_isi_entries = [
        ("HALAMAN JUDUL", "i"),
        ("LEMBAR PERSETUJUAN", "ii"),
        ("HALAMAN PENGESAHAN", "iii"),
        ("HALAMAN PERSEMBAHAN", "iv"),
        ("KATA PENGANTAR", "v"),
        ("DAFTAR ISI", "vi"),
        ("DAFTAR TABEL", "vii"),
        ("DAFTAR GAMBAR", "viii"),
        ("DAFTAR LAMPIRAN", "x"),
        ("ABSTRAK", "xi"),
        ("BAB I GAMBARAN UMUM PROYEK", "1"),
        ("A. Deskripsi Proyek", "1"),
        ("B. Ruang Lingkup Proyek", "2"),
        ("C. Tahapan Pelaksanaan Proyek", "4"),
        ("D. Jadwal Pelaksanaan", "10"),
        ("BAB II INSTANSI MITRA", "11"),
        ("A. Profil Instansi Mitra", "11"),
        ("B. Struktur Organisasi Mitra", "12"),
        ("C. Lokasi Mitra", "12"),
        ("D. Visi dan Misi", "13"),
        ("BAB III PELAKSANAAN PROYEK", "14"),
        ("A. Hasil Tahapan Pelaksanaan", "14"),
        ("1. Perencanaan (Planning)", "14"),
        ("2. Analisis Kebutuhan (Analysis)", "15"),
        ("3. Perancangan Sistem (Design)", "22"),
        ("4. Pengembangan Sistem (Implementation)", "30"),
        ("5. Pengujian Sistem (Testing)", "42"),
        ("B. Kendala Pelaksanaan", "50"),
        ("BAB IV PENUTUP", "52"),
        ("A. Kesimpulan", "52"),
        ("B. Saran", "52"),
        ("DAFTAR PUSTAKA", "54"),
        ("LAMPIRAN", "56")
    ]
    for title, pg in daftar_isi_entries:
        indent = Cm(0.5) if (title.startswith("A.") or title.startswith("B.") or title.startswith("C.") or title.startswith("D.") or title.startswith("1.") or title.startswith("2.") or title.startswith("3.") or title.startswith("4.") or title.startswith("5.")) else None
        bold = True if (title.startswith("BAB") or title.isupper()) else False
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(2)
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.15
        if indent:
            p_toc.paragraph_format.left_indent = indent
        r_toc = p_toc.add_run(f"{title}\t{pg}")
        r_toc.font.name = "Times New Roman"
        r_toc.font.size = Pt(11)
        r_toc.font.bold = bold
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # DAFTAR TABEL (HALAMAN vii)
    # ----------------------------------------------------
    add_heading_1(doc, "DAFTAR TABEL")
    daftar_tabel_entries = [
        ("Tabel 1.1 Jadwal Pelaksanaan Kerja Praktik", "10"),
        ("Tabel 2.1 Informasi Lokasi dan Kontak Resmi DINPERINNAKER Kabupaten Purbalingga", "12"),
        ("Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)", "16"),
        ("Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)", "17"),
        ("Tabel 3.3 Spesifikasi Teknologi Website (Web Technology Stack)", "18"),
        ("Tabel 3.4 Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)", "19"),
        ("Tabel 3.5 Katalog Aset Visual dan Desain Antarmuka", "20"),
        ("Tabel 3.6 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)", "21"),
        ("Tabel 3.7 Spesifikasi Struktur Tabel Basis Data unit_kerja", "26"),
        ("Tabel 3.8 Spesifikasi Struktur Tabel Basis Data profiles", "27"),
        ("Tabel 3.9 Spesifikasi Struktur Tabel Basis Data data_records", "28"),
        ("Tabel 3.10 Spesifikasi Struktur Tabel Basis Data log_aktivitas", "29"),
        ("Tabel 3.11 Pengujian Halaman Login", "43"),
        ("Tabel 3.12 Pengujian Halaman Dasbor Eksekutif", "43"),
        ("Tabel 3.13 Pengujian Halaman Kelola Data Sektoral", "44"),
        ("Tabel 3.14 Pengujian Validasi Pembatasan Hak Akses dan Auto-Lock Unit", "44"),
        ("Tabel 3.15 Pengujian Tautan Dokumen Pendukung Google Drive", "45"),
        ("Tabel 3.16 Pengujian Fitur Ubah dan Hapus Data Sektoral", "45"),
        ("Tabel 3.17 Pengujian Filter dan Pencarian Data Sektoral", "46"),
        ("Tabel 3.18 Pengujian Fitur Ekspor Data ke Microsoft Excel", "46"),
        ("Tabel 3.19 Pengujian Pratinjau Dokumen Cetak Ber-Kop Resmi", "47"),
        ("Tabel 3.20 Pengujian Halaman Manajemen Master Unit Kerja", "47"),
        ("Tabel 3.21 Pengujian Halaman Manajemen Akun Pengguna", "48"),
        ("Tabel 3.22 Pengujian Fitur Pencadangan (Backup) dan Pemulihan Basis Data", "48"),
        ("Tabel 3.23 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)", "49"),
        ("Tabel 3.24 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa", "51")
    ]
    for title, pg in daftar_tabel_entries:
        p_dt = doc.add_paragraph()
        p_dt.paragraph_format.space_before = Pt(2)
        p_dt.paragraph_format.space_after = Pt(2)
        p_dt.paragraph_format.line_spacing = 1.15
        r_dt = p_dt.add_run(f"{title}\t{pg}")
        r_dt.font.name = "Times New Roman"
        r_dt.font.size = Pt(11)
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # DAFTAR GAMBAR (HALAMAN viii)
    # ----------------------------------------------------
    add_heading_1(doc, "DAFTAR GAMBAR")
    daftar_gambar_entries = [
        ("Gambar 1.1 Tahapan Metode SDLC Pendekatan Waterfall", "5"),
        ("Gambar 1.2 Purwarupa Desain Antarmuka Login Admin", "7"),
        ("Gambar 1.3 Use Case Diagram Konseptual", "8"),
        ("Gambar 1.4 Activity Diagram Autentikasi Pengguna", "9"),
        ("Gambar 2.1 Bagan Struktur Organisasi DINPERINNAKER Kabupaten Purbalingga", "12"),
        ("Gambar 3.1 Use Case Diagram Sistem SatuNaker", "23"),
        ("Gambar 3.2 Activity Diagram Login Pengguna", "24"),
        ("Gambar 3.3 Activity Diagram Tambah Data Sektoral", "25"),
        ("Gambar 3.4 Relasi Antar Tabel (Entity Relationship Diagram - ERD)", "29"),
        ("Gambar 3.5 Desain Purwarupa Halaman Login", "30"),
        ("Gambar 3.6 Desain Purwarupa Dasbor Eksekutif", "31"),
        ("Gambar 3.7 Desain Purwarupa Kelola Data Sektoral", "31"),
        ("Gambar 3.8 Tampilan Halaman Login Sistem", "32"),
        ("Gambar 3.9 Tampilan Dasbor Eksekutif Kepala Dinas", "33"),
        ("Gambar 3.10 Tampilan Dasbor dengan Filter Tahun Aktif", "34"),
        ("Gambar 3.11 Tampilan Tabel Kelola Data Sektoral", "35"),
        ("Gambar 3.12 Tampilan Formulir Modal Tambah Data Sektoral", "36"),
        ("Gambar 3.13 Tampilan Pusat Laporan Eksekutif", "37"),
        ("Gambar 3.14 Tampilan Pratinjau Dokumen Cetak Ber-Kop Resmi", "38"),
        ("Gambar 3.15 Tampilan Manajemen Master Unit Kerja Dinas", "39"),
        ("Gambar 3.16 Tampilan Manajemen Akun Pengguna & Hak Akses", "40"),
        ("Gambar 3.17 Tampilan Pencadangan Mandiri (Backup) & Pemulihan Basis Data", "41")
    ]
    for title, pg in daftar_gambar_entries:
        p_dg = doc.add_paragraph()
        p_dg.paragraph_format.space_before = Pt(2)
        p_dg.paragraph_format.space_after = Pt(2)
        p_dg.paragraph_format.line_spacing = 1.15
        r_dg = p_dg.add_run(f"{title}\t{pg}")
        r_dg.font.name = "Times New Roman"
        r_dg.font.size = Pt(11)
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # DAFTAR LAMPIRAN (HALAMAN x)
    # ----------------------------------------------------
    add_heading_1(doc, "DAFTAR LAMPIRAN")
    lampiran_entries = [
        ("Lampiran 1 Surat Keterangan Telah Menyelesaikan Kerja Praktik dari Mitra", "56"),
        ("Lampiran 2 Formulir Daftar Hadir Peserta Seminar Kerja Praktik", "57"),
        ("Lampiran 3 Lembar Persetujuan Laporan Kerja Praktik", "58"),
        ("Lampiran 4 Bukti Dokumen Legalitas / SK Instansi Mitra DINPERINNAKER", "59"),
        ("Lampiran 5 Logbook Rekapitulasi Catatan Aktivitas Harian Magang Mahasiswa", "60")
    ]
    for title, pg in lampiran_entries:
        p_dl = doc.add_paragraph()
        p_dl.paragraph_format.space_before = Pt(2)
        p_dl.paragraph_format.space_after = Pt(2)
        p_dl.paragraph_format.line_spacing = 1.15
        r_dl = p_dl.add_run(f"{title}\t{pg}")
        r_dl.font.name = "Times New Roman"
        r_dl.font.size = Pt(11)
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # ABSTRAK (HALAMAN xi)
    # ----------------------------------------------------
    add_heading_1(doc, "ABSTRAK")
    add_guidance_box(doc, "Abstrak disusun dalam 1 paragraf padat (200–250 kata) dengan spasi 1.0 (tunggal). Memuat: (1) Latar belakang urgensi digitalisasi sistem data dinas, (2) Permasalahan nyata data sektoral di DINPERINNAKER, (3) Solusi pengembangan sistem SatuNaker, (4) Metode SDLC Waterfall, (5) Tumpukan teknologi yang dipakai (Next.js, TypeScript, Tailwind, Supabase), (6) Aktor pengguna dan fungsionalitas utama, serta (7) Dampak/manfaat nyata bagi akuntabilitas dinas.")
    
    add_para(doc, "[TULISKAN PARAGRAF ABSTRAK ANDA DI SINI. Contoh draft lengkap telah disediakan pada Bank Materi Pendukung].", italic=True, line_spacing=1.0, first_line_indent=Cm(1.0))
    
    add_para(doc, "Kata kunci: satu data, dinperinnaker purbalingga, website sektoral, next.js, supabase, waterfall", italic=True, line_spacing=1.0, first_line_indent=None, space_before=Pt(8))
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # BAB I GAMBARAN UMUM PROYEK (HALAMAN 1)
    # ----------------------------------------------------
    add_heading_1(doc, "BAB I\nGAMBARAN UMUM PROYEK")
    
    add_heading_2(doc, "A. Deskripsi Proyek")
    add_guidance_box(doc, "Uraikan 3–4 paragraf yang mencakup: (1) Peran penting teknologi informasi dan website di sektor pemerintahan modern, (2) Landasan hukum Perpres No. 39 Tahun 2019 tentang Satu Data Indonesia (SDI), (3) Kondisi faktual pengelolaan data di DINPERINNAKER Kabupaten Purbalingga yang menaungi 7 unit kerja (Sekretariat, HIJTK, PPTK, Perindustrian, BLK, PILOG) yang selama ini menghadapi kendala 'data silo' (Excel/laporan fisik terpisah), serta (4) Rumusan solusi sistem Website Satu Data (SatuNaker) sebagai Single Source of Truth.")
    add_para(doc, "[Tuliskan uraian latar belakang dan deskripsi proyek di sini...]")
    
    add_heading_2(doc, "B. Ruang Lingkup Proyek")
    add_guidance_box(doc, "Uraikan ruang lingkup teknis dan fungsional pengembangan sistem, mencakup: (1) Stack teknologi yang digunakan, (2) Hak akses pengguna (Super Admin, Admin Bidang/UPTD/Sekretariat, Kepala Dinas, Publik), (3) Fitur fungsional utama (CRUD data sektoral, filter multi-kategori, ekspor Excel otomatis, cetak kop surat resmi, audit log), serta (4) Batasan sistem (fokus data statistik sektoral dinas, tidak mencakup transaksi kasda atau perizinan OSS eksternal).")
    add_para(doc, "[Tuliskan rincian ruang lingkup dan batasan proyek di sini...]")
    
    add_heading_2(doc, "C. Tahapan Pelaksanaan Proyek")
    add_guidance_box(doc, "Jelaskan metode pengembangan SDLC Waterfall yang meliputi 5 tahapan linear: (1) Perencanaan, (2) Analisis, (3) Perancangan, (4) Pengembangan/Implementasi, dan (5) Pengujian. Sertakan diagram alur Waterfall (Gambar 1.1) beserta purwarupa desain awal dan diagram perilaku umum.")
    add_para(doc, "[Tuliskan penjelasan metode SDLC Waterfall di sini...]")
    add_image_placeholder(doc, "Gambar 1.1 Tahapan Metode SDLC Pendekatan Waterfall")
    
    add_heading_2(doc, "D. Jadwal Pelaksanaan")
    add_guidance_box(doc, "Sajikan jadwal matriks rencana dan realisasi kerja praktik mingguan selama 40 hari kerja aktif magang di dinas dalam bentuk tabel ilmiah 3 garis horizontal.")
    add_caption_table(doc, "Tabel 1.1 Jadwal Pelaksanaan Kerja Praktik")
    
    # Template Tabel Jadwal Pelaksanaan
    jadwal_headers = ["No.", "Tahapan Aktivitas Proyek", "Bulan 1 (Minggu)", "Bulan 2 (Minggu)"]
    jadwal_widths = [Cm(1.2), Cm(7.8), Cm(3.5), Cm(3.5)]
    jadwal_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    jadwal_data = [
        ["1", "Perencanaan Proyek & Pengumpulan Data Awal", "Minggu 1 - 2", "-"],
        ["2", "Analisis Kebutuhan Sistem & Wawancara Dinas", "Minggu 3 - 4", "-"],
        ["3", "Perancangan Arsitektur Basis Data, UML, & UI", "-", "Minggu 1 - 2"],
        ["4", "Implementasi Pemrograman (Coding) Next.js", "-", "Minggu 2 - 3"],
        ["5", "Pengujian Sistem (Black-Box Testing) & Evaluasi", "-", "Minggu 3 - 4"],
        ["6", "Penyusunan Laporan Akhir & Demo Sistem", "-", "Minggu 4"]
    ]
    add_academic_table(doc, jadwal_headers, jadwal_data, jadwal_widths, jadwal_aligns)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # BAB II INSTANSI MITRA (HALAMAN 11)
    # ----------------------------------------------------
    add_heading_1(doc, "BAB II\nINSTANSI MITRA")
    
    add_heading_2(doc, "A. Profil Instansi Mitra")
    add_guidance_box(doc, "Uraikan profil resmi DINPERINNAKER Kabupaten Purbalingga, dasar hukum pembentukan (Peraturan Daerah Kabupaten Purbalingga Nomor 12 Tahun 2016 dan Perbup Nomor 87 Tahun 2021), sejarah kelembagaan penggabungan sektor industri dan tenaga kerja, serta peran strategis dinas dalam pembangunan daerah.")
    add_para(doc, "[Tuliskan profil dan sejarah kelembagaan dinas di sini...]")
    
    add_heading_2(doc, "B. Struktur Organisasi Mitra")
    add_guidance_box(doc, "Tampilkan bagan struktur organisasi dinas (Gambar 2.1) dan uraikan tugas pokok dan fungsi (Tupoksi) seluruh 7 unit kerja: Kepala Dinas, Sekretariat (Renkeu & Umpeg), Bidang HIJTK, Bidang PPTK, Bidang Perindustrian, UPTD BLK, dan UPTD PILOG.")
    add_para(doc, "[Tuliskan uraian tugas pokok dan fungsi unit kerja dinas di sini...]")
    add_image_placeholder(doc, "Gambar 2.1 Bagan Struktur Organisasi DINPERINNAKER Kabupaten Purbalingga")
    
    add_heading_2(doc, "C. Lokasi Mitra")
    add_guidance_box(doc, "Sajikan informasi lokasi kantor dinas, alamat lengkap, kontak telepon, email kedinasan, dan website resmi.")
    add_caption_table(doc, "Tabel 2.1 Informasi Lokasi dan Kontak Resmi DINPERINNAKER Kabupaten Purbalingga")
    
    lokasi_headers = ["Parameter Informasi", "Pemisah", "Keterangan Resmi Instansi"]
    lokasi_widths = [Cm(5.0), Cm(1.0), Cm(10.0)]
    lokasi_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    lokasi_data = [
        ["Nama Instansi", ":", "Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER)"],
        ["Pemerintah Daerah", ":", "Pemerintah Kabupaten Purbalingga, Provinsi Jawa Tengah"],
        ["Alamat Kantor", ":", "Jl. Mayjen Sungkono No. 34, Selabaya, Kec. Kalimanah, Kab. Purbalingga"],
        ["Kode Pos", ":", "53371"],
        ["Nomor Telepon", ":", "(0281) 891404"],
        ["Surel Resmi (Email)", ":", "dinperinnaker@purbalinggakab.go.id"],
        ["Website Resmi", ":", "https://dinperinnaker.purbalinggakab.go.id"]
    ]
    add_academic_table(doc, lokasi_headers, lokasi_data, lokasi_widths, lokasi_aligns)
    
    add_heading_2(doc, "D. Visi dan Misi")
    add_guidance_box(doc, "Tuliskan Visi dan Misi RPJMD Kabupaten Purbalingga 2021-2026 yang menjadi mandat bagi DINPERINNAKER, khususnya Misi Ke-3 (pertumbuhan ekonomi & lapangan kerja) dan Misi Ke-4 (tata kelola pemerintahan berbasis teknologi informasi).")
    add_para(doc, "[Tuliskan visi dan misi instansi di sini...]")
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # BAB III PELAKSANAAN PROYEK (HALAMAN 14)
    # ----------------------------------------------------
    add_heading_1(doc, "BAB III\nPELAKSANAAN PROYEK")
    
    add_heading_2(doc, "A. Hasil Tahapan Pelaksanaan")
    add_para(doc, "Pengembangan sistem informasi portal data SatuNaker dilaksanakan mengikuti tahapan metodologi Waterfall yang terstruktur ke dalam lima tahapan sekuensial, mulai dari perencanaan, analisis kebutuhan, perancangan sistem, pengembangan kode program, hingga pengujian perangkat lunak.")
    
    add_heading_3(doc, "1. Perencanaan (Planning)")
    add_guidance_box(doc, "Uraikan aktivitas tahap awal perencanaan proyek: (1) Observasi langsung proses pengelolaan data di kantor dinas, (2) Wawancara mendalam bersama Kepala Dinas (Johan Arifin, S.Sos., M.Si.) dan para Kepala Bidang, serta (3) Telaah dokumen fisik/digital (Laporan DBHCHT, data BPJS Ketenagakerjaan, data pelatihan BLK, direktori IKM).")
    add_para(doc, "[Tuliskan hasil pelaksanaan tahap perencanaan di sini...]")
    
    add_heading_3(doc, "2. Analisis Kebutuhan (Analysis)")
    add_guidance_box(doc, "Uraikan analisis kebutuhan sistem yang terbagi menjadi Analisis Kebutuhan Non-Fungsional (5 tabel spesifikasi resmi yang telah disetujui) dan Analisis Kebutuhan Fungsional (Matriks RBAC).")
    
    # a. Hardware
    add_para(doc, "a. Spesifikasi Kebutuhan Perangkat Keras (Hardware)", bold=True, first_line_indent=None)
    add_para(doc, "Spesifikasi kebutuhan perangkat keras mencakup lingkungan komputasi pengembang sistem serta spesifikasi minimal perangkat pengguna (klien dinas) baik melalui komputer desktop, laptop, maupun telepon pintar (smartphone) sebagaimana disajikan pada Tabel 3.1.")
    add_caption_table(doc, "Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)")
    hw_headers = ["No.", "Kategori Perangkat", "Spesifikasi Teknis Minimal"]
    hw_widths = [Cm(1.2), Cm(4.8), Cm(10.0)]
    hw_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]
    hw_data = [
        ["1", "Komputer Pengembang (Developer PC/Laptop)", "Prosesor AMD Ryzen 5 5500U / Intel Core i5 Generasi ke-11 (Base Clock 2.1 GHz, 6 Core, 12 Thread), Memori RAM 16 GB DDR4 Dual Channel 3200 MHz, Media Penyimpanan 512 GB SSD M.2 NVMe PCIe 3.0, Layar 14 Inci Full HD (1920x1080 piksel), Keyboard & Touchpad terintegrasi, Koneksi Internet Kecepatan Stabil."],
        ["2", "Perangkat Klien / Pengguna Dinas (Desktop / Laptop)", "Prosesor Dual Core 2.0 GHz (Intel Pentium Gold / Celeron / Core i3 setara), Memori RAM Minimal 2 GB (Disarankan 4 GB untuk kelancaran multitasking), Ruang Kosong Penyimpanan 500 MB untuk Cache Browser, Resolusi Layar Minimal 1366x768 piksel, Koneksi Jaringan Intranet / Internet Wi-Fi Dinas."],
        ["3", "Perangkat Klien Mobile (Smartphone / Tablet)", "Prosesor Quad-Core 1.5 GHz, Memori RAM Minimal 2 GB, Layar Sentuh dengan Resolusi Minimal 360x640 piksel (Mendukung Tampilan Responsif Mobile PWA), Jaringan Seluler 4G LTE / Wi-Fi."],
        ["4", "Perangkat Keras Input dan Output", "Keyboard Standar QWERTY, Mouse Optik / Touchpad, Monitor Eksternal Resolusi Minimal 1920x1080 piksel (Opsional untuk Analisis Dasbor), Printer Laserjet / Inkjet Berwarna untuk Pencetakan Laporan Ber-Kop Resmi."]
    ]
    add_academic_table(doc, hw_headers, hw_data, hw_widths, hw_aligns)
    
    # b. Software
    add_para(doc, "b. Spesifikasi Kebutuhan Perangkat Lunak (Software)", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Spesifikasi lingkungan perangkat lunak pengembangan dan operasional mencakup sistem operasi, perangkat lunak editor program, pengelola paket pustaka, platform basis data awan, serta piranti peramban web modern sebagaimana disajikan pada Tabel 3.2.")
    add_caption_table(doc, "Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)")
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
    add_academic_table(doc, sw_headers, sw_data, sw_widths, sw_aligns)
    
    # c. Web Tech Stack
    add_para(doc, "c. Spesifikasi Teknologi Website (Web Technology Stack)", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Sistem SatuNaker dikembangkan dengan memanfaatkan tumpukan teknologi modern (modern web stack) berbasis kerangka kerja Next.js 16 App Router dan pustaka reaktif React 19 guna menghadirkan performa tinggi, efisiensi kompilasi Turbopack, serta keandalan antarmuka sebagaimana disajikan pada Tabel 3.3.")
    add_caption_table(doc, "Tabel 3.3 Spesifikasi Teknologi Website (Web Technology Stack)")
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
    add_academic_table(doc, web_headers, web_data, web_widths, web_aligns)
    
    # d. Storage & Persistence
    add_para(doc, "d. Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Mekanisme penyimpanan data pada sistem SatuNaker dirancang secara hibrida multi-tier guna menjamin integritas data relasional, pembaruan waktu nyata (real-time), serta efisiensi penyimpanan fisik dokumen sebagaimana disajikan pada Tabel 3.4.")
    add_caption_table(doc, "Tabel 3.4 Arsitektur dan Spesifikasi Penyimpanan Data (Storage & Persistence)")
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
    add_academic_table(doc, st_headers, st_data, st_widths, st_aligns)
    
    # e. Aset Visual
    add_para(doc, "e. Katalog Aset Visual dan Desain Antarmuka", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Guna menghadirkan citra profesional kedinasan dan konsistensi antarmuka pengguna, sistem SatuNaker menggunakan aset visual resmi, palet warna branding DINPERINNAKER, serta standarisasi tata letak laporan kedinasan sebagaimana disajikan pada Tabel 3.5.")
    add_caption_table(doc, "Tabel 3.5 Katalog Aset Visual dan Desain Antarmuka")
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
    add_academic_table(doc, av_headers, av_data, av_widths, av_aligns)
    
    # f. RBAC Table
    add_para(doc, "f. Matriks Kebutuhan Hak Akses Pengguna (RBAC)", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Sistem SatuNaker menerapkan pembatasan hak akses berbasis peran (Role-Based Access Control) multi-level secara ketat guna menjaga integritas dan kerahasiaan data sektoral antar unit kerja. Matriks hak akses disajikan pada Tabel 3.6.")
    add_caption_table(doc, "Tabel 3.6 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)")
    rbac_headers = ["No.", "Fitur Fungsionalitas Sistem", "Super Admin / Kadis", "Admin Bidang / UPTD"]
    rbac_widths = [Cm(1.2), Cm(6.8), Cm(4.0), Cm(4.0)]
    rbac_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    rbac_data = [
        ["1", "Autentikasi Akun (Login & Logout)", "Tersedia Penuh", "Tersedia Penuh"],
        ["2", "Melihat Dasbor Eksekutif & Statistik Agregat", "Tersedia Penuh", "Tersedia Penuh"],
        ["3", "Menambah Data Sektoral Baru", "Bebas Semua Unit", "Terkunci Unit Sendiri (Auto-Lock)"],
        ["4", "Mengubah & Menghapus Data Sektoral", "Bebas Semua Unit", "Hanya Data Milik Unit Sendiri"],
        ["5", "Menyaring & Mencari Data Sektoral", "Tersedia Penuh", "Tersedia Penuh"],
        ["6", "Mengekspor Laporan ke Spreadsheet Excel", "Tersedia Penuh", "Tersedia Penuh"],
        ["7", "Mencetak Dokumen Laporan Kop Resmi Dinas", "Tersedia Penuh (Tanda Tangan Kadis)", "Pratinjau Draft Sektoral"],
        ["8", "Mengelola Master Unit Kerja Dinas", "Akses Khusus Super Admin", "Dibatasi (Hanya Baca)"],
        ["9", "Mengelola Akun Pengguna & Reset Sandi", "Akses Khusus Super Admin", "Tidak Dapat Mengakses"],
        ["10", "Pencadangan (Backup) & Pemulihan Basis Data", "Akses Khusus Super Admin", "Tidak Dapat Mengakses"]
    ]
    add_academic_table(doc, rbac_headers, rbac_data, rbac_widths, rbac_aligns)
    
    # 3. Perancangan Sistem
    add_heading_3(doc, "3. Perancangan Sistem (Design)")
    add_guidance_box(doc, "Uraikan: (1) Perancangan UML (Use Case Diagram & Activity Diagram), (2) Perancangan Desain Antarmuka (Purwarupa Wireframe UI), serta (3) Perancangan Basis Data (Kamus Data 4 tabel: unit_kerja, profiles, data_records, log_aktivitas dan ERD).")
    
    add_para(doc, "a. Perancangan Diagram Sistem (UML)", bold=True, first_line_indent=None)
    add_para(doc, "Interaksi fungsional sistem dimodelkan menggunakan Use Case Diagram (Gambar 3.1) dan Activity Diagram alur kerja operasional (Gambar 3.2 dan Gambar 3.3).")
    add_image_placeholder(doc, "Gambar 3.1 Use Case Diagram Sistem SatuNaker")
    add_image_placeholder(doc, "Gambar 3.2 Activity Diagram Login Pengguna")
    add_image_placeholder(doc, "Gambar 3.3 Activity Diagram Tambah Data Sektoral")
    
    add_para(doc, "b. Perancangan Basis Data (Database Design)", bold=True, first_line_indent=None, space_before=Pt(8))
    add_para(doc, "Struktur relasional basis data SatuNaker disajikan melalui Diagram Relasi Entitas (ERD) pada Gambar 3.4 serta kamus data terperinci pada Tabel 3.7 sampai dengan Tabel 3.10.")
    add_image_placeholder(doc, "Gambar 3.4 Relasi Antar Tabel (Entity Relationship Diagram - ERD)")
    
    # Kamus Data Tables
    add_caption_table(doc, "Tabel 3.7 Spesifikasi Struktur Tabel Basis Data unit_kerja")
    uk_headers = ["No.", "Nama Kolom", "Tipe Data", "Ukuran / Batasan", "Keterangan Kolom"]
    uk_widths = [Cm(1.0), Cm(3.5), Cm(2.5), Cm(3.0), Cm(6.0)]
    uk_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    uk_data = [
        ["1", "id", "bigint", "Primary Key", "Identifikator unik entitas unit kerja dinas"],
        ["2", "nama_unit", "varchar", "255, NOT NULL", "Nama resmi unit kerja struktural / UPTD dinas"],
        ["3", "tipe", "varchar", "50, NOT NULL", "Klasifikasi unit: 'bidang', 'sekretariat', 'uptd'"],
        ["4", "created_at", "timestamptz", "DEFAULT NOW()", "Waktu perekaman entitas pertama kali"],
        ["5", "updated_at", "timestamptz", "DEFAULT NOW()", "Waktu pembaruan data entitas terakhir"]
    ]
    add_academic_table(doc, uk_headers, uk_data, uk_widths, uk_aligns)
    
    add_caption_table(doc, "Tabel 3.8 Spesifikasi Struktur Tabel Basis Data profiles")
    p_headers = ["No.", "Nama Kolom", "Tipe Data", "Ukuran / Batasan", "Keterangan Kolom"]
    p_widths = [Cm(1.0), Cm(3.5), Cm(2.5), Cm(3.0), Cm(6.0)]
    p_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    p_data = [
        ["1", "id", "uuid", "Primary Key", "Identifikator unik pengguna terhubung auth Supabase"],
        ["2", "nama_lengkap", "varchar", "255, NOT NULL", "Nama lengkap pegawai operator pengelola data"],
        ["3", "username", "varchar", "50, UNIQUE", "Nama pengguna unik untuk proses login sistem"],
        ["4", "email", "varchar", "100, UNIQUE", "Alamat surel resmi kedinasan pengguna"],
        ["5", "role", "varchar", "50, NOT NULL", "Hak akses: 'Super Admin', 'Admin Bidang', 'Kepala Dinas'"],
        ["6", "unit_kerja_id", "bigint", "FK unit_kerja(id)", "Relasi ke unit kerja tempat pegawai bertugas"],
        ["7", "status", "varchar", "20, DEFAULT 'Aktif'", "Status keaktifan akun: 'Aktif' atau 'Nonaktif'"],
        ["8", "created_at", "timestamptz", "DEFAULT NOW()", "Waktu pembuatan akun pengguna"]
    ]
    add_academic_table(doc, p_headers, p_data, p_widths, p_aligns)
    
    add_caption_table(doc, "Tabel 3.9 Spesifikasi Struktur Tabel Basis Data data_records")
    dr_headers = ["No.", "Nama Kolom", "Tipe Data", "Ukuran / Batasan", "Keterangan Kolom"]
    dr_widths = [Cm(1.0), Cm(3.5), Cm(2.5), Cm(3.0), Cm(6.0)]
    dr_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    dr_data = [
        ["1", "id", "bigint", "Primary Key", "Identifikator unik entri rekaman data sektoral"],
        ["2", "unit_kerja_id", "bigint", "FK unit_kerja(id)", "Relasi ke unit kerja pemilik rekaman data"],
        ["3", "nama_data", "varchar", "255, NOT NULL", "Nama indikator atau judul capaian data dinas"],
        ["4", "satuan", "varchar", "50, NOT NULL", "Satuan ukur data (contoh: Orang, Kasus, Paket)"],
        ["5", "tahun_awal", "int", "CHECK (2000..2100)", "Tahun pencatatan data capaian indikator"],
        ["6", "jumlah", "numeric", "NOT NULL, min 0", "Besaran nilai numerik capaian statistik dinas"],
        ["7", "link_gdrive", "text", "NULLABLE", "Tautan URL dokumen bukti fisik di Google Drive"],
        ["8", "deskripsi", "text", "NULLABLE", "Uraian penjelasan metodologi atau catatan khusus"],
        ["9", "status", "varchar", "20, DEFAULT 'Aktif'", "Status publikasi data: 'Aktif', 'Arsip', 'Tidak Aktif'"],
        ["10", "created_by", "uuid", "FK profiles(id)", "Identifikator pengguna yang menginputkan data"]
    ]
    add_academic_table(doc, dr_headers, dr_data, dr_widths, dr_aligns)
    
    add_caption_table(doc, "Tabel 3.10 Spesifikasi Struktur Tabel Basis Data log_aktivitas")
    la_headers = ["No.", "Nama Kolom", "Tipe Data", "Ukuran / Batasan", "Keterangan Kolom"]
    la_widths = [Cm(1.0), Cm(3.5), Cm(2.5), Cm(3.0), Cm(6.0)]
    la_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    la_data = [
        ["1", "id", "bigint", "Primary Key", "Identifikator unik catatan riwayat log audit trail"],
        ["2", "user", "varchar", "100, NOT NULL", "Identitas nama pengguna yang melakukan transaksi"],
        ["3", "aktivitas", "text", "NOT NULL", "Deskripsi rinci tindakan perubahan data sistem"],
        ["4", "tanggal", "varchar", "50, NOT NULL", "Label tanggal transaksi yang mudah dibaca"],
        ["5", "ip_address", "varchar", "50, NULLABLE", "Alamat IP perangkat jaringan pengguna sistem"],
        ["6", "created_at", "timestamptz", "DEFAULT NOW()", "Waktu pencatatan jejak audit sistem"]
    ]
    add_academic_table(doc, la_headers, la_data, la_widths, la_aligns)
    
    # 4. Pengembangan Sistem
    add_heading_3(doc, "4. Pengembangan Sistem (Implementation)")
    add_guidance_box(doc, "Jelaskan proses implementasi pemrograman (Next.js 16, TypeScript, Tailwind CSS, Supabase) dan dokumentasikan tangkapan layar antarmuka sistem nyata (Gambar 3.8 sampai Gambar 3.17) lengkap dengan penjelasan fungsionalitasnya.")
    add_para(doc, "[Tuliskan penjelasan implementasi arsitektur kode dan penjelasan antarmuka di sini...]")
    
    screenshots = [
        ("Gambar 3.8 Tampilan Halaman Login Sistem", "Antarmuka autentikasi pengguna dengan proteksi sandi dan verifikasi peran."),
        ("Gambar 3.9 Tampilan Dasbor Eksekutif Kepala Dinas", "Dasbor pemantauan indikator kinerja agregat dan statistik grafik sektoral."),
        ("Gambar 3.10 Tampilan Dasbor dengan Filter Tahun Aktif", "Fitur penyaringan dasbor interaktif berdasarkan tahun anggaran."),
        ("Gambar 3.11 Tampilan Tabel Kelola Data Sektoral", "Tabel manajemen data sektoral dinas dengan fitur pencarian, filter, dan aksi."),
        ("Gambar 3.12 Tampilan Formulir Modal Tambah Data Sektoral", "Formulir input data sektoral yang dilengkapi validasi dan fitur auto-lock unit kerja."),
        ("Gambar 3.13 Tampilan Pusat Laporan Eksekutif", "Pusat rekapitulasi data sektoral dinas untuk pimpinan dan ekspor dokumen."),
        ("Gambar 3.14 Tampilan Pratinjau Dokumen Cetak Ber-Kop Resmi", "Format cetak resmi ber-kop Pemerintah Kabupaten Purbalingga DINPERINNAKER."),
        ("Gambar 3.15 Tampilan Manajemen Master Unit Kerja Dinas", "Modul pengelolaan daftar 7 unit kerja struktural dinas bagi Super Admin."),
        ("Gambar 3.16 Tampilan Manajemen Akun Pengguna & Hak Akses", "Modul tata kelola akun pegawai operator dinas dan pengaturan peran pengguna."),
        ("Gambar 3.17 Tampilan Pencadangan Mandiri (Backup) & Pemulihan Basis Data", "Modul cadangan data SQL Dump dan snapshot JSON untuk pemulihan bencana.")
    ]
    for g_title, g_desc in screenshots:
        add_para(doc, g_desc, italic=True)
        add_image_placeholder(doc, g_title)
        
    # 5. Pengujian Sistem
    add_heading_3(doc, "5. Pengujian Sistem (Testing)")
    add_guidance_box(doc, "Pengujian dilakukan menggunakan metode Black-Box Testing secara modular per halaman/fitur (Tabel 3.11 sampai Tabel 3.23). Setiap tabel memuat: No, Pengujian / Kasus Uji, Hasil yang Diharapkan, Hasil Pengujian, dan Status.")
    add_para(doc, "Guna menjamin mutu rekayasa perangkat lunak serta memastikan seluruh modul berjalan bebas dari cacat fungsional kritis, dilakukan pengujian perangkat lunak menggunakan metode Black-Box Testing yang difokuskan pada pengamatan masukan dan keluaran antarmuka tanpa memeriksa struktur kode internal.")
    
    # Template Pengujian Sample
    add_caption_table(doc, "Tabel 3.11 Pengujian Halaman Login")
    test_headers = ["No.", "Skenario Pengujian", "Hasil yang Diharapkan", "Hasil Pengujian", "Status"]
    test_widths = [Cm(1.0), Cm(4.5), Cm(4.5), Cm(4.0), Cm(2.0)]
    test_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    test_data = [
        ["1", "Memasukkan username dan password benar", "Sistem memvalidasi sesi dan mengarahkan ke dasbor", "Masuk ke halaman dasbor dinas", "Berhasil"],
        ["2", "Memasukkan kombinasi password yang salah", "Muncul notifikasi galat penolakan autentikasi", "Tampil notifikasi 'Kredensial tidak valid'", "Berhasil"],
        ["3", "Aksi keluar sistem (Logout)", "Sesi terhapus dan kembali ke layar login awal", "Berhasil keluar sistem secara aman", "Berhasil"]
    ]
    add_academic_table(doc, test_headers, test_data, test_widths, test_aligns)
    
    add_guidance_box(doc, "Lanjutkan tabel pengujian untuk modul lainnya (Tabel 3.12 s/d Tabel 3.23) dengan format kolom yang sama. Rincian seluruh tabel pengujian lengkap siap salin telah disediakan pada Bank Materi Pendukung.")
    
    # Kendala Pelaksanaan
    add_heading_2(doc, "B. Kendala Pelaksanaan")
    add_guidance_box(doc, "Uraikan kendala-kendala faktual yang dihadapi selama pelaksanaan kerja praktik di dinas beserta solusi rekayasa teknologi yang diterapkan.")
    add_caption_table(doc, "Tabel 3.24 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa")
    kendala_headers = ["No.", "Aspek Kendala", "Deskripsi Kendala Lapangan", "Solusi Rekayasa Sistem SatuNaker"]
    kendala_widths = [Cm(1.0), Cm(3.5), Cm(5.5), Cm(6.0)]
    kendala_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.JUSTIFY]
    kendala_data = [
        ["1", "Heterogenitas Format Data Mentah", "Setiap bidang memiliki format spreadsheet lokal yang berbeda tanpa standardisasi kolom dan satuan.", "Standardisasi skema basis data terpusat dengan validasi kolom wajib pada formulir modal input."],
        ["2", "Pemisahan Hak Akses Lintas Unit", "Risiko operator bidang keliru mengubah atau menghapus data milik bidang kerja lain.", "Penerapan Role-Based Access Control (RBAC) dan fitur auto-lock pilihan unit kerja sesuai akun operator."],
        ["3", "Penyimpanan Berkas Bukti Fisik Besar", "Keterbatasan kuota media penyimpanan server lokal untuk menampung ribuan dokumen PDF/PPT dinas.", "Penerapan arsitektur tautan hibrida terintegrasi ke Google Drive resmi dinas."],
        ["4", "Standardisasi Laporan Kedinasan", "Format pelaporan eksekutif harus mematuhi tata naskah dinas resmi Pemerintah Kabupaten Purbalingga.", "Pengembangan modul pratinjau cetak ber-kop resmi Pemkab Purbalingga lengkap dengan format pengesahan Kepala Dinas."]
    ]
    add_academic_table(doc, kendala_headers, kendala_data, kendala_widths, kendala_aligns)
    
    doc.add_page_break()
    
    # ----------------------------------------------------
    # BAB IV PENUTUP (HALAMAN 52)
    # ----------------------------------------------------
    add_heading_1(doc, "BAB IV\nPENUTUP")
    
    add_heading_2(doc, "A. Kesimpulan")
    add_guidance_box(doc, "Sajikan 3–4 butir kesimpulan yang menjawab rumusan masalah dan tujuan kerja praktik.")
    add_para(doc, "Berdasarkan hasil analisis, perancangan, implementasi, dan pengujian yang telah dilaksanakan pada proyek Kerja Praktik di Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga, dapat diambil kesimpulan sebagai berikut:")
    kesimpulan_pts = [
        "1. Telah berhasil dirancang dan dibangun Website Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker) berbasis Next.js 16 App Router dan Supabase PostgreSQL sebagai portal data statistik sektoral terpadu.",
        "2. Sistem SatuNaker berhasil menyatukan pencatatan data dari seluruh 7 unit kerja dinas (HIJTK, PPTK, Perindustrian, Renkeu, Umpeg, BLK, dan PILOG) ke dalam satu repositori sentral (Single Source of Truth), mengeliminasi fenomena pulau-pulau data (data silo).",
        "3. Penerapan mekanisme Role-Based Access Control (RBAC) dan fitur auto-lock unit kerja terbukti efektif menjaga integritas data antar-bidang dan membatasi wewenang modifikasi data sesuai tugas pokok masing-masing operator.",
        "4. Ketersediaan dasbor eksekutif, ekspor spreadsheet Excel otomatis, dan cetak dokumen resmi ber-kop Pemerintah Kabupaten Purbalingga berhasil memangkas waktu penyusunan laporan dinas secara signifikan."
    ]
    for k_txt in kesimpulan_pts:
        add_para(doc, k_txt, space_before=Pt(2), space_after=Pt(4), line_spacing=2.0, first_line_indent=Cm(0.5))
        
    add_heading_2(doc, "B. Saran")
    add_guidance_box(doc, "Sajikan saran konstruktif yang terbagi ke dalam 3 sasaran pihak: (1) Untuk Instansi Mitra, (2) Untuk Pengembangan Sistem, dan (3) Untuk Mahasiswa Kerja Praktik Selanjutnya.")
    
    saran_sections = [
        ("1. Untuk Instansi Mitra (DINPERINNAKER Kabupaten Purbalingga)", 
         "Pihak dinas disarankan menyusun Standar Operasional Prosedur (SOP) penginputan data berkala bagi para operator bidang dan UPTD, melaksanakan sosialisasi teknis pengoperasian sistem, serta menyediakan alokasi kapasitas penyimpanan Google Drive resmi kedinasan guna menjamin kelancaran penyimpanan berkas bukti fisik digital."),
        ("2. Untuk Pengembangan Sistem (SatuNaker)", 
         "Sistem dapat dikembangkan lebih lanjut dengan menambahkan fitur notifikasi otomatis ke surel/WhatsApp saat data baru diunggah, integrasi Application Programming Interface (API) langsung ke portal Satu Data Indonesia tingkat pusat/daerah (Bappeda), serta modul analitik prediksi tren ketenagakerjaan berbasis kecerdasan buatan."),
        ("3. Untuk Mahasiswa Kerja Praktik Selanjutnya", 
         "Mahasiswa kerja praktik pada periode berikutnya disarankan dapat memperluas pengujian sistem dengan automated unit and integration testing, optimalisasi performa caching peramban, serta perancangan aplikasi versi perangkat bergerak (mobile apps) berbasis framework Flutter atau React Native.")
    ]
    for s_title, s_desc in saran_sections:
        add_para(doc, s_title, bold=True, first_line_indent=None, space_before=Pt(6), space_after=Pt(2))
        add_para(doc, s_desc, first_line_indent=Cm(1.0), space_before=Pt(0), space_after=Pt(6))
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # DAFTAR PUSTAKA (HALAMAN 54)
    # ----------------------------------------------------
    add_heading_1(doc, "DAFTAR PUSTAKA")
    add_guidance_box(doc, "Daftar pustaka disusun secara alfabetis menggunakan format standar APA Style (American Psychological Association) 7th Edition dengan indentasi gantung (hanging indent 1.27 cm) dan spasi 1.0/1.5. Memuat literatur bereputasi dari buku referensi, jurnal ilmiah terakreditasi, regulasi pemerintah, dan dokumentasi teknologi resmi.")
    
    pustaka_list = [
        "Badan Pusat Statistik Kabupaten Purbalingga. (2024). Kabupaten Purbalingga dalam Angka 2024. BPS Kabupaten Purbalingga.",
        "Hidayat, A., & Rahmawati, E. (2022). Implementasi Kebijakan Satu Data Indonesia dalam Mendukung Tata Kelola Pemerintahan Berbasis Elektronik di Tingkat Daerah. Jurnal Kebijakan Publik dan Ilmu Administrasi, 10(2), 145–158.",
        "Jogiyanto, H. M. (2018). Analisis dan Desain Sistem Informasi: Pendekatan Terstruktur Teori dan Praktik Aplikasi Bisnis (Edisi 4). Andi Offset.",
        "Martin, R. C. (2018). Clean Architecture: A Craftsman's Guide to Software Structure and Design. Prentice Hall.",
        "Next.js Documentation. (2026). Next.js App Router Architecture, Turbopack, and Server Components Reference. Vercel Inc. https://nextjs.org/docs",
        "Nugroho, A. (2020). Rekayasa Perangkat Lunak Berorientasi Objek dengan Pendekatan UML (Edisi Revisi). Informatika Bandung.",
        "Pemerintah Kabupaten Purbalingga. (2021). Peraturan Daerah Kabupaten Purbalingga Nomor 5 Tahun 2021 tentang Rencana Pembangunan Jangka Menengah Daerah Kabupaten Purbalingga Tahun 2021–2026. Pemerintah Kabupaten Purbalingga.",
        "Pratama, I. P., & Widiastuti, N. (2024). Analisis Efektivitas Role-Based Access Control (RBAC) pada Sistem Portal Data Sektoral Dinas Ketenagakerjaan Daerah. Jurnal Teknologi Informasi dan Rekayasa Sistem Komputer, 12(1), 77–88.",
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "Republik Indonesia. (2019). Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia. Lembaran Negara Republik Indonesia Tahun 2019 Nomor 112.",
        "Saputra, R., & Handayani, T. (2023). Penerapan Model Waterfall dalam Rancang Bangun Sistem Informasi Pengelolaan Data Ketenagakerjaan Terintegrasi. Jurnal Riset Sistem Informasi dan Rekayasa Perangkat Lunak, 5(2), 112–123.",
        "Sommerville, I. (2019). Software Engineering (10th ed.). Pearson Education Limited.",
        "Supabase Documentation. (2026). PostgreSQL Database, Row Level Security, and Realtime Engine Guide. Supabase Inc. https://supabase.com/docs",
        "Tailwind Labs. (2026). Tailwind CSS Modern Utility-First Framework Documentation (v4.0). Tailwind Labs Inc. https://tailwindcss.com/docs"
    ]
    for p_item in pustaka_list:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Cm(1.27)
        p_ref.paragraph_format.first_line_indent = Cm(-1.27)
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.15
        r_ref = p_ref.add_run(p_item)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(11)
        
    doc.add_page_break()
    
    # ----------------------------------------------------
    # LAMPIRAN (HALAMAN 56)
    # ----------------------------------------------------
    add_heading_1(doc, "LAMPIRAN")
    add_guidance_box(doc, "Bagian lampiran menyajikan bukti fisik pelaksanaan magang: (1) Surat Keterangan Selesai KP dari dinas, (2) Formulir presensi daftar hadir seminar KP, (3) Lembar persetujuan laporan KP bertanda tangan, (4) Dokumen legalitas/SK Dinas, dan (5) Logbook harian magang.")
    
    lampiran_items = [
        ("Lampiran 1 Surat Keterangan Telah Menyelesaikan Kerja Praktik dari Mitra", 
         "[Tempatkan hasil pemindaian (scan) resmi Surat Keterangan Selesai Magang yang ditandatangani oleh Kepala Dinas DINPERINNAKER dan distempel resmi]"),
        ("Lampiran 2 Formulir Daftar Hadir Peserta Seminar Kerja Praktik", 
         "[Tempatkan formulir presensi seminar KP yang memuat tanda tangan minimal 20 mahasiswa peserta seminar dan dosen pembimbing/penguji]"),
        ("Lampiran 3 Lembar Persetujuan Laporan Kerja Praktik", 
         "[Tempatkan lembar persetujuan laporan kerja praktik yang telah ditandatangani asli oleh dosen pembimbing]"),
        ("Lampiran 4 Bukti Dokumen Legalitas / SK Instansi Mitra DINPERINNAKER", 
         "[Tempatkan salinan dokumen Perda / SK Bupati Purbalingga terkait pembentukan struktur DINPERINNAKER]"),
        ("Lampiran 5 Logbook Rekapitulasi Catatan Aktivitas Harian Magang Mahasiswa", 
         "[Tempatkan rekapitulasi catatan harian aktivitas magang selama 40 hari kerja aktif]")
    ]
    for l_title, l_box in lampiran_items:
        add_para(doc, l_title, bold=True, first_line_indent=None, space_before=Pt(10), space_after=Pt(4))
        p_lbox = doc.add_paragraph()
        p_lbox.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lbox.paragraph_format.space_before = Pt(8)
        p_lbox.paragraph_format.space_after = Pt(16)
        r_lb = p_lbox.add_run(f"📷 {l_box}")
        r_lb.font.name = "Times New Roman"
        r_lb.font.size = Pt(10.5)
        r_lb.font.italic = True
        r_lb.font.color.rgb = RGBColor(120, 120, 120)
        
    # Save the template file
    doc.save(OUTPUT_PATH)
    shutil.copyfile(OUTPUT_PATH, ARTIFACT_PATH)
    print("Template DOCX generated and copied to artifact successfully!")

if __name__ == "__main__":
    main()
