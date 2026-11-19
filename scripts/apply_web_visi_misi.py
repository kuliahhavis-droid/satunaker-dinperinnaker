# -*- coding: utf-8 -*-
"""
Script to apply the EXACT Visi and Misi from official website:
https://dinperinnaker.purbalinggakab.go.id/sample-page/
"""
import os
import shutil
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_master_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    print("Updating Master Docx with official website Visi Misi:", path)
    doc = docx.Document(path)
    
    idx_d = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == 'D. Visi dan Misi':
            idx_d = i
            break
            
    idx_bab3 = None
    for j in range(idx_d + 1, len(doc.paragraphs)):
        if 'BAB III' in doc.paragraphs[j].text:
            idx_bab3 = j
            break
            
    print(f"Subbab D at {idx_d}, BAB III at {idx_bab3}")
    
    # Remove existing paragraphs between idx_d and idx_bab3
    while idx_bab3 > idx_d + 1:
        p_to_del = doc.paragraphs[idx_d + 1]
        p_to_del._p.getparent().remove(p_to_del._p)
        idx_bab3 -= 1
        
    p_bab3 = doc.paragraphs[idx_bab3]
    
    paragraphs_to_add = [
        # (text, bold_prefix, italic, indent)
        ("Visi merupakan rumusan umum mengenai keadaan yang diinginkan pada akhir periode perencanaan dengan mengacu pada RPJMD Kabupaten Purbalingga. Telaahan Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih untuk melihat sinkronisasi arah kebijakan pembangunan. Dinas Tenaga Kerja (Dinas Perindustrian dan Tenaga Kerja) Kabupaten Purbalingga yang merupakan salah satu Organisasi Perangkat Daerah Kabupaten Purbalingga dalam menjalankan tugas pokok dan fungsinya diarahkan untuk mendukung pencapaian Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih.", "1. Visi\n", False, 0.5),
        ("“PURBALINGGA YANG MANDIRI DAN BERDAYA SAING MENUJU MASYARAKAT SEJAHTERA YANGBERAKHLAK MULIA”.", "Adapun Visi Kepala Daerah dan Wakil Kepala Daerah terpilih Kabupaten Purbalingga adalah ", True, 0.5),
        ("Sebagai penjabaran dari Visi Kabupaten Purbalingga, maka Pemerintahan Kabupaten Purbalingga menetapkan misi. Misi merupakan sesuatu yang harus diemban atau dilaksanakan oleh suatu organisasi dalam merumuskan upaya-upaya untuk mewujudkan visi tersebut. Peraturan Daerah Kabupaten Purbalingga telah menetapkan Peraturan Daerah Kabupaten Purbalingga Nomor 05 Tahun 2021 tentang Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga tahun 2021-2026 meliputi:", "2. Misi\n", False, 0.5),
        ("Menyelenggarakan pemerintahan yang profesional, efisien, efektif, bersih dan demokratis, sehingga mampu memberikan pelayanan secara prima kepada masyarakat;", "1. ", False, 0.5),
        ("Mendorong kehidupan masyarakat religius yang beriman dan bertaqwa kehadirat Allah SWT serta mengembangkan paham kebangsaan guna mewujudkan rasa aman dan tenteram dalam masyarakat yang berdasar pada realitas kebhinekaan;", "2. ", False, 0.5),
        ("Mengupayakan kecukupan kebutuhan pokok manusia utamanya pangan dan papan secara layak;", "3. ", False, 0.5),
        ("Meningkatkan kualitas sumberdaya manusia utamanya melalui peningkatan derajat pendidikan dan derajat kesehatan masyarakat;", "4. ", False, 0.5),
        ("Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya industri pengolahan dan manufaktur, perdagangan, jasa, pariwisata, industri kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja;", "5. ", False, 0.5),
        ("Meningkatkan pembangunan berbasis desa dan kawasan perdesaan melalui optimalisasi penyelenggaraan pemerintah desa, pembangunan pembinaan kemasyarakatan dan pemberdayaan masyarakat desa;", "6. ", False, 0.5),
        ("Meningkatkan kualitas dan kuantitas sarana dan prasarana wilayah/infrastruktur dengan tetap memperhatikan kelestarian lingkungan.", "7. ", False, 0.5),
        ("Dari pernyataan misi tersebut, dapat disimpulkan misi yang berkaitan di mana pencapaiannya didukung secara langsung oleh Dinas Perindustrian dan Tenaga Kerja yaitu pada Misi Ke-5, yaitu: “Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya dalam industri pengolahan dan manufaktur, pertanian, perdagangan, jasa, pariwisata, UMKM dan ekonomi kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja”.", "", False, 0.5),
        ("Di samping Misi Ke-5, pengembangan Website Satu Data DINPERINNAKER (SatuNaker) dalam kerja praktik ini juga secara strategis mendukung pencapaian Misi Ke-1 (tata kelola pemerintahan yang profesional, efektif, bersih, dan akuntabel berbasis teknologi informasi) serta Misi Ke-4 (peningkatan kualitas sumber daya manusia dan tenaga kerja terampil melalui UPTD Balai Latihan Kerja).", "", False, 0.5)
    ]
    
    for body, prefix, italic, indent in paragraphs_to_add:
        new_p = p_bab3.insert_paragraph_before()
        new_p.paragraph_format.line_spacing = 2.0
        new_p.paragraph_format.space_before = Pt(0)
        new_p.paragraph_format.space_after = Pt(0)
        new_p.paragraph_format.first_line_indent = Inches(indent)
        new_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if prefix:
            r_pre = new_p.add_run(prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            if '1. Visi' in prefix or '2. Misi' in prefix:
                r_pre.bold = True
                
        r_body = new_p.add_run(body)
        r_body.font.name = 'Times New Roman'
        r_body.font.size = Pt(12)
        if italic:
            r_body.bold = True
            r_body.italic = True
            
    doc.save(path)
    print("Master Docx updated and saved!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

def update_template_docx():
    path = r'D:\Magang\sistem-satudata-dinperinnaker\document\TEMPLATE_LAPORAN_KP_TI_UMP.docx'
    print("Updating Template Docx:", path)
    doc = docx.Document(path)
    
    for p in doc.paragraphs:
        if 'Petunjuk Pengisian' in p.text and 'Visi dan Misi' in p.text:
            p.text = (
                "👉 [Petunjuk Pengisian]: Sajikan rumusan resmi Visi dan Misi RPJMD Kabupaten Purbalingga 2021-2026 "
                "sesuai laman resmi DINPERINNAKER (https://dinperinnaker.purbalinggakab.go.id/sample-page/) "
                "yang mencakup Visi daerah, 7 Misi lengkap, serta penegasan dukungan dinas pada Misi Ke-5 (pertumbuhan ekonomi "
                "industri manufaktur & lapangan kerja) dan Misi Ke-1 (tata kelola pemerintahan digital via SatuNaker)."
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
    print("Updating Bank Materi MD:", path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    web_text_md = """### D. Subbab D: Visi dan Misi Mitra
*(Sumber Resmi: Laman Portal DINPERINNAKER Kabupaten Purbalingga - https://dinperinnaker.purbalinggakab.go.id/sample-page/)*

> **1. Visi**  
> Visi merupakan rumusan umum mengenai keadaan yang diinginkan pada akhir periode perencanaan dengan mengacu pada RPJMD Kabupaten Purbalingga. Telaahan Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih untuk melihat sinkronisasi arah kebijakan pembangunan. Dinas Tenaga Kerja (Dinas Perindustrian dan Tenaga Kerja) Kabupaten Purbalingga yang merupakan salah satu Organisasi Perangkat Daerah Kabupaten Purbalingga dalam menjalankan tugas pokok dan fungsinya diarahkan untuk mendukung pencapaian Visi, Misi dan Program Kepala Daerah dan Wakil Kepala Daerah terpilih.  
>  
> Adapun Visi Kepala Daerah dan Wakil Kepala Daerah terpilih Kabupaten Purbalingga adalah:  
> **“PURBALINGGA YANG MANDIRI DAN BERDAYA SAING MENUJU MASYARAKAT SEJAHTERA YANGBERAKHLAK MULIA”**.  
>  
> **2. Misi**  
> Sebagai penjabaran dari Visi Kabupaten Purbalingga, maka Pemerintahan Kabupaten Purbalingga menetapkan misi. Misi merupakan sesuatu yang harus diemban atau dilaksanakan oleh suatu organisasi dalam merumuskan upaya-upaya untuk mewujudkan visi tersebut. Peraturan Daerah Kabupaten Purbalingga telah menetapkan Peraturan Daerah Kabupaten Purbalingga Nomor 05 Tahun 2021 tentang Rencana Pembangunan Jangka Menengah Daerah (RPJMD) Kabupaten Purbalingga tahun 2021-2026 meliputi:  
> 1. Menyelenggarakan pemerintahan yang profesional, efisien, efektif, bersih dan demokratis, sehingga mampu memberikan pelayanan secara prima kepada masyarakat;  
> 2. Mendorong kehidupan masyarakat religius yang beriman dan bertaqwa kehadirat Allah SWT serta mengembangkan paham kebangsaan guna mewujudkan rasa aman dan tenteram dalam masyarakat yang berdasar pada realitas kebhinekaan;  
> 3. Mengupayakan kecukupan kebutuhan pokok manusia utamanya pangan dan papan secara layak;  
> 4. Meningkatkan kualitas sumberdaya manusia utamanya melalui peningkatan derajat pendidikan dan derajat kesehatan masyarakat;  
> 5. Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya industri pengolahan dan manufaktur, perdagangan, jasa, pariwisata, industri kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja;  
> 6. Meningkatkan pembangunan berbasis desa dan kawasan perdesaan melalui optimalisasi penyelenggaraan pemerintah desa, pembangunan pembinaan kemasyarakatan dan pemberdayaan masyarakat desa;  
> 7. Meningkatkan kualitas dan kuantitas sarana dan prasarana wilayah/infrastruktur dengan tetap memperhatikan kelestarian lingkungan.  
>  
> Dari pernyataan misi tersebut, dapat disimpulkan misi yang berkaitan di mana pencapaiannya didukung secara langsung oleh Dinas Perindustrian dan Tenaga Kerja yaitu pada **Misi Ke-5**, yaitu:  
> *“Mempercepat pertumbuhan dan pemerataan ekonomi rakyat, dengan mendorong simpul-simpul perekonomian utamanya dalam industri pengolahan dan manufaktur, pertanian, perdagangan, jasa, pariwisata, UMKM dan ekonomi kreatif dengan tetap berorientasi pada kemitraan dan pengembangan potensi lokal serta didukung dengan penciptaan iklim kondusif untuk pengembangan usaha, investasi dan penciptaan lapangan kerja”*.  
>  
> Di samping Misi Ke-5, perancangan dan pembangunan Website Satu Data DINPERINNAKER (SatuNaker) pada kegiatan Kerja Praktik ini juga berkontribusi nyata dalam mewujudkan **Misi Ke-1** (penyelenggaraan tata kelola pemerintahan yang profesional, efektif, dan akuntabel berbasis teknologi informasi) serta **Misi Ke-4** (penguatan kualitas sumber daya manusia dan tenaga kerja terampil melalui unit pelatihan vokasi UPTD BLK)."""

    import re
    content = re.sub(r'### D\. Subbab D: Visi dan Misi Mitra.*?(?=---|\Z)', web_text_md + '\n\n', content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Bank Materi MD updated!")
    art_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\BANK_MATERI_LAPORAN_WEBSITE_SATUNAKER.md'
    shutil.copyfile(path, art_path)
    print("Copied to artifacts!")

if __name__ == '__main__':
    update_master_docx()
    update_template_docx()
    update_bank_materi_md()
    print("ALL DONE!")
