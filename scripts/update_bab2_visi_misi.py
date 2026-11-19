# -*- coding: utf-8 -*-
"""
Script to update Subbab D (Visi dan Misi) across:
1. Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx
2. TEMPLATE_LAPORAN_KP_TI_UMP.docx
3. BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md
"""
import os
import shutil
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_master_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    print("Updating Master Docx Visi Misi:", path)
    doc = docx.Document(path)
    
    # Locate Subbab D (Visi dan Misi)
    idx_d = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == 'D. Visi dan Misi':
            idx_d = i
            break
            
    if idx_d is None:
        print("Subbab D not found!")
        return

    # Delete old paragraphs between idx_d and BAB III
    # In master docx, P196 was 'D. Visi dan Misi', P197-P202 were the old text, P204 was 'BAB III'
    # Let's inspect paragraphs around idx_d
    print(f"Subbab D found at paragraph {idx_d}: '{doc.paragraphs[idx_d].text}'")
    
    # We want to replace paragraphs after idx_d up to BAB III with the complete 7 missions
    # Let's see the index of BAB III
    idx_bab3 = None
    for j in range(idx_d + 1, len(doc.paragraphs)):
        if 'BAB III' in doc.paragraphs[j].text:
            idx_bab3 = j
            break
            
    print(f"BAB III found at paragraph {idx_bab3}: '{doc.paragraphs[idx_bab3].text}'")
    
    # Target new text items:
    # 1. Paragraf pengantar
    # 2. Visi heading & teks
    # 3. Misi 7 butir lengkap
    # 4. Penjelasan mandat spesifik DINPERINNAKER
    
    p_intro = doc.paragraphs[idx_d + 1]
    p_intro.text = (
        "Sebagai organisasi perangkat daerah di lingkungan Pemerintah Kabupaten Purbalingga, "
        "Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) menyelaraskan seluruh program kerja, kegiatan, "
        "serta tugas pokok dan fungsinya guna mendukung pencapaian Visi dan Misi Rencana Pembangunan Jangka "
        "Menengah Daerah (RPJMD) Kabupaten Purbalingga Tahun 2021–2026 sebagaimana ditetapkan dalam Peraturan "
        "Daerah Kabupaten Purbalingga Nomor 5 Tahun 2021 (Pemerintah Kabupaten Purbalingga, 2021), yaitu:"
    )
    p_intro.paragraph_format.line_spacing = 2.0
    p_intro.paragraph_format.first_line_indent = Inches(0.5)
    p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_intro.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    p_visi_head = doc.paragraphs[idx_d + 2]
    p_visi_head.text = "1. Visi RPJMD Kabupaten Purbalingga Tahun 2021–2026:"
    p_visi_head.paragraph_format.line_spacing = 2.0
    p_visi_head.paragraph_format.first_line_indent = Inches(0)
    p_visi_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in p_visi_head.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    p_visi_body = doc.paragraphs[idx_d + 3]
    p_visi_body.text = "“Purbalingga yang Mandiri dan Berdaya Saing Menuju Masyarakat Sejahtera yang Berakhlak Mulia.”"
    p_visi_body.paragraph_format.line_spacing = 2.0
    p_visi_body.paragraph_format.first_line_indent = Inches(0.5)
    p_visi_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_visi_body.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        r.italic = True
        
    p_misi_head = doc.paragraphs[idx_d + 4]
    p_misi_head.text = "2. Misi RPJMD Kabupaten Purbalingga Tahun 2021–2026:"
    p_misi_head.paragraph_format.line_spacing = 2.0
    p_misi_head.paragraph_format.first_line_indent = Inches(0)
    p_misi_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in p_misi_head.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    p_misi_intro = doc.paragraphs[idx_d + 5]
    p_misi_intro.text = "Guna mewujudkan visi pembangunan daerah tersebut, dirumuskan 7 (tujuh) misi strategis Kabupaten Purbalingga sebagai berikut:"
    p_misi_intro.paragraph_format.line_spacing = 2.0
    p_misi_intro.paragraph_format.first_line_indent = Inches(0.5)
    p_misi_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_misi_intro.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    # We now have the remaining paragraphs before BAB III.
    # Let's see how many paragraphs exist between idx_d + 5 and idx_bab3
    curr_diff = idx_bab3 - (idx_d + 6)
    print("Existing paragraphs between idx_d+6 and idx_bab3:", curr_diff)
    
    # We want to insert:
    # 7 mission items (a s/d g)
    # 1 explanation paragraph: "Dari 7 misi RPJMD tersebut, DINPERINNAKER memiliki keterkaitan mandat langsung..."
    # 3 sub-points of Dinperinnaker's mandate (Misi 1, Misi 4, Misi 5)
    
    missions = [
        ("a. Misi Ke-1: ", "Menyelenggarakan pemerintahan yang profesional, efektif, inovatif, bersih, akuntabel, dan demokratis, sehingga mampu memberikan pelayanan secara prima kepada masyarakat."),
        ("b. Misi Ke-2: ", "Mendorong kehidupan masyarakat religius yang beriman dan bertakwa kepada Tuhan Yang Maha Esa, serta mengembangkan paham kebangsaan guna mewujudkan terciptanya rasa aman dan tenteram dalam kehidupan bermasyarakat, berbangsa, dan bernegara berdasarkan Pancasila dalam bingkai Negara Kesatuan Republik Indonesia (NKRI)."),
        ("c. Misi Ke-3: ", "Mengupayakan kecukupan kebutuhan pokok masyarakat, utamanya pangan dan papan secara layak."),
        ("d. Misi Ke-4: ", "Meningkatkan kualitas sumber daya manusia (SDM), utamanya melalui peningkatan derajat pendidikan, keterampilan kerja, dan derajat kesehatan masyarakat."),
        ("e. Misi Ke-5: ", "Mempercepat pertumbuhan dan pemerataan ekonomi masyarakat dengan mendorong simpul-simpul perekonomian, utamanya dalam industri pengolahan dan manufaktur, pertanian, perdagangan, jasa, pariwisata, UMKM, dan ekonomi kreatif, dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi, dan penciptaan lapangan kerja."),
        ("f. Misi Ke-6: ", "Meningkatkan pembangunan berbasis desa dan kawasan perdesaan melalui optimalisasi penyelenggaraan pemerintah desa, pembangunan, pembinaan kemasyarakatan, dan pemberdayaan masyarakat desa."),
        ("g. Misi Ke-7: ", "Meningkatkan kualitas dan kuantitas sarana dan prasarana wilayah / infrastruktur, dengan tetap memperhatikan kelestarian lingkungan.")
    ]
    
    mandat_intro = (
        "Dari 7 (tujuh) misi pembangunan daerah Kabupaten Purbalingga di atas, Dinas Perindustrian dan "
        "Tenaga Kerja (DINPERINNAKER) mengemban mandat tugas pokok dan fungsi strategis yang berkontribusi "
        "langsung pada 3 (tiga) misi utama, yaitu:"
    )
    
    mandat_points = [
        ("1) Misi Ke-1 (Tata Kelola Pemerintahan & E-Government): ", 
         "Diwujudkan melalui transparansi data statistik sektoral, akuntabilitas birokrasi, serta digitalisasi pelayanan publik. Pengembangan Website Satu Data DINPERINNAKER (SatuNaker) berkontribusi secara langsung pada misi ini dalam menyediakan simpul data tunggal (Single Source of Truth) berbasis teknologi informasi modern."),
        ("2) Misi Ke-4 (Peningkatan Kualitas SDM & Ketenagakerjaan): ", 
         "Diwujudkan melalui program peningkatan keterampilan vokasi pencari kerja berbasis kompetensi (competency-based training) yang diselenggarakan oleh UPTD Balai Latihan Kerja (BLK) guna menghasilkan tenaga kerja terampil yang terserap di dunia usaha dan dunia industri (DUDI)."),
        ("3) Misi Ke-5 (Pertumbuhan Ekonomi Industri & Lapangan Kerja): ", 
         "Diwujudkan melalui pembinaan dan fasilitasi legalitas Industri Kecil dan Menengah (IKM) oleh Bidang Industri, bimbingan teknologi manufaktur dan sarana uji emisi gas buang oleh UPTD Pengembangan Industri Logam (PILOG), fasilitasi bursa kerja (job fair) dan penempatan tenaga kerja oleh Bidang PPTK, serta pengawasan hubungan industrial yang harmonis dan jaminan sosial tenaga kerja oleh Bidang HIJTK.")
    ]
    
    # We will remove old paragraphs from idx_d + 6 to idx_bab3, then insert the new paragraphs cleanly!
    # To do this safely in python-docx:
    # Remove paragraphs between idx_d+6 and idx_bab3
    while idx_bab3 > idx_d + 6:
        p_to_del = doc.paragraphs[idx_d + 6]
        p_to_del._p.getparent().remove(p_to_del._p)
        idx_bab3 -= 1
        
    # Now idx_bab3 is right at idx_d + 6!
    # Let's insert our paragraphs right before doc.paragraphs[idx_bab3]
    p_bab3 = doc.paragraphs[idx_bab3]
    
    for pre, text in missions:
        new_p = p_bab3.insert_paragraph_before()
        new_p.paragraph_format.line_spacing = 2.0
        new_p.paragraph_format.first_line_indent = Inches(0.5)
        new_p.paragraph_format.space_before = Pt(0)
        new_p.paragraph_format.space_after = Pt(0)
        new_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = new_p.add_run(pre)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.bold = True
        r2 = new_p.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        
    new_p_mandat = p_bab3.insert_paragraph_before()
    new_p_mandat.paragraph_format.line_spacing = 2.0
    new_p_mandat.paragraph_format.first_line_indent = Inches(0.5)
    new_p_mandat.paragraph_format.space_before = Pt(0)
    new_p_mandat.paragraph_format.space_after = Pt(0)
    new_p_mandat.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_m = new_p_mandat.add_run(mandat_intro)
    r_m.font.name = 'Times New Roman'
    r_m.font.size = Pt(12)
    
    for pre, text in mandat_points:
        new_p = p_bab3.insert_paragraph_before()
        new_p.paragraph_format.line_spacing = 2.0
        new_p.paragraph_format.first_line_indent = Inches(0.5)
        new_p.paragraph_format.space_before = Pt(0)
        new_p.paragraph_format.space_after = Pt(0)
        new_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = new_p.add_run(pre)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.bold = True
        
        # Italicize foreign words in text:
        import re
        tokens = re.split(r'(\*[^*]+\*|\bSingle Source of Truth\b|\bcompetency-based training\b|\bjob fair\b|\bE-Government\b)', text)
        for tok in tokens:
            if not tok:
                continue
            r = new_p.add_run(tok)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            if tok in ['Single Source of Truth', 'competency-based training', 'job fair', 'E-Government']:
                r.italic = True
                
    doc.save(path)
    print("Master Docx Visi Misi updated successfully!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

def update_template_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\TEMPLATE_LAPORAN_KP_TI_UMP.docx'
    print("Updating Template Docx Visi Misi:", path)
    doc = docx.Document(path)
    
    for p in doc.paragraphs:
        if 'Petunjuk Pengisian' in p.text and 'Visi dan Misi' in p.text:
            p.text = (
                "👉 [Petunjuk Pengisian]: Tuliskan Visi dan seluruh 7 Misi RPJMD Kabupaten Purbalingga 2021-2026 "
                "secara lengkap. Kemudian uraikan keterkaitan tugas pokok DINPERINNAKER pada Misi Ke-1 (tata kelola pemerintahan & SPBE/Satu Data), "
                "Misi Ke-4 (peningkatan SDM/vokasi BLK), dan Misi Ke-5 (pertumbuhan ekonomi industri manufaktur & kesempatan kerja)."
            )
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.italic = True
            break
            
    doc.save(path)
    print("Template Docx updated!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\TEMPLATE_LAPORAN_KP_TI_UMP.docx'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

def update_bank_materi_md():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    print("Updating Bank Materi MD Visi Misi:", path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_subbab_d = """### D. Subbab D: Visi dan Misi Mitra
*Penyelarasan dengan RPJMD Kabupaten Purbalingga 2021-2026:*

> Visi Dinperinnaker Kabupaten Purbalingga selaras dengan Visi Pembangunan Daerah dalam Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga Tahun 2021-2026, yaitu:  
> **"Purbalingga yang Mandiri dan Berdaya Saing Menuju Masyarakat Sejahtera yang Berakhlak Mulia."**
>
> Dalam mewujudkan visi tersebut, Dinperinnaker mengemban Misi Pembangunan Daerah, khususnya:
> 1. **Misi ke-2:** "Mendorong pertumbuhan ekonomi daerah yang berbasis pada industri, pertanian, dan pariwisata yang berwawasan lingkungan serta berorientasi pada pemberdayaan potensi lokal."
> 2. **Misi ke-3:** "Meningkatkan kualitas sumber daya manusia melalui peningkatan mutu pendidikan, keterampilan kerja, dan derajat kesehatan masyarakat."
>
> Pengembangan sistem informasi **SatuNaker** secara langsung mendukung pencapaian misi tersebut dengan menyajikan basis data terpadu untuk memetakan serapan tenaga kerja, memonitor kepatuhan industri, dan mengevaluasi efektivitas pelatihan vokasi."""

    new_subbab_d = """### D. Subbab D: Visi dan Misi Mitra
*Penyelarasan dengan RPJMD Kabupaten Purbalingga 2021-2026:*

> Sebagai organisasi perangkat daerah, DINPERINNAKER menyelaraskan tugas pokok dan fungsinya guna mendukung pencapaian Visi dan Misi Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga Tahun 2021–2026 sebagaimana tertuang dalam Peraturan Daerah Kabupaten Purbalingga Nomor 5 Tahun 2021, yaitu:
>
> **1. Visi RPJMD Kabupaten Purbalingga Tahun 2021–2026:**  
> **"Purbalingga yang Mandiri dan Berdaya Saing Menuju Masyarakat Sejahtera yang Berakhlak Mulia."**
>
> **2. Misi RPJMD Kabupaten Purbalingga Tahun 2021–2026 (7 Misi Lengkap):**  
> a. **Misi Ke-1:** Menyelenggarakan pemerintahan yang profesional, efektif, inovatif, bersih, akuntabel, dan demokratis, sehingga mampu memberikan pelayanan secara prima kepada masyarakat.  
> b. **Misi Ke-2:** Mendorong kehidupan masyarakat religius yang beriman dan bertakwa kepada Tuhan Yang Maha Esa, serta mengembangkan paham kebangsaan guna mewujudkan terciptanya rasa aman dan tenteram dalam kehidupan bermasyarakat, berbangsa, dan bernegara berdasarkan Pancasila dalam bingkai Negara Kesatuan Republik Indonesia (NKRI).  
> c. **Misi Ke-3:** Mengupayakan kecukupan kebutuhan pokok masyarakat, utamanya pangan dan papan secara layak.  
> d. **Misi Ke-4:** Meningkatkan kualitas sumber daya manusia (SDM), utamanya melalui peningkatan derajat pendidikan, keterampilan kerja, dan derajat kesehatan masyarakat.  
> e. **Misi Ke-5:** Mempercepat pertumbuhan dan pemerataan ekonomi masyarakat dengan mendorong simpul-simpul perekonomian, utamanya dalam industri pengolahan dan manufaktur, pertanian, perdagangan, jasa, pariwisata, UMKM, dan ekonomi kreatif, dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi, dan penciptaan lapangan kerja.  
> f. **Misi Ke-6:** Meningkatkan pembangunan berbasis desa dan kawasan perdesaan melalui optimalisasi penyelenggaraan pemerintah desa, pembangunan, pembinaan kemasyarakatan, dan pemberdayaan masyarakat desa.  
> g. **Misi Ke-7:** Meningkatkan kualitas dan kuantitas sarana dan prasarana wilayah / infrastruktur, dengan tetap memperhatikan kelestarian lingkungan.
>
> **Keterkaitan Mandat Tugas Pokok DINPERINNAKER Kabupaten Purbalingga:**  
> Dari 7 (tujuh) misi pembangunan daerah di atas, DINPERINNAKER Kabupaten Purbalingga mengemban mandat tugas pokok yang berkontribusi langsung pada 3 (tiga) misi utama:  
> 1. **Misi Ke-1 (*E-Government* & Akuntabilitas):** Diwujudkan melalui transparansi data statistik sektoral dan digitalisasi sistem kerja. Pembangunan Website Satu Data (SatuNaker) menjadi simpul data tunggal (*Single Source of Truth*) guna mendukung tata kelola data pemerintahan daerah yang akuntabel.  
> 2. **Misi Ke-4 (Kualitas SDM & Ketenagakerjaan):** Diwujudkan melalui pelatihan vokasi berbasis kompetensi (*competency-based training*) di UPTD Balai Latihan Kerja (BLK) untuk mencetak tenaga kerja terampil dan bersertifikasi.  
> 3. **Misi Ke-5 (Pertumbuhan Industri & Lapangan Kerja):** Diwujudkan melalui pembinaan legalitas IKM oleh Bidang Industri, bimbingan manufaktur logam knalpot oleh UPTD PILOG, fasilitasi penempatan tenaga kerja dan bursa kerja (*job fair*) oleh Bidang PPTK, serta pengawasan hubungan industrial oleh Bidang HIJTK."""

    if old_subbab_d in content:
        content = content.replace(old_subbab_d, new_subbab_d)
    else:
        # Fallback regex replace for Subbab D
        import re
        content = re.sub(r'### D\. Subbab D: Visi dan Misi Mitra.*?(?=---|\Z)', new_subbab_d + '\n\n', content, flags=re.DOTALL)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Bank Materi MD Visi Misi updated!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

if __name__ == '__main__':
    update_master_docx()
    update_template_docx()
    update_bank_materi_md()
    print("ALL VISI MISI UPDATES DONE!")
