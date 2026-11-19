import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx"

doc = docx.Document(DOC_PATH)

# Find paragraph A. Deskripsi Proyek
p_desc_idx = None
p_scope_idx = None

for idx, p in enumerate(doc.paragraphs):
    if p.text.strip() == "A. Deskripsi Proyek":
        p_desc_idx = idx
    elif p.text.strip() == "B. Ruang Lingkup Proyek":
        p_scope_idx = idx
        break

print(f"Desc at {p_desc_idx}, Scope at {p_scope_idx}")

# The paragraphs between p_desc_idx and p_scope_idx
paras_desc = doc.paragraphs[p_desc_idx+1:p_scope_idx]
print(f"Found {len(paras_desc)} paragraphs in Deskripsi Proyek.")

# Text for paragraph 1
p1_text = (
    "Dalam era transformasi digital kepemerintahan menuju penerapan Electronic Government yang terintegrasi, "
    "ketersediaan data statistik sektoral yang valid, akurat, mutakhir, dan mudah diakses merupakan fondasi esensial "
    "bagi perumusan kebijakan publik yang tepat sasaran. Dinas Perindustrian dan Tenaga Kerja (DINPERINNAKER) "
    "Kabupaten Purbalingga sebagai unsur pelaksana urusan pemerintahan daerah di bidang perindustrian dan ketenagakerjaan "
    "menaungi unit kerja struktural yang setiap periodenya memproduksi ribuan rekaman data strategis. Unit kerja tersebut "
    "meliputi Sekretariat (Subbag Perencanaan & Keuangan serta Subbag Umum & Kepegawaian), Bidang Hubungan Industrial dan "
    "Jaminan Sosial Tenaga Kerja (HIJTK), Bidang Pembinaan, Penempatan Tenaga Kerja, dan Transmigrasi (PPTK), "
    "Bidang Perindustrian, UPTD Balai Latihan Kerja (BLK), serta UPTD Pengembangan Industri Logam (PILOG)."
)

# Text for paragraph 2
p2_text = (
    "Berdasarkan observasi lapangan dan wawancara mendalam yang dilakukan selama pelaksanaan Kerja Praktik, "
    "pengelolaan data di lingkungan DINPERINNAKER Kabupaten Purbalingga masih menghadapi hambatan struktural yang signifikan. "
    "Setiap bidang mengelola data operasionalnya secara mandiri menggunakan berkas lembar sebar (spreadsheet) lokal seperti "
    "Microsoft Excel tanpa standardisasi struktur kolom yang seragam. Kondisi ini menciptakan fenomena pulau-pulau data (data silo) "
    "di mana pertukaran informasi antar-bidang sangat terhambat. Ketika pimpinan dinas atau instansi vertikal seperti Badan Pusat "
    "Statistik (BPS Kabupaten Purbalingga, 2024) dan Bappelitbangda memerlukan laporan rekapitulasi tahunan atau evaluasi Laporan "
    "Kinerja Instansi Pemerintah (LKjIP), staf dinas harus melakukan kompilasi manual berulang kali yang memakan waktu hingga berhari-hari "
    "kerja dan memiliki kerentanan tinggi terhadap kesalahan pengetikan ganda (human error)."
)

# Text for paragraph 3
p3_text = (
    "Selain permasalahan pada data numerik tabular, kendala mendasar lainnya terletak pada verifikasi berkas bukti fisik data dukung operasional. "
    "Dokumen penting seperti berkas Perjanjian Kerja Bersama (PKB), risalah mediasi perselisihan ketenagakerjaan, dokumen penempatan pencari kerja (kartu AK-1), "
    "sertifikat kelulusan pelatihan vokasi BLK, hingga dokumen uji mutu knalpot PILOG seringkali masih diarsipkan dalam bentuk fisik di lemari berkas masing-masing seksi. "
    "Akibatnya, proses validasi keabsahan data membutuhkan pencarian dokumen fisik secara konvensional yang tidak efisien dan rentan terhadap risiko kerusakan fisik maupun kehilangan dokumen historis."
)

# Text for paragraph 4
p4_text = (
    "Menjawab permasalahan tersebut, proyek Kerja Praktik ini difokuskan pada perancangan dan pembangunan sistem portal data terpadu berbasis web modern "
    "yang diberi nama Website Satu Data DINPERINNAKER Kabupaten Purbalingga (SatuNaker). Sistem SatuNaker dirancang sebagai simpul sentral (Single Source of Truth) "
    "yang menyatukan seluruh aliran pencatatan data sektoral dari seluruh unit kerja (HIJTK, PPTK, Perindustrian, Renkeu, Umpeg, BLK, dan PILOG) ke dalam satu basis data terpusat. "
    "Dengan arsitektur berbasis web modern, sistem ini memungkinkan staf admin bidang melakukan input data secara fleksibel, pimpinan dinas memantau indikator kinerja melalui dasbor "
    "eksekutif secara waktu-nyata (real-time), dan laporan resmi dinas dapat dicetak seketika lengkap dengan kop resmi Pemerintah Kabupaten Purbalingga, selaras dengan amanat "
    "Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia (Republik Indonesia, 2019), sehingga mendukung percepatan perwujudan tata kelola satu data di lingkungan pemerintah daerah secara terintegrasi (Hidayat & Rahmawati, 2022)."
)

correct_paras = [p1_text, p2_text, p3_text, p4_text]

# Set the paragraphs
for i in range(4):
    p = paras_desc[i]
    p.text = correct_paras[i]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(1.0)
    for run in p.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

# If there were extra paragraphs in paras_desc, remove them
if len(paras_desc) > 4:
    for p in paras_desc[4:]:
        p._element.getparent().remove(p._element)

doc.save(DOC_PATH)
print("Bab I Deskripsi Proyek paragraphs restored and polished perfectly!")
