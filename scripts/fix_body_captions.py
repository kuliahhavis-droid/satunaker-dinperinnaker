import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx"

doc = docx.Document(DOC_PATH)

print("Fixing body captions...")

# 1. Fix RBAC in body
for p in doc.paragraphs[220:235]:
    if "Matriks hak akses disajikan pada Tabel 3.3." in p.text:
        p.text = p.text.replace("Tabel 3.3.", "Tabel 3.6.")
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(12)
        print("Updated RBAC intro reference.")
    elif "Tabel 3.3 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)" in p.text:
        p.text = "Tabel 3.6 Matriks Hak Akses Pengguna Berdasarkan Peran (RBAC)"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(11)
        p.runs[0].font.bold = True
        print("Updated RBAC caption.")

# 2. Fix Testing intro and captions in body (paragraphs 290 to 330)
testing_caption_replacements = {
    "Tabel 3.8 Pengujian Autentikasi Pengguna (Login & Logout)": "Tabel 3.11 Pengujian Autentikasi Pengguna (Login & Logout)",
    "Tabel 3.9 Pengujian Dashboard Eksekutif & Pemantauan Data": "Tabel 3.12 Pengujian Dashboard Eksekutif & Pemantauan Data",
    "Tabel 3.10 Pengujian Tambah Data Sektoral oleh Admin Bidang": "Tabel 3.13 Pengujian Tambah Data Sektoral oleh Admin Bidang",
    "Tabel 3.11 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja": "Tabel 3.14 Pengujian Pembatasan Hak Akses & Auto-Lock Unit Kerja",
    "Tabel 3.12 Pengujian Akses Tautan Data Dukung Google Drive": "Tabel 3.15 Pengujian Akses Tautan Data Dukung Google Drive",
    "Tabel 3.13 Pengujian Ubah dan Hapus Data Sektoral": "Tabel 3.16 Pengujian Ubah dan Hapus Data Sektoral",
    "Tabel 3.14 Pengujian Pencarian dan Penyaringan Data (Filter)": "Tabel 3.17 Pengujian Pencarian dan Penyaringan Data (Filter)",
    "Tabel 3.15 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)": "Tabel 3.18 Pengujian Ekspor Data ke Microsoft Excel (.xlsx)",
    "Tabel 3.16 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga": "Tabel 3.19 Pengujian Cetak Dokumen Ber-Kop Resmi Pemkab Purbalingga",
    "Tabel 3.17 Pengujian Manajemen Master Unit Kerja (Super Admin)": "Tabel 3.20 Pengujian Manajemen Master Unit Kerja (Super Admin)",
    "Tabel 3.18 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)": "Tabel 3.21 Pengujian Manajemen Pengguna & Reset Sandi (Super Admin)",
    "Tabel 3.19 Pengujian Backup & Restore Basis Data (Super Admin)": "Tabel 3.23 Pengujian Backup & Restore Basis Data (Super Admin)",
    "Tabel 3.20 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)": "Tabel 3.22 Pengujian Pencatatan Log Aktivitas Pengguna (Audit Trail)",
    "Tabel 3.21 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa": "Tabel 3.24 Matriks Kendala Pelaksanaan Proyek Kerja Praktik dan Solusi Rekayasa"
}

for p in doc.paragraphs[290:335]:
    if "Rincian hasil pengujian disajikan pada Tabel 3.8 sampai dengan Tabel 3.20." in p.text:
        p.text = p.text.replace("Tabel 3.8 sampai dengan Tabel 3.20.", "Tabel 3.11 sampai dengan Tabel 3.23.")
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(12)
        print("Updated Testing intro reference.")
    elif "disajikan pada Tabel 3.21." in p.text:
        p.text = p.text.replace("disajikan pada Tabel 3.21.", "disajikan pada Tabel 3.24.")
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(12)
        print("Updated Kendala intro reference.")
    else:
        text_strip = p.text.strip()
        if text_strip in testing_caption_replacements:
            new_text = testing_caption_replacements[text_strip]
            p.text = new_text
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
            p.runs[0].font.bold = True
            print(f"Updated: {text_strip[:30]} -> {new_text[:30]}")

doc.save(DOC_PATH)
print("Saved body caption updates successfully.")
