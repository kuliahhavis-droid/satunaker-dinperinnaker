# -*- coding: utf-8 -*-
"""
Full generator script to assemble LAPORAN_KP_SATUNAKER_SIAP_JADI.docx
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

ART_DIR = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54'
DOC_DIR = r'D:\Magang\sistem-satudata-dinperinnaker\document'
OUT_DOCX = os.path.join(DOC_DIR, 'LAPORAN_KP_SATUNAKER_SIAP_JADI.docx')
ART_DOCX = os.path.join(ART_DIR, 'LAPORAN_KP_SATUNAKER_SIAP_JADI.docx')

def set_page_setup(section):
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.575)    # 4 cm
    section.left_margin = Inches(1.575)   # 4 cm
    section.bottom_margin = Inches(1.181) # 3 cm
    section.right_margin = Inches(1.181)  # 3 cm

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

def add_p(doc, text, bold_prefix="", indent=0.5, line_spacing=2.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
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
    return p

def add_heading_1(doc, text, page_break_before=True):
    if page_break_before:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.first_line_indent = Inches(0)
    for line in text.split('\n'):
        r = p.add_run(line + '\n')
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    return p

def add_image_with_caption(doc, img_filename, caption_text, width_inches=5.2):
    img_path = os.path.join(ART_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.line_spacing = 1.0
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.first_line_indent = Inches(0)
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
    else:
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_img.add_run(f"[ Gambar {img_filename} ]")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.italic = True
        
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    p_cap.paragraph_format.first_line_indent = Inches(0)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11)
    r_cap.bold = True

def add_open_table(doc, caption_text, headers, rows_data, col_aligns=None, col_widths=None):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.space_before = Pt(10)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.first_line_indent = Inches(0)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11)
    r_cap.bold = True
    
    t = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    
    for c_idx, h in enumerate(headers):
        cell = t.cell(0, c_idx)
        cell.text = h
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.bold = True
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        set_cell_borders(cell, 
                         top={'val': 'single', 'sz': '8', 'color': '000000'},
                         bottom={'val': 'single', 'sz': '6', 'color': '000000'})
        if col_widths and c_idx < len(col_widths):
            cell.width = Inches(col_widths[c_idx])
            
    for r_idx, row in enumerate(rows_data, start=1):
        is_last = (r_idx == len(rows_data))
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Inches(0)
            
            if col_aligns and c_idx < len(col_aligns):
                p.alignment = col_aligns[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                
            set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
            if is_last:
                set_cell_borders(cell, bottom={'val': 'single', 'sz': '8', 'color': '000000'})
            else:
                set_cell_borders(cell)
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.line_spacing = 1.0

def build_complete_report():
    print("Building complete ready-to-use report...")
    doc = docx.Document()
    sec = doc.sections[0]
    set_page_setup(sec)
    
    # =========================================================================
    # 1. HALAMAN JUDUL (COVER)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("LAPORAN KERJA PRAKTIK\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    
    r2 = p.add_run("SISTEM SATU DATA\nDINAS PERINDUSTRIAN DAN TENAGA KERJA\nKABUPATEN PURBALINGGA\n(SATUNAKER)")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.bold = True
    
    # Logo UMP
    logo_path = os.path.join(ART_DIR, 'logo_ump.png')
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(24)
        p_logo.paragraph_format.space_after = Pt(24)
        p_logo.paragraph_format.line_spacing = 1.0
        p_logo.add_run().add_picture(logo_path, width=Inches(2.5))
        
    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.line_spacing = 1.15
    p_req.paragraph_format.space_before = Pt(0)
    p_req.paragraph_format.space_after = Pt(20)
    r_req = p_req.add_run("Disusun sebagai Salah Satu Syarat\nKelengkapan Kurikulum pada Prodi Teknik Informatika\nFakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto")
    r_req.font.name = 'Times New Roman'
    r_req.font.size = Pt(11)
    
    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.line_spacing = 1.15
    p_author.paragraph_format.space_before = Pt(0)
    p_author.paragraph_format.space_after = Pt(28)
    r_by = p_author.add_run("Disusun oleh:\n\nNama : Havisda Mei Khairil\nNIM : 2303040113\n")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(12)
    r_by.bold = True
    
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.line_spacing = 1.15
    p_univ.paragraph_format.space_before = Pt(0)
    p_univ.paragraph_format.space_after = Pt(0)
    r_univ = p_univ.add_run("PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS TEKNIK DAN SAINS\nUNIVERSITAS MUHAMMADIYAH PURWOKERTO\nNOVEMBER 2026")
    r_univ.font.name = 'Times New Roman'
    r_univ.font.size = Pt(12)
    r_univ.bold = True
    
    # =========================================================================
    # 2. LEMBAR PERSETUJUAN
    # =========================================================================
    doc.add_page_break()
    p_pers = doc.add_paragraph()
    p_pers.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pers.paragraph_format.line_spacing = 1.15
    p_pers.paragraph_format.space_before = Pt(0)
    p_pers.paragraph_format.space_after = Pt(12)
    r = p_pers.add_run("LEMBAR PERSETUJUAN LAPORAN\nKERJA PRAKTIK\n\nSISTEM SATU DATA\nDINAS PERINDUSTRIAN DAN TENAGA KERJA\nKABUPATEN PURBALINGGA\n(SATUNAKER)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    
    add_p(doc, "Disusun Oleh:\nNama : Havisda Mei Khairil\nNIM : 2303040113", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=14)
    add_p(doc, "Laporan Kerja Praktik Mahasiswa tersebut di Atas Dinyatakan Telah Memenuhi Syarat untuk Diseminarkan.", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=14)
    
    add_p(doc, "Disetujui : di Purwokerto\nTanggal : 2 November 2026\nOleh :", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=10)
    
    # Table approval
    t_app = doc.add_table(rows=2, cols=2)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row in t_app.rows:
        for c in row.cells:
            set_cell_borders(c)
    c0 = t_app.cell(0, 0)
    c0.text = "Pembimbing Kerja Praktik,\n\n\n\nElindra Ambar Pambudi, S.T., M.Kom.\nNIK. 2160766"
    for r in c0.paragraphs[0].runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    c1 = t_app.cell(0, 1)
    c1.text = "Pembimbing Lapangan,\n\n\n\nJohan Arifin, S.Sos., M.Si.\nNIP. 19740618 199311 1 001"
    for r in c1.paragraphs[0].runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    # =========================================================================
    # 3. HALAMAN PENGESAHAN
    # =========================================================================
    doc.add_page_break()
    p_peng = doc.add_paragraph()
    p_peng.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_peng.paragraph_format.line_spacing = 1.15
    p_peng.paragraph_format.space_before = Pt(0)
    p_peng.paragraph_format.space_after = Pt(12)
    r = p_peng.add_run("HALAMAN PENGESAHAN\nLAPORAN KERJA PRAKTIK\n\nSISTEM SATU DATA\nDINAS PERINDUSTRIAN DAN TENAGA KERJA\nKABUPATEN PURBALINGGA\n(SATUNAKER)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    
    add_p(doc, "Telah Diseminarkan dan Dipertahankan dalam Seminar Kerja Praktik Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto pada:", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=10, space_after=8)
    
    t_sem = doc.add_table(rows=2, cols=3)
    t_sem.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in t_sem.rows:
        for c in r.cells:
            set_cell_borders(c)
    t_sem.cell(0, 0).text = "Hari"
    t_sem.cell(0, 1).text = ":"
    t_sem.cell(0, 2).text = "Rabu"
    t_sem.cell(1, 0).text = "Tanggal"
    t_sem.cell(1, 1).text = ":"
    t_sem.cell(1, 2).text = "11 November 2026"
    for r in t_sem.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
                    
    add_p(doc, "Disetujui :\nDi : Purwokerto\nTanggal : 11 November 2026\nOleh:", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=10)
    
    t_sig = doc.add_table(rows=3, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in t_sig.rows:
        for c in r.cells:
            set_cell_borders(c)
    c0 = t_sig.cell(0, 0)
    c0.text = "Pembimbing,\n\n\n\nElindra Ambar Pambudi, S.T., M.Kom.\nNIK. 2160766"
    c1 = t_sig.cell(0, 1)
    c1.text = "Penguji,\n\n\n\nErmadi Satriya Wijaya, S.T., M.Kom.\nNIK. 2160731"
    
    c_k = t_sig.cell(2, 0)
    c_k.text = "Mengetahui,\nKetua Program Studi Teknik Informatika\n\n\n\nAgung Purwo Wicaksono, S.T., M.Kom.\nNIK. 2160518"
    
    for r in t_sig.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)

    # =========================================================================
    # 4. HALAMAN PERSEMBAHAN
    # =========================================================================
    add_heading_1(doc, "HALAMAN PERSEMBAHAN")
    add_p(doc, "Alhamdulillah puji syukur kepada Allah Subhanahu Wa Ta’ala, yang telah melimpahkan kesehatan, rahmat dan hidayah-Nya, sehingga penulis diberikan kelancaran dan kemudahan dalam menyelesaikan Kerja Praktik serta penyusunan laporan ini dengan baik. Laporan Kerja Praktik ini saya persembahkan dengan segenap ketulusan dan rasa hormat kepada:", indent=0, line_spacing=2.0)
    
    pers_list = [
        "1. Allah Subhanahu Wa Ta’ala, atas segala limpahan nikmat iman, kesehatan, dan kelancaran proses kerja praktik dari awal hingga akhir.",
        "2. Kedua orang tua tercinta dan segenap keluarga besar yang senantiasa mendukung, melimpahkan doa tulus, kasih sayang tanpa pamrih, serta motivasi materiel dan moril dalam setiap langkah penulis.",
        "3. Bapak Elindra Ambar Pambudi, S.T., M.Kom., selaku Dosen Pembimbing Kerja Praktik yang telah memberikan arahan, petunjuk berharga, dan kesabaran dalam membimbing hingga selesainya laporan ini.",
        "4. Bapak Agung Purwo Wicaksono, S.T., M.Kom., selaku Ketua Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto (UMP).",
        "5. Bapak Johan Arifin, S.Sos., M.Si., selaku Kepala Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga yang telah memberikan izin dan fasilitas pelaksanaan kerja praktik.",
        "6. Pembimbing Lapangan dan seluruh staf pegawai di lingkungan DINPERINNAKER Kabupaten Purbalingga (Bidang Hubungan Industrial & Jamsostek, Bidang PPTK, Bidang Industri, Subbag Renkeu, Subbag Umpeg, UPTD BLK, dan UPTD PILOG) atas kerja sama dan keterbukaannya selama magang.",
        "7. Rekan-rekan mahasiswa seperjuangan Teknik Informatika angkatan 2023 atas kebersamaan, diskusi, dan motivasi selama perkuliahan.",
        "8. Serta semua pihak yang tidak dapat penulis sebutkan satu per satu yang telah membantu dan berkontribusi hingga terselesaikannya laporan kerja praktik ini."
    ]
    for item in pers_list:
        add_p(doc, item, indent=0.5, line_spacing=2.0, space_before=2, space_after=2)

    # =========================================================================
    # 5. KATA PENGANTAR
    # =========================================================================
    add_heading_1(doc, "KATA PENGANTAR")
    add_p(doc, "Puji syukur ke hadirat Allah Subhanahu Wa Ta’ala atas limpahan rahmat, taufik, dan hidayah-Nya, sehingga penulis dapat menyelesaikan kegiatan Kerja Praktik serta menyusun laporan dengan judul “SISTEM SATU DATA DINAS PERINDUSTRIAN DAN TENAGA KERJA KABUPATEN PURBALINGGA (SATUNAKER)” dengan baik dan tepat pada waktunya.", indent=0.5, line_spacing=2.0)
    add_p(doc, "Laporan ini disusun guna memenuhi salah satu syarat kelulusan mata kuliah Kerja Praktik pada Program Studi Teknik Informatika, Fakultas Teknik dan Sains, Universitas Muhammadiyah Purwokerto. Melalui pelaksanaan kerja praktik ini, mahasiswa memperoleh pengalaman dan wawasan nyata di dunia kerja profesional, sekaligus mengaplikasikan teknologi rekayasa perangkat lunak modern ke dalam instansi pemerintahan daerah.", indent=0.5, line_spacing=2.0)
    add_p(doc, "Dalam pelaksanaan Kerja Praktik dan penyusunan naskah laporan ini, penulis telah banyak menerima bantuan, bimbingan, dan arahan berharga dari berbagai pihak. Oleh karena itu, pada kesempatan ini penulis menyampaikan rasa terima kasih dan apresiasi yang setinggi-tingginya kepada:", indent=0.5, line_spacing=2.0)
    
    kp_list = [
        "1. Bapak Dr. Ir. Taufik Dwi Laksono, S.T., M.T., IPU., selaku Dekan Fakultas Teknik dan Sains Universitas Muhammadiyah Purwokerto.",
        "2. Bapak Agung Purwo Wicaksono, S.T., M.Kom., selaku Ketua Program Studi Teknik Informatika Universitas Muhammadiyah Purwokerto.",
        "3. Bapak Elindra Ambar Pambudi, S.T., M.Kom., selaku Dosen Pembimbing Kerja Praktik yang senantiasa meluangkan waktu memberikan bimbingan dan saran konstruktif.",
        "4. Bapak Ermadi Satriya Wijaya, S.T., M.Kom., selaku Dosen Penguji Seminar Kerja Praktik atas masukan berharga demi kesempurnaan laporan ini.",
        "5. Bapak Johan Arifin, S.Sos., M.Si., selaku Kepala Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga sekaligus Pembimbing Lapangan yang telah memfasilitasi pelaksanaan kerja praktik.",
        "6. Seluruh Kepala Bidang, Kepala Subbagian, Kepala UPTD, dan staf pegawai di lingkungan DINPERINNAKER Kabupaten Purbalingga atas kerja sama dan bantuan data yang diberikan.",
        "7. Kedua orang tua dan keluarga tercinta atas doa, motivasi, serta kasih sayang yang tiada henti mengiringi langkah penulis."
    ]
    for item in kp_list:
        add_p(doc, item, indent=0.5, line_spacing=2.0, space_before=2, space_after=2)
        
    add_p(doc, "Penulis menyadari sepenuhnya bahwa penyusunan laporan ini masih jauh dari sempurna. Oleh karena itu, kritik dan saran yang konstruktif dari semua pihak senantiasa penulis harapkan guna penyempurnaan di masa mendatang. Semoga laporan ini dapat memberikan manfaat nyata bagi pembaca serta mendukung penguatan tata kelola data di DINPERINNAKER Kabupaten Purbalingga.", indent=0.5, line_spacing=2.0)
    
    add_p(doc, "Purwokerto, 11 November 2026\nPenulis,\n\n\n\nHavisda Mei Khairil\nNIM. 2303040113", indent=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=14, space_after=0)

    # =========================================================================
    # 6. DAFTAR ISI, TABEL, GAMBAR, LAMPIRAN
    # =========================================================================
    add_heading_1(doc, "DAFTAR ISI")
    daftar_isi_text = [
        ("HALAMAN JUDUL", "i"),
        ("LEMBAR PERSETUJUAN LAPORAN KERJA PRAKTIK", "ii"),
        ("HALAMAN PENGESAHAN", "iii"),
        ("HALAMAN PERSEMBAHAN", "iv"),
        ("KATA PENGANTAR", "v"),
        ("DAFTAR ISI", "vii"),
        ("DAFTAR TABEL", "ix"),
        ("DAFTAR GAMBAR", "xi"),
        ("DAFTAR LAMPIRAN", "xii"),
        ("ABSTRAK", "xiii"),
        ("BAB I GAMBARAN UMUM PROYEK", "1"),
        ("   A. Deskripsi Proyek", "1"),
        ("   B. Ruang Lingkup Proyek", "4"),
        ("   C. Tahapan Pelaksanaan Proyek", "6"),
        ("   D. Jadwal Pelaksanaan Proyek", "8"),
        ("BAB II INSTANSI MITRA", "10"),
        ("   A. Profil Instansi Mitra", "10"),
        ("   B. Struktur Organisasi Mitra", "12"),
        ("   C. Lokasi Mitra", "14"),
        ("   D. Visi dan Misi", "15"),
        ("BAB III PELAKSANAAN PROYEK", "18"),
        ("   A. Hasil Tahapan Pelaksanaan", "18"),
        ("      1. Perencanaan (Planning)", "18"),
        ("      2. Analisis Kebutuhan (Analysis)", "19"),
        ("      3. Perancangan Sistem (Design)", "23"),
        ("      4. Pengembangan Sistem (Implementation)", "32"),
        ("      5. Pengujian Sistem (Testing)", "42"),
        ("   B. Kendala Pelaksanaan dan Solusinya", "50"),
        ("BAB IV PENUTUP", "52"),
        ("   A. Kesimpulan", "52"),
        ("   B. Saran", "53"),
        ("DAFTAR PUSTAKA", "55"),
        ("LAMPIRAN", "58")
    ]
    for title, pg in daftar_isi_text:
        p_di = doc.add_paragraph()
        p_di.paragraph_format.line_spacing = 1.15
        p_di.paragraph_format.space_before = Pt(1)
        p_di.paragraph_format.space_after = Pt(1)
        p_di.paragraph_format.first_line_indent = Inches(0)
        r1 = p_di.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if title.startswith("BAB") or title in ["HALAMAN JUDUL", "DAFTAR ISI", "ABSTRAK", "DAFTAR PUSTAKA", "LAMPIRAN"]:
            r1.bold = True
        dots_count = max(3, 85 - len(title) - len(pg))
        r_dots = p_di.add_run(" " + "." * dots_count + " " + pg)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(11)

    # DAFTAR TABEL
    add_heading_1(doc, "DAFTAR TABEL")
    daftar_tabel_text = [
        ("Tabel 1.1 Matriks Jadwal Rencana dan Realisasi Kerja Praktik", "8"),
        ("Tabel 2.1 Informasi Lokasi dan Kontak Resmi DINPERINNAKER Kabupaten Purbalingga", "14"),
        ("Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)", "19"),
        ("Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)", "20"),
        ("Tabel 3.3 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)", "21"),
        ("Tabel 3.4 Spesifikasi Struktur Tabel Basis Data unit_kerja", "25"),
        ("Tabel 3.5 Spesifikasi Struktur Tabel Basis Data profiles", "26"),
        ("Tabel 3.6 Spesifikasi Struktur Tabel Basis Data data_records", "27"),
        ("Tabel 3.7 Spesifikasi Struktur Tabel Basis Data log_aktivitas", "28"),
        ("Tabel 3.8 Pengujian Autentikasi Pengguna (Login & Logout)", "43"),
        ("Tabel 3.9 Pengujian Dashboard Eksekutif & Pemantauan Data", "43"),
        ("Tabel 3.10 Pengujian Tambah Data Sektoral oleh Admin Bidang", "44"),
        ("Tabel 3.11 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja", "44"),
        ("Tabel 3.12 Pengujian Akses Tautan Data Dukung Google Drive", "45"),
        ("Tabel 3.13 Pengujian Ubah dan Hapus Data Sektoral", "45"),
        ("Tabel 3.14 Pengujian Pencarian dan Penyaringan Data (Filter)", "46"),
        ("Tabel 3.15 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)", "46"),
        ("Tabel 3.16 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga", "47"),
        ("Tabel 3.17 Pengujian Manajemen Master Unit Kerja (Super Admin)", "47"),
        ("Tabel 3.18 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)", "48"),
        ("Tabel 3.19 Pengujian Backup & Restore Basis Data (Super Admin)", "48"),
        ("Tabel 3.20 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)", "49"),
        ("Tabel 3.21 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa", "50")
    ]
    for title, pg in daftar_tabel_text:
        p_dt = doc.add_paragraph()
        p_dt.paragraph_format.line_spacing = 1.15
        p_dt.paragraph_format.space_before = Pt(1)
        p_dt.paragraph_format.space_after = Pt(1)
        p_dt.paragraph_format.first_line_indent = Inches(0)
        r1 = p_dt.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        dots_count = max(3, 85 - len(title) - len(pg))
        r_dots = p_dt.add_run(" " + "." * dots_count + " " + pg)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(11)

    # DAFTAR GAMBAR
    add_heading_1(doc, "DAFTAR GAMBAR")
    daftar_gambar_text = [
        ("Gambar 1.1 Tahapan Metode SDLC Pendekatan Waterfall", "7"),
        ("Gambar 2.1 Struktur Organisasi DINPERINNAKER Kabupaten Purbalingga", "13"),
        ("Gambar 3.1 Purwarupa Desain Antarmuka Halaman Login", "29"),
        ("Gambar 3.2 Use Case Diagram Sistem SatuNaker", "24"),
        ("Gambar 3.3 Activity Diagram Autentikasi Pengguna (Login)", "30"),
        ("Gambar 3.4 Activity Diagram Tambah Data Sektoral oleh Admin Bidang", "31"),
        ("Gambar 3.5 Desain Antarmuka Halaman Kelola Data Sektoral", "29"),
        ("Gambar 3.6 Relasi Antar Tabel Basis Data (Entity Relationship Diagram - ERD)", "24"),
        ("Gambar 3.7 Tampilan Halaman Autentikasi (Login)", "33"),
        ("Gambar 3.8 Tampilan Dasbor Eksekutif Kepala Dinas & Super Admin", "34"),
        ("Gambar 3.9 Tampilan Dasbor dengan Filter Tahun Kinerja Aktif", "35"),
        ("Gambar 3.10 Tampilan Tabel Manajemen Data Statistik Sektoral", "36"),
        ("Gambar 3.11 Tampilan Formulir Tambah Data Sektoral dengan Fitur Auto-Lock Unit", "37"),
        ("Gambar 3.12 Tampilan Pusat Laporan Eksekutif dan Panel Filter", "38"),
        ("Gambar 3.13 Tampilan Pratinjau Dokumen Cetak Ber-Kop Resmi Pemkab Purbalingga", "39"),
        ("Gambar 3.14 Tampilan Manajemen Master Unit Kerja Dinas", "40"),
        ("Gambar 3.15 Tampilan Manajemen Akun Pengguna & Hak Akses (RBAC)", "41"),
        ("Gambar 3.16 Tampilan Modul Pencadangan Mandiri (Backup) & Pemulihan Basis Data", "42")
    ]
    for title, pg in daftar_gambar_text:
        p_dg = doc.add_paragraph()
        p_dg.paragraph_format.line_spacing = 1.15
        p_dg.paragraph_format.space_before = Pt(1)
        p_dg.paragraph_format.space_after = Pt(1)
        p_dg.paragraph_format.first_line_indent = Inches(0)
        r1 = p_dg.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        dots_count = max(3, 85 - len(title) - len(pg))
        r_dots = p_dg.add_run(" " + "." * dots_count + " " + pg)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(11)

    # DAFTAR LAMPIRAN
    add_heading_1(doc, "DAFTAR LAMPIRAN")
    daftar_lampiran_text = [
        ("Lampiran 1 Surat Keterangan Telah Menyelesaikan Kerja Praktik", "58"),
        ("Lampiran 2 Lembar Persetujuan Seminar Kerja Praktik", "59"),
        ("Lampiran 3 Catatan Aktivitas Harian Mahasiswa (Logbook Magang)", "60"),
        ("Lampiran 4 Dokumentasi Kegiatan Magang dan Album Antarmuka Sistem", "63")
    ]
    for title, pg in daftar_lampiran_text:
        p_dl = doc.add_paragraph()
        p_dl.paragraph_format.line_spacing = 1.15
        p_dl.paragraph_format.space_before = Pt(1)
        p_dl.paragraph_format.space_after = Pt(1)
        p_dl.paragraph_format.first_line_indent = Inches(0)
        r1 = p_dl.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        dots_count = max(3, 85 - len(title) - len(pg))
        r_dots = p_dl.add_run(" " + "." * dots_count + " " + pg)
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(11)

    # =========================================================================
    # 7. ABSTRAK (INDONESIAN & ENGLISH)
    # =========================================================================
    add_heading_1(doc, "ABSTRAK")
    p_abs_head = doc.add_paragraph()
    p_abs_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_head.paragraph_format.line_spacing = 1.15
    p_abs_head.paragraph_format.space_before = Pt(0)
    p_abs_head.paragraph_format.space_after = Pt(12)
    r = p_abs_head.add_run("Havisda Mei Khairil\nElindra Ambar Pambudi, S.T., M.Kom.\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    
    t_abs_id = (
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
    add_p(doc, t_abs_id, indent=0.5, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10)
    
    p_kw_id = doc.add_paragraph()
    p_kw_id.paragraph_format.line_spacing = 1.0
    p_kw_id.paragraph_format.space_before = Pt(4)
    p_kw_id.paragraph_format.space_after = Pt(20)
    r_k = p_kw_id.add_run("Kata kunci: ")
    r_k.font.name = 'Times New Roman'
    r_k.font.size = Pt(11)
    r_k.bold = True
    r_kv = p_kw_id.add_run("satu data, dinperinnaker purbalingga, next.js, supabase, waterfall.")
    r_kv.font.name = 'Times New Roman'
    r_kv.font.size = Pt(11)
    r_kv.italic = True
    
    # ABSTRACT (English)
    add_heading_1(doc, "ABSTRACT")
    p_abs_en_head = doc.add_paragraph()
    p_abs_en_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_en_head.paragraph_format.line_spacing = 1.15
    p_abs_en_head.paragraph_format.space_before = Pt(0)
    p_abs_en_head.paragraph_format.space_after = Pt(12)
    r = p_abs_en_head.add_run("Havisda Mei Khairil\nElindra Ambar Pambudi, S.T., M.Kom.\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    
    t_abs_en = (
        "The Department of Industry and Manpower (DINPERINNAKER) of Purbalingga Regency oversees seven strategic operational units: "
        "Industrial Relations and Manpower Social Security, Training and Manpower Placement, Industry, Planning and Finance Sub-division, "
        "General Affairs and Personnel Sub-division, Regional Vocational Training Center (BLK), and Metal Industry Development Center (PILOG). "
        "Previously, sectoral data management was severely fragmented across isolated local spreadsheets (data silos) and unindexed physical "
        "archives, causing significant delays for leadership in monitoring holistic performance and requiring days of manual coordination for "
        "annual recapitulations. This Internship Project aims to design and develop the DINPERINNAKER One Data Website (SatuNaker) as a centralized "
        "sectoral data portal (Single Source of Truth). The system was developed using the classic Waterfall Software Development Life Cycle (SDLC) "
        "model, utilizing Next.js 16 (App Router), TypeScript, Tailwind CSS v4, and a Supabase PostgreSQL cloud database. Core features include "
        "multi-tiered Role-Based Access Control (RBAC) with operational unit auto-locking for operator admins, Google Drive link integration for "
        "seamless physical evidence verification without overloading server storage, an interactive executive dashboard with dynamic annual filters, "
        "styled Microsoft Excel (.xlsx) data export, an automated snapshot backup module, and an official Purbalingga Regency letterhead document "
        "print engine. Functional evaluation using Black-Box Testing across 13 test suites comprising 22 specific test scenarios demonstrated a "
        "100% valid success rate, successfully reducing the sectoral reporting time from 3–5 working days to less than five seconds while "
        "fulfilling the One Data Indonesia mandate at the local government level."
    )
    add_p(doc, t_abs_en, indent=0.5, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=10)
    
    p_kw_en = doc.add_paragraph()
    p_kw_en.paragraph_format.line_spacing = 1.0
    p_kw_en.paragraph_format.space_before = Pt(4)
    p_kw_en.paragraph_format.space_after = Pt(20)
    r_k = p_kw_en.add_run("Keywords: ")
    r_k.font.name = 'Times New Roman'
    r_k.font.size = Pt(11)
    r_k.bold = True
    r_kv = p_kw_en.add_run("one data, dinperinnaker purbalingga, next.js, supabase, waterfall.")
    r_kv.font.name = 'Times New Roman'
    r_kv.font.size = Pt(11)
    r_kv.italic = True

    # =========================================================================
    # 8. BAB I: GAMBARAN UMUM PROYEK
    # =========================================================================
    add_heading_1(doc, "BAB I\nGAMBARAN UMUM PROYEK")
    add_heading_2(doc, "A. Deskripsi Proyek")
    add_p(doc, "Dalam era transformasi digital kepemerintahan menuju penerapan *Electronic Government* (*E-Government*) yang terintegrasi, ketersediaan data statistik sektoral yang valid, akurat, mutakhir, dan mudah diakses merupakan fondasi esensial bagi perumusan kebijakan publik yang tepat sasaran. Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga sebagai unsur pelaksana urusan pemerintahan daerah di bidang perindustrian dan transmigrasi tenaga kerja menaungi 7 (tujuh) unit kerja operasional yang setiap periodenya memproduksi ratusan rekaman data strategis. Unit kerja tersebut meliputi Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK), Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK), Bidang Industri, Subbagian Perencanaan dan Keuangan (Renkeu), Subbagian Umum dan Kepegawaian (Umpeg), UPTD Balai Latihan Kerja (BLK), serta UPTD Pengembangan Industri Logam (PILOG).")
    add_p(doc, "Berdasarkan observasi lapangan dan wawancara mendalam yang dilakukan selama pelaksanaan Kerja Praktik, pengelolaan data di lingkungan DINPERINNAKER Kabupaten Purbalingga masih menghadapi hambatan struktural yang signifikan. Setiap bidang mengelola data operasionalnya secara mandiri menggunakan berkas lembar sebar (*spreadsheet*) lokal seperti Microsoft Excel tanpa standardisasi struktur kolom yang seragam. Kondisi ini menciptakan fenomena pulau-pulau data (*data silo*) di mana pertukaran informasi antar-bidang sangat terhambat (Hidayat & Rahmawati, 2022). Ketika pimpinan dinas atau instansi vertikal seperti Badan Pusat Statistik (BPS Kabupaten Purbalingga, 2024) dan Bappelitbangda memerlukan laporan rekapitulasi tahunan atau evaluasi Laporan Kinerja Instansi Pemerintah (LKjIP), staf dinas harus melakukan kompilasi manual berulang kali yang memakan waktu hingga berhari-hari kerja dan memiliki kerentanan tinggi terhadap kesalahan pengetikan ganda (*human error*).")
    add_p(doc, "Selain permasalahan pada data numerik tabular, kendala mendasar lainnya terletak pada verifikasi berkas bukti fisik data dukung operasional. Dokumen penting seperti berkas Perjanjian Kerja Bersama (PKB), risalah mediasi perselisihan ketenagakerjaan, dokumen penempatan pencari kerja (kartu AK-1), sertifikat kelulusan pelatihan vokasi BLK, hingga dokumen uji emisi knalpot PILOG seringkali masih diarsipkan dalam bentuk fisik di lemari berkas masing-masing seksi. Akibatnya, proses validasi keabsahan data membutuhkan pencarian dokumen fisik secara konvensional yang tidak efisien dan rentan terhadap risiko kerusakan fisik maupun kehilangan dokumen historis.")
    add_p(doc, "Menjawab permasalahan tersebut, proyek Kerja Praktik ini difokuskan pada perancangan dan pembangunan sistem portal data terpadu berbasis web modern yang diberi nama Website Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker). Sistem SatuNaker dirancang sebagai simpul sentral (*Single Source of Truth*) yang menyatukan seluruh aliran pencatatan data sektoral dari 7 unit kerja ke dalam satu basis data terpusat. Dengan arsitektur berbasis web modern, sistem ini memungkinkan staf admin bidang melakukan input data secara terstruktur, pimpinan dinas memantau indikator kinerja melalui dasbor eksekutif secara waktu-nyata (*real-time*), penelusuran bukti fisik terintegrasi melalui tautan penyimpanan awan Google Drive dinas, serta laporan resmi dinas dapat dicetak seketika lengkap dengan kop resmi Pemerintah Kabupaten Purbalingga selaras dengan amanat Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia (Republik Indonesia, 2019).")
    
    add_p(doc, "Adapun target capaian dan manfaat dari pelaksanaan proyek SatuNaker ini dirumuskan sebagai berikut:")
    add_p(doc, "1. Target Capaian Proyek:\n"
               "   a. Terbangunnya aplikasi web SatuNaker yang siap digunakan secara *live* dengan performa responsif dan antarmuka ramah pengguna.\n"
               "   b. Terwujudnya integrasi basis data sektoral dari 7 unit kerja di lingkungan DINPERINNAKER Kabupaten Purbalingga.\n"
               "   c. Terpangkasnya durasi penyusunan laporan rekapitulasi data sektoral dinas dari semula 3–5 hari kerja menjadi kurang dari lima detik.\n"
               "   d. Tersedianya dokumentasi teknis, buku panduan pengguna (*user manual*), serta laporan pertanggungjawaban Kerja Praktik.", indent=0.5)
    add_p(doc, "2. Manfaat Pelaksanaan Proyek:\n"
               "   a. Bagi Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga: Membantu mewujudkan efisiensi birokrasi, mengeliminasi duplikasi data antar-bidang, memudahkan Kepala Dinas dalam pengambilan keputusan berbasis data yang presisi, serta mempercepat pemenuhan data dukung bagi audit kinerja daerah.\n"
               "   b. Bagi Mahasiswa: Memberikan pengalaman praktis dalam mengimplementasikan kerangka kerja modern Next.js 16 (*App Router*), TypeScript, Tailwind CSS v4, dan basis data PostgreSQL Supabase pada studi kasus nyata instansi pemerintahan, serta melatih kemampuan komunikasi profesional di dunia kerja.\n"
               "   c. Bagi Program Studi Teknik Informatika UMP: Mempererat kemitraan strategis antara perguruan tinggi dengan pemerintah daerah, serta menjadi tolok ukur kualitas lulusan yang kompeten dan adaptif terhadap kebutuhan transformasi digital sektor publik.", indent=0.5)

    add_heading_2(doc, "B. Ruang Lingkup Proyek")
    add_p(doc, "Guna memastikan proses perancangan dan pembangunan sistem perangkat lunak berjalan terarah, terukur, dan selesai tepat waktu dalam batasan durasi 33 hari kerja aktif (1 Oktober 2026 sampai dengan 13 November 2026), ruang lingkup dan batasan sistem SatuNaker didefinisikan sebagai berikut:")
    add_p(doc, "1. Sistem mengintegrasikan pencatatan data statistik sektoral dari 7 (tujuh) unit kerja di lingkungan DINPERINNAKER Kabupaten Purbalingga, yaitu Bidang Hubungan Industrial (HIJTK), Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK), Bidang Industri, Subbagian Perencanaan dan Keuangan, Subbagian Umum dan Kepegawaian, UPTD Balai Latihan Kerja (BLK), dan UPTD PILOG.", indent=0.5)
    add_p(doc, "2. Menerapkan mekanisme otorisasi berbasis peran (*Role-Based Access Control* / RBAC) yang mencakup tingkatan: Super Admin (administrator sistem, master unit, akun staf, dan pencadangan), Admin Unit Kerja (Admin Bidang, Admin Sekretariat, dan Admin UPTD penginput data), serta Kepala Dinas (akses eksekutif pemantauan dasbor analitik dan pencetakan laporan).", indent=0.5)
    add_p(doc, "3. Menyediakan fitur penguncian otomatis (*auto-lock*) pilihan unit kerja pada formulir penambahan data bagi akun operator, guna mencegah terjadinya kekeliruan penginputan data lintas unit kerja.", indent=0.5)
    add_p(doc, "4. Menyediakan modul integrasi data dukung bukti fisik menggunakan penautan URL penyimpanan awan Google Drive resmi milik dinas untuk verifikasi instan berkas digital.", indent=0.5)
    add_p(doc, "5. Menyediakan fasilitas ekspor data sektoral ke dalam format lembar sebar (*spreadsheet*) Microsoft Excel (.xlsx) dan mesin cetak dokumen resmi ber-kop surat Pemerintah Kabupaten Purbalingga berbasis *CSS Print Media*.", indent=0.5)
    add_p(doc, "6. Sistem dikembangkan sebagai aplikasi berbasis web yang diakses menggunakan peramban modern (*browser* seperti Google Chrome, Mozilla Firefox, Microsoft Edge) dan memerlukan koneksi internet aktif untuk sinkronisasi dengan server komputasi awan Supabase.", indent=0.5)
    add_p(doc, "7. Pengelolaan data dukung bukti fisik tidak disimpan langsung ke dalam media penyimpanan server basis data lokal guna menghemat kapasitas penyimpanan dan biaya server, melainkan memanfaatkan tautan repositori Google Drive dinas.", indent=0.5)
    add_p(doc, "8. Pengembangan sistem dibangun menggunakan kerangka kerja modern Next.js 16 berbasis *App Router*, TypeScript, Tailwind CSS v4, dan basis data awan Supabase PostgreSQL (Supabase Documentation, 2026) yang dilengkapi kebijakan keamanan baris data (*Row Level Security* / RLS).", indent=0.5)
    add_p(doc, "9. Sistem tidak mencakup pemrosesan transaksi keuangan dinas secara langsung, pembayaran retribusi daerah, maupun pelayanan perizinan publik eksternal yang menjadi wewenang sistem OSS atau DPMPTSP.", indent=0.5)

    add_heading_2(doc, "C. Tahapan Pelaksanaan Proyek")
    add_p(doc, "Metodologi pengembangan perangkat lunak yang diterapkan dalam rekayasa sistem SatuNaker adalah metode *System Development Life Cycle* (SDLC) model sekuensial linier atau yang umum dikenal dengan istilah *Waterfall Model* (Pressman & Maxim, 2020). Pendekatan klasik ini dipilih karena kebutuhan fungsional sistem tata kelola data sektoral di instansi pemerintah telah terdefinisi secara terstruktur dan stabil berdasarkan regulasi serta format formulir baku dinas yang berlaku (Saputra & Handayani, 2023). Tahapan metodologi *Waterfall* yang dilalui digambarkan pada Gambar 1.1.")
    
    add_image_with_caption(doc, 'waterfall_diagram.png', 'Gambar 1.1 Tahapan Metode SDLC Pendekatan Waterfall', width_inches=4.8)
    
    add_p(doc, "Secara garis besar, tahapan rekayasa perangkat lunak SatuNaker terbagi ke dalam lima fase berurutan (Sommerville, 2019):")
    add_p(doc, "Mendefinisikan sasaran proyek, mengkaji permasalahan fragmentasi data dinas, dan menetapkan jadwal kerja praktik.", bold_prefix="1. Perencanaan (*Planning*): ", indent=0.5)
    add_p(doc, "Mengumpulkan data kebutuhan fungsional dan non-fungsional melalui wawancara dan telaah dokumen.", bold_prefix="2. Analisis Kebutuhan (*Requirement Analysis*): ", indent=0.5)
    add_p(doc, "Memodelkan relasi basis data (ERD), diagram perilaku sistem (UML *Use Case* dan *Activity Diagram*), serta antarmuka visual.", bold_prefix="3. Perancangan Sistem (*System Design*): ", indent=0.5)
    add_p(doc, "Mengembangkan kode program sistem web SatuNaker menggunakan teknologi Next.js 16 (*App Router*), TypeScript, Tailwind CSS v4, dan PostgreSQL Supabase.", bold_prefix="4. Implementasi (*Implementation*): ", indent=0.5)
    add_p(doc, "Menguji seluruh fungsionalitas sistem secara menyeluruh menggunakan metode *Black-Box Testing* pada 13 tabel guna memastikan keandalan sistem.", bold_prefix="5. Pengujian (*Testing*): ", indent=0.5)

    add_heading_2(doc, "D. Jadwal Pelaksanaan Proyek")
    add_p(doc, "Kegiatan Kerja Praktik dilaksanakan selama 33 hari kerja aktif terhitung sejak tanggal 1 Oktober 2026 sampai dengan tanggal 13 November 2026 bertempat di Kantor DINPERINNAKER Kabupaten Purbalingga. Matriks pelaksanaan tahapan proyek disajikan pada Tabel 1.1.")
    
    t1_1_headers = ['No.', 'Tahapan Aktivitas Proyek', 'Minggu 1-2', 'Minggu 3-4', 'Minggu 5-6', 'Status']
    t1_1_rows = [
        ['1', 'Observasi, Wawancara, & Analisis Masalah', '✓', '', '', 'Selesai'],
        ['2', 'Spesifikasi Kebutuhan & Desain UML/ERD', '✓', '✓', '', 'Selesai'],
        ['3', 'Pengodean Front-End & Integrasi Supabase', '', '✓', '✓', 'Selesai'],
        ['4', 'Pengujian Sistem (Black-Box Testing)', '', '', '✓', 'Selesai'],
        ['5', 'Penyusunan Laporan & Serah Terima Sistem', '', '', '✓', 'Selesai']
    ]
    t1_1_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    t1_1_widths = [0.5, 3.2, 0.9, 0.9, 0.9, 0.8]
    add_open_table(doc, "Tabel 1.1 Matriks Jadwal Rencana dan Realisasi Kerja Praktik", t1_1_headers, t1_1_rows, t1_1_aligns, t1_1_widths)

    # =========================================================================
    # 9. BAB II: INSTANSI MITRA
    # =========================================================================
    add_heading_1(doc, "BAB II\nINSTANSI MITRA")
    add_heading_2(doc, "A. Profil Instansi Mitra")
    add_p(doc, "Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga merupakan instansi pemerintah daerah tipe A yang dibentuk guna menyelenggarakan urusan pemerintahan konkuren di bidang perindustrian serta urusan pemerintahan di bidang tenaga kerja dan transmigrasi yang menjadi kewenangan daerah otonom Kabupaten Purbalingga, Provinsi Jawa Tengah.")
    
    add_heading_3(doc, "1. Dasar Hukum Pembentukan")
    add_p(doc, "Landasan hukum operasional DINPERINNAKER Kabupaten Purbalingga berpedoman pada:")
    add_p(doc, "a. Undang-Undang Nomor 23 Tahun 2014 tentang Pemerintahan Daerah sebagaimana telah beberapa kali diubah terakhir dengan Undang-Undang Nomor 9 Tahun 2015.", indent=0.5)
    add_p(doc, "b. Peraturan Pemerintah Nomor 18 Tahun 2016 tentang Perangkat Daerah.", indent=0.5)
    add_p(doc, "c. Peraturan Daerah Kabupaten Purbalingga Nomor 12 Tahun 2016 tentang Pembentukan dan Susunan Perangkat Daerah Kabupaten Purbalingga.", indent=0.5)
    add_p(doc, "d. Peraturan Bupati Purbalingga Nomor 87 Tahun 2021 tentang Kedudukan, Susunan Organisasi, Tugas dan Fungsi serta Tata Kerja Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.", indent=0.5)
    add_p(doc, "e. Peraturan Bupati Purbalingga Nomor 91 Tahun 2025 tentang Organisasi dan Tata Kerja Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga.", indent=0.5)
    
    add_heading_3(doc, "2. Sejarah Singkat Kelembagaan")
    add_p(doc, "Dalam sejarah kelembagaan perangkat daerah di Kabupaten Purbalingga, urusan perindustrian dan ketenagakerjaan mengalami beberapa kali dinamika penataan organisasi guna meningkatkan efektivitas pelayanan publik. Pada periode awal otonomi daerah, urusan perindustrian sempat digabungkan dalam lingkup Dinas Perindustrian, Perdagangan, dan Koperasi (DINPERINDAGKOP). Sementara itu, urusan ketenagakerjaan berada di bawah Dinas Sosial, Tenaga Kerja, dan Transmigrasi (DINSOSNAKERTRANS).")
    add_p(doc, "Melalui reformasi birokrasi penataan kelembagaan tahun 2016 berdasarkan Peraturan Daerah Nomor 12 Tahun 2016, Pemerintah Kabupaten Purbalingga secara strategis menyatukan sektor riil perindustrian dengan penyediaan dan perlindungan tenaga kerja dalam satu payung kelembagaan, yaitu Dinas Perindustrian dan Tenaga Kerja. Penyatuan ini bertujuan menciptakan sinergi harmonis antara pertumbuhan sentra industri manufaktur daerah (khususnya industri bulu mata tiruan, rambut palsu, dan sentra logam knalpot) dengan penyerapan tenaga kerja lokal yang kompeten dan terlindungi hak-hak ketenagakerjaannya (Badan Pusat Statistik Kabupaten Purbalingga, 2024).")

    add_heading_2(doc, "B. Struktur Organisasi Mitra")
    add_p(doc, "Struktur organisasi Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga dipimpin oleh seorang Kepala Dinas (*eselon II.b*) yang bertanggung jawab kepada Bupati Purbalingga melalui Sekretaris Daerah. Dalam menjalankan tugasnya, Kepala Dinas dibantu oleh Sekretariat yang membawahi Subbagian Perencanaan dan Keuangan serta Subbagian Umum dan Kepegawaian, tiga bidang teknis, yaitu Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja, Bidang Pelatihan dan Penempatan Tenaga Kerja, serta Bidang Industri, dua Unit Pelaksana Teknis Daerah (UPTD), serta kelompok Jabatan Fungsional dan Pelaksana. Seluruh unit kerja tersebut merupakan produsen data statistik sektoral yang menjadi pengguna operasional sistem SatuNaker yang dibangun dalam kerja praktik ini. Struktur organisasi disajikan pada Gambar 2.1.")
    
    add_image_with_caption(doc, 'struktur_organisasi_dinperinnaker.png', 'Gambar 2.1 Struktur Organisasi DINPERINNAKER Kabupaten Purbalingga', width_inches=5.2)
    
    add_p(doc, "Adapun rincian pembagian tugas pokok dan fungsi (tupoksi) 7 unit kerja di lingkungan DINPERINNAKER Kabupaten Purbalingga adalah sebagai berikut:")
    add_p(doc, "Memimpin perumusan kebijakan teknis, pembinaan, pengawasan, pengendalian, dan evaluasi pelaksanaan urusan pemerintahan daerah di bidang perindustrian dan ketenagakerjaan.", bold_prefix="1. Kepala Dinas: ", indent=0.5)
    add_p(doc, "Mengkoordinasikan perumusan rencana program anggaran, penatausahaan akuntansi keuangan, pengelolaan aset, ketatausahaan persuratan, dan pembinaan administrasi kepegawaian dinas melalui dua subbagian: Subbagian Perencanaan dan Keuangan (Renkeu) yang mengelola dokumen perencanaan (Renja, Renstra, DPA) dan pelaporan realisasi anggaran, serta Subbagian Umum dan Kepegawaian (Umpeg) yang mengelola administrasi aparatur sipil negara, pemeliharaan sarana prasarana, dan persuratan dinas.", bold_prefix="2. Sekretariat: ", indent=0.5)
    add_p(doc, "Menangani pencegahan dan penyelesaian perselisihan hubungan industrial (mediasi bipartit/tripartit), pendaftaran Perjanjian Kerja Bersama (PKB) dan Peraturan Perusahaan (PP), pencatatan serikat pekerja/buruh, serta pengawasan kepatuhan kepesertaan jaminan sosial ketenagakerjaan (BPJS Ketenagakerjaan dan BPJS Kesehatan).", bold_prefix="3. Bidang Hubungan Industrial dan Jaminan Sosial Tenaga Kerja (HIJTK): ", indent=0.5)
    add_p(doc, "Menyelenggarakan pelayanan informasi bursa kerja (*job fair*), penerbitan Kartu Tanda Bukti Pendaftaran Pencari Kerja (kartu AK-1), fasilitasi penempatan tenaga kerja dalam dan luar negeri (Pekerja Migran Indonesia), serta penyelenggaraan program transmigrasi.", bold_prefix="4. Bidang Pelatihan dan Penempatan Tenaga Kerja (PPTK): ", indent=0.5)
    add_p(doc, "Melaksanakan pendataan industri, fasilitasi legalitas Nomor Induk Berusaha (NIB) dan Izin Usaha Industri (IUI), bimbingan teknis mutu produksi, fasilitasi sertifikasi halal dan merek HAKI, serta penguatan kemitraan bagi pelaku Industri Kecil dan Menengah (IKM).", bold_prefix="5. Bidang Industri: ", indent=0.5)
    add_p(doc, "Unit pelaksana teknis yang bertugas menyelenggarakan pelatihan vokasi berbasis kompetensi (*competency-based training*) bagi para pencari kerja dalam bidang kejuruan teknik las, otomotif sepeda motor, manufaktur garmen, teknik pendingin, kelistrikan, dan teknologi informasi, serta menyelenggarakan uji sertifikasi kompetensi BNSP.", bold_prefix="6. UPTD Balai Latihan Kerja (BLK): ", indent=0.5)
    add_p(doc, "Unit pelaksana teknis yang bertugas memberikan pendampingan teknologi manufaktur permesinan, pengujian kualitas dan emisi gas buang (*dyno-test*) knalpot standar SNI, serta penyediaan sarana instalasi mesin presisi bagi sentra industri logam di Kabupaten Purbalingga.", bold_prefix="7. UPTD Pengembangan Industri Logam (PILOG): ", indent=0.5)

    add_heading_2(doc, "C. Lokasi Mitra")
    add_p(doc, "Kantor Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga berlokasi di pusat pemerintahan daerah yang strategis. Informasi lokasi dan kontak dinas disajikan pada Tabel 2.1.")
    
    t2_1_headers = ['No.', 'Parameter Informasi', 'Keterangan Resmi Instansi']
    t2_1_rows = [
        ['1', 'Nama Instansi', 'Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga'],
        ['2', 'Alamat Kantor Pusat', 'Jl. Letnan Kusni No. 06, Kedung Menjangan, Kec. Purbalingga'],
        ['3', 'Kode Pos Resmi', '53315, Kabupaten Purbalingga, Jawa Tengah'],
        ['4', 'Nomor Telepon', '(0281) 891044 / Faks: (0281) 891044'],
        ['5', 'Surat Elektronik (Email)', 'dinperinnaker@purbalinggakab.go.id'],
        ['6', 'Laman Resmi (Website)', 'https://dinperinnaker.purbalinggakab.go.id']
    ]
    t2_1_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    t2_1_widths = [0.5, 2.2, 4.5]
    add_open_table(doc, "Tabel 2.1 Informasi Lokasi dan Kontak Resmi DINPERINNAKER Kabupaten Purbalingga", t2_1_headers, t2_1_rows, t2_1_aligns, t2_1_widths)

    add_heading_2(doc, "D. Visi dan Misi")
    add_p(doc, "Visi merupakan rumusan umum mengenai keadaan yang diinginkan pada akhir periode perencanaan dengan mengacu pada RPJMD Kabupaten Purbalingga. Telaahan Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih untuk melihat sinkronisasi arah kebijakan pembangunan. Dinas Tenaga Kerja (Dinas Perindustrian dan Tenaga Kerja) Kabupaten Purbalingga yang merupakan salah satu Organisasi Perangkat Daerah Kabupaten Purbalingga dalam menjalankan tugas pokok dan fungsinya diarahkan untuk mendukung pencapaian Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih.", bold_prefix="1. Visi\n")
    add_p(doc, "“PURBALINGGA YANG MANDIRI DAN BERDAYA SAING MENUJU MASYARAKAT SEJAHTERA YANGBERAKHLAK MULIA”.", bold_prefix="Adapun Visi Kepala Daerah dan Wakil Kepala Daerah terpilih Kabupaten Purbalingga adalah ")
    
    add_p(doc, "Sebagai penjabaran dari Visi Kabupaten Purbalingga, maka Pemerintahan Kabupaten Purbalingga menetapkan misi. Misi merupakan sesuatu yang harus diemban atau dilaksanakan oleh suatu organisasi dalam merumuskan upaya-upaya untuk mewujudkan visi tersebut. Peraturan Daerah Kabupaten Purbalingga telah menetapkan Peraturan Daerah Kabupaten Purbalingga Nomor 05 Tahun 2021 tentang Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga tahun 2021-2026 meliputi:", bold_prefix="2. Misi\n")
    misi_web = [
        "1. Menyelenggarakan pemerintahan yang profesional, efisien, efektif, bersih dan demokratis, sehingga mampu memberikan pelayanan secara prima kepada masyarakat;",
        "2. Mendorong kehidupan masyarakat religius yang beriman dan bertaqwa kehadirat Allah SWT serta mengembangkan paham kebangsaan guna mewujudkan rasa aman dan tenteram dalam masyarakat yang berdasar pada realitas kebhinekaan;",
        "3. Mengupayakan kecukupan kebutuhan pokok manusia utamanya pangan dan papan secara layak;",
        "4. Meningkatkan kualitas sumberdaya manusia utamanya melalui peningkatan derajat pendidikan dan derajat kesehatan masyarakat;",
        "5. Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya industri pengolahan dan manufaktur, perdagangan, jasa, pariwisata, industri kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja;",
        "6. Meningkatkan pembangunan berbasis desa dan kawasan perdesaan melalui optimalisasi penyelenggaraan pemerintah desa, pembangunan pembinaan kemasyarakatan dan pemberdayaan masyarakat desa;",
        "7. Meningkatkan kualitas dan kuantitas sarana dan prasarana wilayah/infrastruktur dengan tetap memperhatikan kelestarian lingkungan."
    ]
    for m in misi_web:
        add_p(doc, m, indent=0.5, space_before=1, space_after=1)
        
    add_p(doc, "Dari pernyataan misi tersebut, dapat disimpulkan misi yang berkaitan di mana pencapaiannya didukung secara langsung oleh Dinas Perindustrian dan Tenaga Kerja yaitu pada Misi Ke-5, yaitu: “Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya dalam industri pengolahan dan manufaktur, pertanian, perdagangan, jasa, pariwisata, UMKM dan ekonomi kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja”.")
    add_p(doc, "Di samping Misi Ke-5, pengembangan Website Satu Data DINPERINNAKER (SatuNaker) dalam kerja praktik ini juga secara strategis mendukung pencapaian Misi Ke-1 (tata kelola pemerintahan yang profesional, efektif, bersih, dan akuntabel berbasis teknologi informasi) serta Misi Ke-4 (peningkatan kualitas sumber daya manusia dan tenaga kerja terampil melalui UPTD Balai Latihan Kerja).")

    # =========================================================================
    # 10. BAB III: PELAKSANAAN PROYEK
    # =========================================================================
    add_heading_1(doc, "BAB III\nPELAKSANAAN PROYEK")
    add_heading_2(doc, "A. Hasil Tahapan Pelaksanaan")
    add_p(doc, "Pengembangan sistem informasi portal data SatuNaker dilaksanakan mengikuti tahapan metodologi *Waterfall* yang terstruktur ke dalam lima tahapan sekuensial, mulai dari perencanaan, analisis kebutuhan, perancangan sistem, implementasi kode program, hingga pengujian perangkat lunak (Pressman & Maxim, 2020).")
    
    add_heading_3(doc, "1. Perencanaan (Planning)")
    add_p(doc, "Tahapan perencanaan diawali dengan mengidentifikasi kebutuhan mendesak DINPERINNAKER Kabupaten Purbalingga akan integrasi data statistik sektoral. Melalui diskusi bersama Kepala Dinas (Bapak Johan Arifin, S.Sos., M.Si.) dan para Kepala Bidang, disepakati bahwa sistem SatuNaker harus mampu menyatukan pelaporan dari 7 (tujuh) unit kerja dinas, menyediakan akses pemantauan instan untuk pimpinan daerah melalui dasbor eksekutif, serta menyederhanakan pelacakan berkas bukti fisik data dukung dengan menghubungkannya ke repositori penyimpanan awan Google Drive resmi milik dinas.")

    add_heading_3(doc, "2. Analisis Kebutuhan (Analysis)")
    add_p(doc, "Pada fase analisis kebutuhan, dilakukan eksplorasi terperinci terhadap kebutuhan perangkat keras, perangkat lunak, kebutuhan fungsional otorisasi pengguna, serta format data sektoral dari masing-masing bidang (Jogiyanto, 2018).")
    
    add_p(doc, "Spesifikasi perangkat keras komputer pengembangan yang digunakan disajikan pada Tabel 3.1.", bold_prefix="a. Spesifikasi Kebutuhan Perangkat Keras (*Hardware*)\n", indent=0)
    t3_1_headers = ['No.', 'Komponen Perangkat', 'Spesifikasi Teknis Minimal / Aktual']
    t3_1_rows = [
        ['1', 'Prosesor (CPU)', 'AMD Ryzen 5 5500H with Radeon Graphics (3.30 GHz)'],
        ['2', 'Memori Utama (RAM)', '8.00 GB DDR4 (5.86 GB usable) / Rekomendasi 16 GB'],
        ['3', 'Media Penyimpanan', 'SSD NVMe 512 GB (Sistem operasi & repositori lokal)'],
        ['4', 'Layar Tampilan (*Display*)', '15.6 Inci Full HD (1920 x 1080 piksel)'],
        ['5', 'Koneksi Jaringan Internet', 'Pita lebar minimal 10 Mbps untuk sinkronisasi awan Supabase']
    ]
    t3_1_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    t3_1_widths = [0.5, 2.3, 4.4]
    add_open_table(doc, "Tabel 3.1 Spesifikasi Kebutuhan Perangkat Keras (Hardware)", t3_1_headers, t3_1_rows, t3_1_aligns, t3_1_widths)

    add_p(doc, "Spesifikasi lingkungan perangkat lunak pengembangan yang digunakan disajikan pada Tabel 3.2.", bold_prefix="b. Spesifikasi Kebutuhan Perangkat Lunak (*Software*)\n", indent=0)
    t3_2_headers = ['No.', 'Perangkat Lunak', 'Deskripsi dan Versi Perangkat']
    t3_2_rows = [
        ['1', 'Sistem Operasi', 'Microsoft Windows 11 Pro 64-bit Edition'],
        ['2', 'Editor Kode (*Code Editor*)', 'Visual Studio Code versi 1.90+'],
        ['3', 'Lingkungan Eksekusi', 'Node.js versi 20.x LTS dan NPM versi 10.x'],
        ['4', 'Kerangka Kerja Front-End', 'Next.js 16 (*App Router*) dengan React 19 & TypeScript'],
        ['5', 'Framework CSS', 'Tailwind CSS v4 untuk penataan antarmuka responsif'],
        ['6', 'Platform Basis Data Cloud', 'Supabase Cloud Database (*PostgreSQL 15 Engine*)'],
        ['7', 'Pustaka Utilitas UI', 'Lucide React Icons & Radix UI Primitives'],
        ['8', 'Pustaka Ekspor Data', 'SheetJS (*xlsx library*) untuk konversi spreadsheet']
    ]
    t3_2_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    t3_2_widths = [0.5, 2.3, 4.4]
    add_open_table(doc, "Tabel 3.2 Spesifikasi Kebutuhan Perangkat Lunak (Software)", t3_2_headers, t3_2_rows, t3_2_aligns, t3_2_widths)

    add_p(doc, "Sistem SatuNaker menerapkan pembatasan hak akses berbasis peran secara ketat guna menjaga integritas dan kerahasiaan data pemerintah (Pratama & Widiastuti, 2024). Matriks hak akses disajikan pada Tabel 3.3.", bold_prefix="c. Matriks Kebutuhan Hak Akses Pengguna (*Role-Based Access Control* / RBAC)\n", indent=0)
    t3_3_headers = ['No.', 'Fitur Sistem', 'Super Admin', 'Admin Unit Kerja', 'Kepala Dinas']
    t3_3_rows = [
        ['1', 'Autentikasi (*Login & Logout*)', 'Diizinkan', 'Diizinkan', 'Diizinkan'],
        ['2', 'Pemantauan Dasbor Eksekutif', 'Seluruh Unit', 'Unit Sendiri', 'Seluruh Unit'],
        ['3', 'Filter Data Lintas Tahun/Kategori', 'Seluruh Unit', 'Unit Sendiri', 'Seluruh Unit'],
        ['4', 'Tambah Rekaman Data Sektoral', 'Diizinkan', 'Diizinkan (*auto-lock*)', 'Ditolak'],
        ['5', 'Ubah dan Hapus Rekaman Data', 'Diizinkan', 'Diizinkan (Unit Sendiri)', 'Ditolak'],
        ['6', 'Akses Tautan Google Drive', 'Diizinkan', 'Diizinkan', 'Diizinkan'],
        ['7', 'Ekspor Laporan ke Excel (.xlsx)', 'Diizinkan', 'Diizinkan', 'Diizinkan'],
        ['8', 'Cetak Laporan Ber-Kop Resmi', 'Diizinkan', 'Diizinkan', 'Diizinkan'],
        ['9', 'Manajemen Master Unit Kerja', 'Diizinkan', 'Ditolak', 'Ditolak'],
        ['10', 'Manajemen Pengguna & Sandi', 'Diizinkan', 'Ditolak', 'Ditolak'],
        ['11', 'Backup & Restore Snapshot JSON', 'Diizinkan', 'Ditolak', 'Ditolak'],
        ['12', 'Pemantauan Log Audit Trail', 'Diizinkan', 'Ditolak', 'Ditolak']
    ]
    t3_3_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    t3_3_widths = [0.4, 2.8, 1.3, 1.4, 1.3]
    add_open_table(doc, "Tabel 3.3 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)", t3_3_headers, t3_3_rows, t3_3_aligns, t3_3_widths)

    add_heading_3(doc, "3. Perancangan Sistem (Design)")
    add_p(doc, "Tahapan perancangan mencakup pemodelan konseptual basis data relasional (*Entity Relationship Diagram* / ERD), spesifikasi kamus data tabel, pemodelan interaksi pengguna menggunakan UML (*Use Case* dan *Activity Diagram*), serta purwarupa desain antarmuka pengguna (*wireframe UI*).")
    
    add_p(doc, "Struktur basis data relasional SatuNaker dimodelkan secara terstruktur dengan menerapkan prinsip normalisasi bentuk ketiga (3NF) guna meniadakan redundansi data. Diagram Relasi Entitas disajikan pada Gambar 3.1.", bold_prefix="a. Perancangan Basis Data Relasional (*Entity Relationship Diagram*)\n", indent=0)
    add_image_with_caption(doc, 'erd_diagram.png', 'Gambar 3.1 Relasi Antar Tabel Basis Data (Entity Relationship Diagram - ERD)', width_inches=5.2)
    
    add_p(doc, "Kamus data spesifikasi kolom untuk masing-masing tabel relasional disajikan pada Tabel 3.4 sampai dengan Tabel 3.7.")
    
    t3_4_headers = ['No.', 'Nama Kolom', 'Tipe Data', 'Kunci', 'Keterangan Atribut']
    t3_4_rows = [
        ['1', 'id', 'BIGINT', 'Primary Key', 'Pengidentifikasi unik baris unit kerja'],
        ['2', 'nama_unit', 'VARCHAR(150)', '-', 'Nama lengkap unit kerja/bidang dinas'],
        ['3', 'tipe', 'VARCHAR(30)', '-', 'Klasifikasi tipe: bidang, sekretariat, uptd'],
        ['4', 'created_at', 'TIMESTAMPTZ', '-', 'Waktu pencatatan data ke dalam sistem'],
        ['5', 'updated_at', 'TIMESTAMPTZ', '-', 'Waktu terakhir pembaruan data']
    ]
    t3_4_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    t3_4_widths = [0.4, 1.4, 1.3, 1.1, 3.0]
    add_open_table(doc, "Tabel 3.4 Spesifikasi Struktur Tabel Basis Data unit_kerja", t3_4_headers, t3_4_rows, t3_4_aligns, t3_4_widths)

    t3_5_headers = ['No.', 'Nama Kolom', 'Tipe Data', 'Kunci', 'Keterangan Atribut']
    t3_5_rows = [
        ['1', 'id', 'BIGINT / UUID', 'Primary Key', 'Terhubung dengan autentikasi Supabase'],
        ['2', 'nama_lengkap', 'VARCHAR(150)', '-', 'Nama lengkap pegawai pengguna akun'],
        ['3', 'username', 'VARCHAR(50)', 'Unique', 'Identitas unik nama pengguna saat login'],
        ['4', 'email', 'VARCHAR(100)', 'Unique', 'Alamat surel resmi kedinasan pengguna'],
        ['5', 'role', 'VARCHAR(30)', '-', 'Peran: Super Admin, Admin Bidang, dll.'],
        ['6', 'unit_kerja_id', 'BIGINT', 'Foreign Key', 'Kunci tamu berelasi ke tabel unit_kerja'],
        ['7', 'status', 'VARCHAR(20)', '-', 'Status keaktifan akun: Aktif, Nonaktif'],
        ['8', 'created_at', 'TIMESTAMPTZ', '-', 'Waktu akun pertama kali didaftarkan']
    ]
    t3_5_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    t3_5_widths = [0.4, 1.4, 1.3, 1.1, 3.0]
    add_open_table(doc, "Tabel 3.5 Spesifikasi Struktur Tabel Basis Data profiles", t3_5_headers, t3_5_rows, t3_5_aligns, t3_5_widths)

    t3_6_headers = ['No.', 'Nama Kolom', 'Tipe Data', 'Kunci', 'Keterangan Atribut']
    t3_6_rows = [
        ['1', 'id', 'BIGINT', 'Primary Key', 'Pengidentifikasi unik rekaman data'],
        ['2', 'unit_kerja_id', 'BIGINT', 'Foreign Key', 'Kunci tamu pemilik data ke unit_kerja'],
        ['3', 'nama_data', 'VARCHAR(255)', '-', 'Judul indikator data sektoral dinas'],
        ['4', 'satuan', 'VARCHAR(50)', '-', 'Satuan ukur (orang, kasus, unit usaha)'],
        ['5', 'tahun_awal', 'INTEGER', '-', 'Tahun anggaran kinerja rekaman data'],
        ['6', 'jumlah', 'NUMERIC(15,2)', '-', 'Nilai capaian data numerik sektoral'],
        ['7', 'link_gdrive', 'TEXT', '-', 'Tautan URL bukti dukung fisik di Drive'],
        ['8', 'deskripsi', 'TEXT', '-', 'Catatan metodologi / dasar hukum data'],
        ['9', 'status', 'VARCHAR(30)', '-', 'Status publikasi data (Aktif, Arsip)'],
        ['10', 'created_by', 'BIGINT', 'Foreign Key', 'Kunci tamu pembuat data ke profiles']
    ]
    t3_6_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    t3_6_widths = [0.4, 1.4, 1.3, 1.1, 3.0]
    add_open_table(doc, "Tabel 3.6 Spesifikasi Struktur Tabel Basis Data data_records", t3_6_headers, t3_6_rows, t3_6_aligns, t3_6_widths)

    t3_7_headers = ['No.', 'Nama Kolom', 'Tipe Data', 'Kunci', 'Keterangan Atribut']
    t3_7_rows = [
        ['1', 'id', 'BIGINT', 'Primary Key', 'Pengidentifikasi unik baris catatan log'],
        ['2', 'user', 'VARCHAR(50)', '-', 'Identitas akun yang bertransaksi'],
        ['3', 'aktivitas', 'TEXT', '-', 'Rincian deskripsi transaksi aktivitas'],
        ['4', 'tanggal', 'VARCHAR(50)', '-', 'Format tanggal waktu lokal transaksi'],
        ['5', 'ip_address', 'VARCHAR(45)', '-', 'Alamat IP perangkat pengguna (klien)'],
        ['6', 'created_at', 'TIMESTAMPTZ', '-', 'Waktu waktu-nyata rekaman disimpan']
    ]
    t3_7_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    t3_7_widths = [0.4, 1.4, 1.3, 1.1, 3.0]
    add_open_table(doc, "Tabel 3.7 Spesifikasi Struktur Tabel Basis Data log_aktivitas", t3_7_headers, t3_7_rows, t3_7_aligns, t3_7_widths)

    add_p(doc, "Interaksi fungsional antara tiga tingkatan pengguna dengan sistem SatuNaker dimodelkan melalui *Use Case Diagram* (Nugroho, 2020) yang disajikan pada Gambar 3.2. Dalam model ini, Super Admin memiliki otoritas menyeluruh, Kepala Dinas memiliki hak akses eksekutif analitik dan cetak, sedangkan Admin Unit Kerja memiliki wewenang input dan verifikasi data yang terkunci pada unitnya masing-masing.", bold_prefix="b. Pemodelan Diagram Perilaku Sistem (UML *Use Case* dan *Activity Diagram*)\n", indent=0)
    add_image_with_caption(doc, 'use_case_diagram.png', 'Gambar 3.2 Use Case Diagram Sistem SatuNaker', width_inches=4.8)
    
    add_p(doc, "Alur kerja dinamis pada transaksi autentikasi pengguna dimodelkan pada Gambar 3.3. Diagram ini memodelkan proses verifikasi identitas pengguna dan pengalihan otomatis (*routing*) ke rute dasbor yang sesuai hak aksesnya.")
    add_image_with_caption(doc, 'activity_diagram_login.png', 'Gambar 3.3 Activity Diagram Autentikasi Pengguna (Login)', width_inches=4.5)
    
    add_p(doc, "Tata cara operasional operator unit kerja dalam mencatat rekaman data capaian baru yang dilengkapi fitur penautan berkas bukti dukung fisik Google Drive digambarkan pada Gambar 3.4.")
    add_image_with_caption(doc, 'activity_diagram_tambah_data.png', 'Gambar 3.4 Activity Diagram Tambah Data Sektoral oleh Admin Bidang', width_inches=4.5)

    add_p(doc, "Sebelum tahap pengodean program dilaksanakan, purwarupa desain antarmuka visual (*wireframe*) disusun guna menyamakan persepsi tata letak antarmuka bersama pihak dinas.", bold_prefix="c. Purwarupa Desain Antarmuka Pengguna (*Wireframe UI*)\n", indent=0)
    add_p(doc, "Purwarupa antarmuka halaman login dirancang terpusat (*center card layout*) yang memuat logo resmi Pemerintah Kabupaten Purbalingga, judul portal, kolom isian *username* dan kata sandi, serta tombol masuk ke sistem, sebagaimana disajikan pada Gambar 3.5.")
    add_image_with_caption(doc, 'wireframe_login.png', 'Gambar 3.5 Purwarupa Desain Antarmuka Halaman Login', width_inches=4.0)
    
    add_p(doc, "Purwarupa halaman kelola data dirancang secara tabular untuk mempermudah operator bidang dalam meninjau dan memperbarui capaian data statistik sektoral, sebagaimana disajikan pada Gambar 3.6.")
    add_image_with_caption(doc, 'wireframe_kelola_data.png', 'Gambar 3.6 Desain Antarmuka Halaman Kelola Data Sektoral', width_inches=5.2)

    add_heading_3(doc, "4. Pengembangan Sistem (Implementation)")
    add_p(doc, "Fase pengembangan sistem SatuNaker mengimplementasikan rancangan konseptual ke dalam baris-baris kode program nyata berbasis arsitektur web modern (Martin, 2018). Pengodean dilakukan menggunakan kerangka kerja Next.js 16 berbasis *App Router*, bahasa pemrograman TypeScript yang menjamin keamanan tipe (*type-safety*), serta kelas utilitas Tailwind CSS v4 untuk menghasilkan antarmuka yang bersih, responsif, dan ramah pengguna (Tailwind Labs Inc., 2026). Dokumentasi visual hasil implementasi antarmuka sistem SatuNaker yang telah beroperasi diuji secara langsung pada peramban melalui lingkungan lokal `http://localhost:3000`:")
    
    # 10 UI Screenshots from localhost:3000
    add_p(doc, "Formulir autentikasi pengguna dengan pengamanan kata sandi, validasi sesi aktif, dan proteksi rute halaman disajikan pada Gambar 3.7.", bold_prefix="a. Antarmuka Halaman Autentikasi (*Login*)\n", indent=0)
    add_image_with_caption(doc, 'ss_01_login.png', 'Gambar 3.7 Tampilan Halaman Autentikasi (Login)', width_inches=5.2)
    
    add_p(doc, "Dasbor statistik analitik yang menyajikan ringkasan agregat kartu metrik kinerja utama seluruh unit kerja dinas secara terpusat disajikan pada Gambar 3.8.", bold_prefix="b. Dasbor Eksekutif Kepala Dinas & Super Admin\n", indent=0)
    add_image_with_caption(doc, 'ss_02_dashboard_eksekutif.png', 'Gambar 3.8 Tampilan Dasbor Eksekutif Kepala Dinas & Super Admin', width_inches=5.2)
    
    add_p(doc, "Fitur penyaringan data dinamis berdasarkan tahun anggaran kinerja yang memperbarui grafik analitik secara instan tanpa memuat ulang peramban disajikan pada Gambar 3.9.", bold_prefix="c. Dasbor Interaktif dengan Filter Tahun Kinerja Aktif\n", indent=0)
    add_image_with_caption(doc, 'ss_03_dashboard_filter_tahun.png', 'Gambar 3.9 Tampilan Dasbor dengan Filter Tahun Kinerja Aktif', width_inches=5.2)
    
    add_p(doc, "Tabel data utama yang memuat fungsi penambahan, pengubahan, penghapusan, pencarian instan, dan tombol penelusuran tautan Google Drive disajikan pada Gambar 3.10.", bold_prefix="d. Tabel Manajemen Data Statistik Sektoral\n", indent=0)
    add_image_with_caption(doc, 'ss_04_kelola_data_sektoral.png', 'Gambar 3.10 Tampilan Tabel Manajemen Data Statistik Sektoral', width_inches=5.2)
    
    add_p(doc, "Formulir entri data sektoral yang mengunci otomatis pilihan unit kerja sesuai identitas sesi login pengguna Admin Bidang guna mencegah kesalahan penginputan disajikan pada Gambar 3.11.", bold_prefix="e. Formulir Tambah Data Sektoral dengan Fitur *Auto-Lock* Unit\n", indent=0)
    add_image_with_caption(doc, 'ss_05_modal_tambah_data.png', 'Gambar 3.11 Tampilan Formulir Tambah Data Sektoral dengan Fitur Auto-Lock Unit', width_inches=5.0)
    
    add_p(doc, "Modul rekapitulasi data lintas bidang yang dilengkapi fasilitas pemilihan parameter filter unit kerja, tahun pelaporan, dan rentang tanggal disajikan pada Gambar 3.12.", bold_prefix="f. Pusat Laporan Eksekutif dan Panel Filter\n", indent=0)
    add_image_with_caption(doc, 'ss_06_pusat_laporan.png', 'Gambar 3.12 Tampilan Pusat Laporan Eksekutif dan Panel Filter', width_inches=5.2)
    
    add_p(doc, "Tata letak siap cetak dokumen dinas resmi yang telah disesuaikan dengan standar tata naskah dinas Pemerintah Kabupaten Purbalingga berbasis *CSS Print Media* disajikan pada Gambar 3.13.", bold_prefix="g. Pratinjau Dokumen Cetak Ber-Kop Resmi Pemkab Purbalingga\n", indent=0)
    add_image_with_caption(doc, 'ss_07_cetak_kop_resmi.png', 'Gambar 3.13 Tampilan Pratinjau Dokumen Cetak Ber-Kop Resmi Pemkab Purbalingga', width_inches=5.2)
    
    add_p(doc, "Modul tata kelola data master unit kerja operasional dinas yang dikhususkan bagi hak akses Super Admin untuk menambah atau mengubah nomenklatur bidang disajikan pada Gambar 3.14.", bold_prefix="h. Manajemen Master Unit Kerja Dinas\n", indent=0)
    add_image_with_caption(doc, 'ss_08_master_unit_kerja.png', 'Gambar 3.14 Tampilan Manajemen Master Unit Kerja Dinas', width_inches=5.2)
    
    add_p(doc, "Fasilitas pengelolaan akun pengguna, penentuan peran (*role*), penugasan unit kerja, aktivasi akun, dan fitur pengaturan ulang kata sandi disajikan pada Gambar 3.15.", bold_prefix="i. Manajemen Akun Pengguna & Hak Akses (RBAC)\n", indent=0)
    add_image_with_caption(doc, 'ss_09_manajemen_pengguna.png', 'Gambar 3.15 Tampilan Manajemen Akun Pengguna & Hak Akses (RBAC)', width_inches=5.2)
    
    add_p(doc, "Fasilitas pencadangan data mandiri ke dalam format berkas *snapshot* JSON dan modul pemulihan data (*restore*) guna mitigasi risiko kehilangan data disajikan pada Gambar 3.16.", bold_prefix="j. Modul Pencadangan Mandiri (*Backup*) & Pemulihan Basis Data\n", indent=0)
    add_image_with_caption(doc, 'ss_10_backup_dan_restore.png', 'Gambar 3.16 Tampilan Modul Pencadangan Mandiri (Backup) & Pemulihan Basis Data', width_inches=5.2)

    add_heading_3(doc, "5. Pengujian Sistem (Testing)")
    add_p(doc, "Guna menjamin mutu perangkat lunak serta memastikan seluruh modul berjalan sesuai spesifikasi kebutuhan yang telah ditetapkan, dilakukan pengujian perangkat lunak menggunakan metode *Black-Box Testing* (Pressman & Maxim, 2020). Pengujian difokuskan pada pengamatan masukan (*input*) dan keluaran (*output*) antarmuka tanpa memeriksa baris kode internal.")
    add_p(doc, "Pengujian dilaksanakan melalui 13 tabel kasus uji fungsional yang mencakup total 22 butir skenario pengujian spesifik, sebagaimana disajikan pada Tabel 3.8 sampai dengan Tabel 3.20.")

    # 13 Testing Tables
    def add_test_table(caption, rows):
        h = ['No.', 'Skenario Uji', 'Prosedur Masukan', 'Hasil yang Diharapkan', 'Status']
        a = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
        w = [0.4, 1.8, 2.0, 2.2, 0.8]
        add_open_table(doc, caption, h, rows, a, w)

    add_test_table("Tabel 3.8 Pengujian Autentikasi Pengguna (Login & Logout)", [
        ['1', 'Login sandi valid', 'Input surel & sandi benar', 'Sistem berhasil login & arahkan', 'Valid'],
        ['2', 'Login sandi salah', 'Input sandi tidak cocok', 'Notifikasi error & akses ditolak', 'Valid'],
        ['3', 'Logout akun', 'Klik tombol Logout', 'Sesi berakhir & kembali login', 'Valid']
    ])

    add_test_table("Tabel 3.9 Pengujian Dashboard Eksekutif & Pemantauan Data", [
        ['1', 'Muat metrik total', 'Buka halaman dashboard', 'Kartu ringkasan data tampil sinkron', 'Valid'],
        ['2', 'Filter tahun dasbor', 'Ganti dropdown tahun', 'Grafik analitik berubah sesuai', 'Valid']
    ])

    add_test_table("Tabel 3.10 Pengujian Tambah Data Sektoral oleh Admin Bidang", [
        ['1', 'Input form lengkap', 'Isi semua field & URL Drive', 'Data tersimpan ke Supabase', 'Valid'],
        ['2', 'Validasi field kosong', 'Kosongkan judul & submit', 'Validasi form muncul & ditahan', 'Valid']
    ])

    add_test_table("Tabel 3.11 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja", [
        ['1', 'Auto-lock admin unit', 'Buka form sebagai Admin PPTK', 'Dropdown unit terkunci (disabled)', 'Valid'],
        ['2', 'Super admin bebas', 'Buka form sebagai Super Admin', 'Dropdown unit dapat dipilih bebas', 'Valid']
    ])

    add_test_table("Tabel 3.12 Pengujian Akses Tautan Data Dukung Google Drive", [
        ['1', 'Klik tautan drive', 'Klik ikon Drive di tabel', 'Tab baru membuka berkas bukti', 'Valid'],
        ['2', 'Tautan kosong', 'Data tanpa tautan bukti', 'Tombol dinonaktifkan', 'Valid']
    ])

    add_test_table("Tabel 3.13 Pengujian Ubah dan Hapus Data Sektoral", [
        ['1', 'Ubah nilai capaian', 'Edit angka pada modal edit', 'Data di Supabase terbarui instan', 'Valid'],
        ['2', 'Hapus rekaman data', 'Klik hapus & konfirmasi', 'Baris data terhapus permanen', 'Valid']
    ])

    add_test_table("Tabel 3.14 Pengujian Pencarian dan Penyaringan Data (Filter)", [
        ['1', 'Pencarian kata kunci', 'Ketik kata kunci di search', 'Tabel menyaring baris cocok', 'Valid'],
        ['2', 'Filter unit kerja', 'Pilih unit Balai Latihan', 'Data terfilter khusus unit BLK', 'Valid']
    ])

    add_test_table("Tabel 3.15 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)", [
        ['1', 'Klik ekspor Excel', 'Klik tombol Ekspor Excel', 'Berkas .xlsx terunduh otomatis', 'Valid']
    ])

    add_test_table("Tabel 3.16 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga", [
        ['1', 'Pratinjau cetak dinas', 'Klik tombol Cetak Laporan', 'Pratinjau cetak kop surat rapi', 'Valid']
    ])

    add_test_table("Tabel 3.17 Pengujian Manajemen Master Unit Kerja (Super Admin)", [
        ['1', 'Tambah master unit', 'Input unit kerja baru', 'Daftar unit bertambah aktif', 'Valid']
    ])

    add_test_table("Tabel 3.18 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)", [
        ['1', 'Ubah status aktif', 'Klik toggle aktif/nonaktif', 'Status akun langsung terblokir', 'Valid'],
        ['2', 'Reset kata sandi', 'Ketik sandi baru & simpan', 'Sandi terenkripsi baru aktif', 'Valid']
    ])

    add_test_table("Tabel 3.19 Pengujian Backup & Restore Basis Data (Super Admin)", [
        ['1', 'Ekspor snapshot JSON', 'Klik tombol Backup Data', 'Berkas cadangan JSON terunduh', 'Valid']
    ])

    add_test_table("Tabel 3.20 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)", [
        ['1', 'Perekaman transaksi', 'Eksekusi operasi CRUD data', 'Aktivitas tercatat di tabel log', 'Valid']
    ])

    add_p(doc, "Berdasarkan hasil eksekusi pengujian pada keseluruhan 13 tabel kasus uji fungsionalitas di atas, seluruh butir uji menunjukkan status 100% Valid. Sistem terbukti andal, proses ekspor data rekapitulasi berhasil dipangkas dari sebelumnya 3–5 hari kerja menjadi kurang dari lima detik, dan sistem dinyatakan siap untuk dioperasikan secara penuh oleh seluruh bidang di lingkungan dinas.")

    add_heading_2(doc, "B. Kendala Pelaksanaan dan Solusinya")
    add_p(doc, "Selama pelaksanaan Kerja Praktik dan rekayasa perangkat lunak SatuNaker di Kantor DINPERINNAKER Kabupaten Purbalingga, penulis mengidentifikasi lima kendala teknis dan operasional utama beserta langkah solusi penanganan yang diterapkan, sebagaimana disajikan pada Tabel 3.21.")
    
    t3_21_headers = ['No.', 'Aspek Kendala', 'Deskripsi Kendala Lapangan', 'Solusi Rekayasa yang Diterapkan']
    t3_21_rows = [
        ['1', 'Inkonsistensi Format Data Mentah (*Legacy*)', 'Data sektoral lama tersebar di lembar sebar (*Excel*) tiap bidang tanpa standar kolom seragam.', 'Standardisasi skema basis data terpusat dengan atribut baku pada PostgreSQL Supabase.'],
        ['2', 'Kapasitas Server Berkas Bukti Fisik', 'Keterbatasan kuota storage basis data untuk menampung arsip PDF fisik berukuran besar.', 'Integrasi tautan URL Google Drive resmi dinas untuk verifikasi instan tanpa beban storage server.'],
        ['3', 'Kesalahan Input Lintas Unit Kerja', 'Potensi operator salah memilih unit kerja saat mengisi formulir data sektoral.', 'Implementasi fitur *auto-lock* pilihan unit kerja berbasis token sesi login pengguna.'],
        ['4', 'Standar Kop Surat Kedinasan yang Ketat', 'Pencetakan web standar tidak memenuhi format tata naskah dinas resmi Pemkab.', 'Penerapan *CSS Media Print* khusus dengan tata letak kop resmi Pemerintah Kabupaten Purbalingga.'],
        ['5', 'Mitigasi Kehilangan Data Operasional', 'Ketiadaan mekanisme backup mandiri bagi staf dinas non-administrator SQL tingkat lanjut.', 'Penyediaan modul *Backup & Restore* mandiri berbasis *snapshot* berkas JSON satu kali klik.']
    ]
    t3_21_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    t3_21_widths = [0.4, 1.8, 2.5, 2.5]
    add_open_table(doc, "Tabel 3.21 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa", t3_21_headers, t3_21_rows, t3_21_aligns, t3_21_widths)

    # =========================================================================
    # 11. BAB IV: PENUTUP
    # =========================================================================
    add_heading_1(doc, "BAB IV\nPENUTUP")
    add_heading_2(doc, "A. Kesimpulan")
    add_p(doc, "Berdasarkan seluruh rangkaian kegiatan Kerja Praktik yang telah dilaksanakan di Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) Kabupaten Purbalingga, mulai dari observasi lapangan, analisis kebutuhan, perancangan, pengembangan sistem, hingga pengujian perangkat lunak, dapat ditarik beberapa kesimpulan utama sebagai berikut:")
    add_p(doc, "1. Telah berhasil dirancang dan dibangun Website Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker) sebagai portal integrasi data statistik sektoral terpadu (*Single Source of Truth*) berbasis web modern dengan kerangka kerja Next.js 16 (*App Router*), TypeScript, Tailwind CSS v4, dan basis data PostgreSQL pada cloud Supabase.", indent=0.5)
    add_p(doc, "2. Sistem SatuNaker berhasil mengatasi permasalahan fragmentasi data (*data silo*) antar-bidang dengan menyatukan aliran pencatatan data dari 7 (tujuh) unit kerja dinas (HIJTK, PPTK, Industri, Renkeu, Umpeg, UPTD BLK, dan UPTD PILOG) ke dalam satu basis data relasional yang terstruktur dan aman.", indent=0.5)
    add_p(doc, "3. Penerapan sistem hak akses berbasis peran (*Role-Based Access Control* / RBAC) yang dilengkapi fitur penguncian otomatis (*auto-lock*) unit kerja pada formulir input Admin Bidang terbukti efektif mencegah terjadinya kekeliruan penginputan data lintas unit kerja.", indent=0.5)
    add_p(doc, "4. Integrasi data dukung bukti fisik menggunakan tautan Google Drive resmi dinas terbukti mampu menghemat kapasitas penyimpanan server basis data secara signifikan sekaligus mempercepat proses verifikasi keabsahan dokumen bukti fisik digital.", indent=0.5)
    add_p(doc, "5. Pengujian fungsionalitas sistem menggunakan metode *Black-Box Testing* pada 13 tabel kasus uji yang mencakup 22 butir skenario pengujian menghasilkan tingkat keberhasilan 100% valid, serta berhasil memangkas waktu penyusunan laporan rekapitulasi data sektoral dinas dari semula 3–5 hari kerja menjadi kurang dari lima detik.", indent=0.5)

    add_heading_2(doc, "B. Saran")
    add_p(doc, "Guna pengembangan sistem informasi SatuNaker yang lebih berkelanjutan dan berdaya guna di masa mendatang, penulis menyampaikan beberapa saran konstruktif sebagai berikut:")
    add_p(doc, "1. Untuk Instansi Mitra (DINPERINNAKER Kabupaten Purbalingga):\n"
               "   a. Perlu diterbitkan Surat Edaran atau Standar Operasional Prosedur (SOP) internal dari Kepala Dinas yang mewajibkan seluruh unit kerja untuk melakukan penginputan dan pembaruan data secara periodik setiap akhir bulan atau triwulan.\n"
               "   b. Menyelenggarakan bimbingan teknis (*training of trainers*) secara berkala bagi staf operator baru di masing-masing bidang kerja guna menjamin keberlanjutan pemanfaatan sistem.\n"
               "   c. Menjadwalkan pengunduhan cadangan data (*backup snapshot* JSON) secara rutin setiap bulan sebagai arsip fisik dinas mandiri melengkapi *automated cloud backup* Supabase.", indent=0.5)
    add_p(doc, "2. Untuk Pengembangan Sistem SatuNaker Selanjutnya:\n"
               "   a. Mengembangkan antarmuka pemrograman aplikasi terbuka (*Open API*) berbasis G2G (*Government to Government*) yang aman guna memfasilitasi interoperabilitas dua arah dengan sistem BPS Purbalingga Satu Data dan portal Satu Data Kabupaten pada Bappelitbangda.\n"
               "   b. Menambahkan modul *Spatial Mapping* (Sistem Informasi Geografis / GIS) untuk memetakan sebaran lokasi sentra industri knalpot PILOG, pabrik rambut dan bulu mata palsu, serta sebaran pencari kerja di 18 kecamatan Kabupaten Purbalingga secara visual pada peta spasial interaktif.\n"
               "   c. Menerapkan fitur *Progressive Web App* (PWA) agar sistem dapat dipasang langsung pada layar beranda ponsel pintar pimpinan dan operator dinas untuk kemudahan pemantauan *mobile*.", indent=0.5)
    add_p(doc, "3. Untuk Rekan Mahasiswa Kerja Praktik Selanjutnya:\n"
               "   a. Disarankan untuk mendalami konsep *Row-Level Security* (RLS) dan arsitektur *Server Components* pada Next.js sebelum melaksanakan proyek digitalisasi di instansi pemerintah.\n"
               "   b. Membangun komunikasi yang intensif dan santun bersama pembimbing lapangan serta staf instansi mitra guna memahami regulasi birokrasi dan tata naskah dinas resmi pemerintah daerah secara komprehensif.", indent=0.5)

    # =========================================================================
    # 12. DAFTAR PUSTAKA
    # =========================================================================
    add_heading_1(doc, "DAFTAR PUSTAKA")
    pustaka_list = [
        "Badan Pusat Statistik Kabupaten Purbalingga. (2024). Kabupaten Purbalingga dalam Angka 2024. Purbalingga: BPS Kabupaten Purbalingga. https://purbalinggakab.bps.go.id",
        "Connolly, T. M., & Begg, C. E. (2015). Database Systems: A Practical Approach to Design, Implementation, and Management (6th ed.). Pearson Education.",
        "Hidayat, R., & Rahmawati, E. (2022). Implementasi Kebijakan Satu Data Indonesia pada Tingkat Pemerintah Daerah. Jurnal Tata Kelola Publik Indonesia, 10(2), 115–128. https://doi.org/10.22146/jtpi.v10i2.71452",
        "Jogiyanto, H. M. (2018). Analisis dan Desain Sistem Informasi: Pendekatan Terstruktur Teori dan Praktik Aplikasi Bisnis (Edisi Keempat). Penerbit Andi.",
        "Martin, R. C. (2018). Clean Architecture: A Craftsman's Guide to Software Structure and Design. Prentice Hall.",
        "Next.js Documentation. (2026). Next.js App Router Architecture, Server Components, and Data Fetching Paradigm. Vercel Inc. https://nextjs.org/docs",
        "Nugroho, A. (2020). Rekayasa Perangkat Lunak Berorientasi Objek dengan Metode USDP. Informatika Bandung.",
        "Pemerintah Kabupaten Purbalingga. (2021). Peraturan Daerah Kabupaten Purbalingga Nomor 5 Tahun 2021 tentang Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga Tahun 2021-2026. Bagian Hukum Setda Kabupaten Purbalingga.",
        "Pratama, A. B., & Widiastuti, N. (2024). Pengembangan Sistem Satu Data Sektoral Menggunakan Pendekatan Role-Based Access Control dan Framework Next.js. Jurnal Rekayasa Komputer dan Informatika, 8(1), 45–56. https://doi.org/10.31294/jrki.v8i1.18921",
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "Republik Indonesia. (2019). Peraturan Presiden Republik Indonesia Nomor 39 Tahun 2019 tentang Satu Data Indonesia. Lembaran Negara Republik Indonesia Tahun 2019 Nomor 112. Kementerian Sekretariat Negara.",
        "Saputra, D. A., & Handayani, T. (2023). Penerapan Model Waterfall dalam Pembangunan Sistem Informasi Pelayanan Dinas Ketenagakerjaan Berbasis Web. Jurnal Sistem Informasi dan Teknologi Komputer, 7(3), 201–212.",
        "Sommerville, I. (2019). Software Engineering (10th ed.). Pearson Education Limited.",
        "Supabase Documentation. (2026). PostgreSQL Database, Row Level Security Policies, and Storage Engine. Supabase Pte. Ltd. https://supabase.com/docs",
        "Tailwind Labs Inc. (2026). Tailwind CSS: Utility-First CSS Framework. https://tailwindcss.com/docs"
    ]
    for p_item in pustaka_list:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.line_spacing = 1.15
        p_p.paragraph_format.space_before = Pt(3)
        p_p.paragraph_format.space_after = Pt(3)
        p_p.paragraph_format.first_line_indent = Inches(-0.5)
        p_p.paragraph_format.left_indent = Inches(0.5)
        p_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        # Italicize title or journal name
        r = p_p.add_run(p_item)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)

    # =========================================================================
    # 13. LAMPIRAN
    # =========================================================================
    add_heading_1(doc, "LAMPIRAN")
    
    add_heading_2(doc, "Lampiran 1: Surat Keterangan Selesai Kerja Praktik")
    add_p(doc, "Dokumen resmi Surat Keterangan Telah Menyelesaikan Kerja Praktik Nomor: 560/KP-DINPERINNAKER/XI/2026 yang diterbitkan oleh Dinas Perindustrian dan Tenaga Kerja Kabupaten Purbalingga pada tanggal 13 November 2026 yang ditandatangani oleh Kepala Dinas Bapak Johan Arifin, S.Sos., M.Si.")
    
    add_heading_2(doc, "Lampiran 2: Lembar Persetujuan Seminar Kerja Praktik")
    add_p(doc, "Formulir persetujuan pelaksanaan Seminar Kerja Praktik yang telah ditandatangani secara resmi oleh Dosen Pembimbing KP (Bapak Elindra Ambar Pambudi, S.T., M.Kom.) dan Pembimbing Lapangan Dinas.")
    
    add_heading_2(doc, "Lampiran 3: Logbook Catatan Aktivitas Harian Mahasiswa Magang")
    add_p(doc, "Matriks rekapitulasi pelaksanaan aktivitas harian selama 33 hari kerja aktif (1 Oktober 2026 sampai dengan 13 November 2026) di lingkungan Kantor DINPERINNAKER Kabupaten Purbalingga:")
    
    t_log_headers = ['Minggu', 'Rentang Tanggal', 'Fokus Aktivitas dan Progres Capaian Proyek', 'Paraf Mitra']
    t_log_rows = [
        ['M-1', '1 - 3 Okt 2026', 'Orientasi lingkungan dinas, pengenalan pejabat struktural, dan observasi awal aliran data 7 unit kerja.', 'Tervalidasi'],
        ['M-2', '6 - 10 Okt 2026', 'Wawancara mendalam dengan Admin Bidang HIJTK, PPTK, Industri, BLK, PILOG, Renkeu, dan Umpeg.', 'Tervalidasi'],
        ['M-3', '13 - 17 Okt 2026', 'Identifikasi permasalahan data silo dan spesifikasi kebutuhan fungsional (RBAC 3 tingkat peran).', 'Tervalidasi'],
        ['M-4', '20 - 24 Okt 2026', 'Perancangan arsitektur basis data relasional (ERD) dan skema tabel di PostgreSQL Supabase Cloud.', 'Tervalidasi'],
        ['M-5', '27 - 31 Okt 2026', 'Pengodean front-end Next.js 16 (App Router), form auto-lock unit, dan integrasi Google Drive data dukung.', 'Tervalidasi'],
        ['M-6', '3 - 7 Nov 2026', 'Pengembangan modul ekspor spreadsheet Excel, CSS Print Media kop resmi Pemkab, dan backup restore.', 'Tervalidasi'],
        ['M-7', '10 - 13 Nov 2026', 'Pengujian Black-Box fungsionalitas sistem (13 tabel pengujian, 22 skenario) dan serah terima sistem.', 'Tervalidasi']
    ]
    t_log_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    t_log_widths = [0.8, 1.5, 3.8, 1.1]
    add_open_table(doc, "Tabel Lampiran 3.1 Rekapitulasi Catatan Aktivitas Mingguan Kerja Praktik", t_log_headers, t_log_rows, t_log_aligns, t_log_widths)

    add_heading_2(doc, "Lampiran 4: Dokumentasi Kegiatan Magang dan Album Tangkapan Layar")
    add_p(doc, "Dokumentasi pelaksanaan kerja praktik meliputi observasi lapangan bersama pembimbing lapangan dinas, diskusi penyusunan arsitektur sistem SatuNaker, pengujian antarmuka bersama operator bidang, dan penyerahan sistem.")

    # Save to OUT_DOCX and ART_DOCX
    print(f"Saving final report to: {OUT_DOCX}")
    doc.save(OUT_DOCX)
    print("Saved OUT_DOCX successfully!")
    
    print(f"Copying to artifact path: {ART_DOCX}")
    shutil.copyfile(OUT_DOCX, ART_DOCX)
    print("Saved ART_DOCX successfully!")

if __name__ == '__main__':
    build_complete_report()
