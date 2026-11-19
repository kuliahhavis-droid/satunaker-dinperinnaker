import docx
from docx.shared import Pt

DOC_PATH = r"D:\Magang\sistem-satudata-dinperinnaker\document\Laporan_Kerja_Praktik_Havisda_Mei_Khairil_2303040113_Revisi_Final.docx"

doc = docx.Document(DOC_PATH)

# Find headings
p_dt_idx = None
p_dg_idx = None
p_dl_idx = None
p_ds_idx = None

for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == "DAFTAR TABEL":
        p_dt_idx = idx
    elif txt == "DAFTAR GAMBAR":
        p_dg_idx = idx
    elif txt == "DAFTAR LAMPIRAN":
        p_dl_idx = idx
    elif txt == "DAFTAR SINGKATAN DAN ISTILAH":
        p_ds_idx = idx
        break

print(f"Indices: DT={p_dt_idx}, DG={p_dg_idx}, DL={p_dl_idx}, DS={p_ds_idx}")

p_dg = doc.paragraphs[p_dg_idx]

# Extract the tabel items (currently at 104:130)
tabel_paras = []
for p in doc.paragraphs[p_dl_idx+1:p_ds_idx]:
    if p.text.startswith("Tabel "):
        tabel_paras.append(p)

print(f"Found {len(tabel_paras)} tabel items to move.")

# Move them before p_dg (DAFTAR GAMBAR)
for p in tabel_paras:
    p_dg._p.addprevious(p._p)

doc.save(DOC_PATH)
print("Preliminary lists reordered successfully!")
