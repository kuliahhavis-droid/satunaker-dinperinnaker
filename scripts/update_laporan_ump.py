import os
import shutil
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOC_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx"
BACKUP_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final_Backup.docx"

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

def populate_table(table, headers, data, col_widths, col_alignments):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Format header row
    for col_idx, h in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        cell.width = col_widths[col_idx]
        format_cell(cell, h, bold=True, align=col_alignments[col_idx], font_size=Pt(10))
        
    # Populate data rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            is_num_col = (col_idx == 0)
            align = col_alignments[col_idx]
            format_cell(cell, str(val), bold=is_num_col, align=align, font_size=Pt(10))
            
    set_academic_table_borders(table)

def main():
    print("Opening document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)
    
    # ----------------------------------------------------
    # 1. Update Lembar Pengesahan: Table 4 (Penguji placeholder)
    # ----------------------------------------------------
    print("Updating Halaman Pengesahan...")
    t4 = doc.tables[3] # Table 4
    # t4.rows[0] is ['Pembimbing,', 'Penguji,']
    # t4.rows[1] is ['Elindra Ambar Pambudi...', 'Ermadi Satriya Wijaya...']
    cell_penguji = t4.rows[1].cells[1]
    cell_penguji.text = ""
    p1 = cell_penguji.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(40) # Space for signature
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.0
    r1 = p1.add_run("......................................................\nNIK. ........................")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True
    
    # ----------------------------------------------------
    # 2. Update Kata Pengantar Paragraph 32 (Dosen Penguji)
    # ----------------------------------------------------
    for p in doc.paragraphs[:40]:
        if "Bapak Ermadi Satriya Wijaya" in p.text:
            p.text = "5. Bapak/Ibu Dosen Penguji Seminar Kerja Praktik yang telah memberikan masukan, evaluasi, dan koreksi membangun."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)
            print("Kata pengantar updated for Dosen Penguji.")
            
    # ----------------------------------------------------
    # 3. Update Bab I (Gambaran Umum Proyek): 7 unit kerja and remove Subbab E (Biaya)
    # ----------------------------------------------------
    for p in doc.paragraphs[140:175]:
        if "lima unit kerja" in p.text:
            p.text = "1. Sistem berfokus pada digitalisasi pencatatan data statistik sektoral pada seluruh unit kerja di lingkungan DINPERINNAKER Kabupaten Purbalingga (Hubungan Industrial dan Jamsostek [HIJTK], Penempatan Tenaga Kerja dan Transmigrasi [PPTK], Bidang Perindustrian, Subbag Perencanaan & Keuangan [Renkeu], Subbag Umum & Kepegawaian [Umpeg], UPTD Balai Latihan Kerja [BLK], serta UPTD Pengembangan Industri Logam [PILOG])."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)
            print("Bab I unit kerja updated to 7 units.")
            
    # Remove Table 7 (Tabel 1.2 Biaya)
    # Let's find Table 7 by checking header
    t_biaya = None
    for t in doc.tables:
        first_row = [c.text.strip() for c in t.rows[0].cells]
        if "Komponen Kebutuhan Proyek" in first_row:
            t_biaya = t
            break
    if t_biaya:
        t_biaya._element.getparent().remove(t_biaya._element)
        print("Table 1.2 (Biaya) removed successfully.")
        
    # Remove paragraphs related to Subbab E and Tabel 1.2
    paras_to_remove = []
    for p in doc.paragraphs[150:180]:
        if "E. Biaya Pelaksanaan Proyek" in p.text or "Rincian Estimasi Biaya Pelaksanaan Proyek" in p.text or "Pengembangan sistem SatuNaker dirancang dengan prinsip efisiensi anggaran" in p.text:
            paras_to_remove.append(p)
    for p in paras_to_remove:
        p._element.getparent().remove(p._element)
        print(f"Removed paragraph: {p.text[:40]}")
        
    # ----------------------------------------------------
    # 4. In DAFTAR ISI: Remove Subbab E
    # ----------------------------------------------------
    for p in doc.paragraphs[35:75]:
        if "E. Biaya Pelaksanaan Proyek" in p.text:
            p._element.getparent().remove(p._element)
            print("Removed E. Biaya Pelaksanaan Proyek from DAFTAR ISI.")
            break
            
    doc.save(DOC_PATH)
    print("Phase 1 saved.")

if __name__ == "__main__":
    main()
