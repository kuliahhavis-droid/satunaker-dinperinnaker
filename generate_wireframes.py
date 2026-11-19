import os
from PIL import Image, ImageDraw, ImageFont

# -------------------------------------------------------------
# Configuration & Constants
# -------------------------------------------------------------
WIDTH = 1024
HEIGHT = 563

COLOR_BG_WHITE = (255, 255, 255)
COLOR_BORDER = (153, 153, 153)
COLOR_SIDEBAR_BG = (220, 220, 220)
COLOR_TOPBAR_BG = (230, 230, 230)
COLOR_BTN_INACTIVE = (236, 236, 236)
COLOR_BTN_ACTIVE = (189, 189, 189)
COLOR_BTN_PRIMARY = (189, 189, 189)
COLOR_BTN_LIGHT = (236, 236, 236)
COLOR_TABLE_HEADER = (207, 207, 207)
COLOR_TABLE_DIVIDER = (220, 220, 220)
COLOR_TEXT_DARK = (20, 20, 20)
COLOR_TEXT_MUTED = (100, 100, 100)
COLOR_CARD_BG = (248, 249, 250)

# TrueType Fonts
FONT_BOLD_18 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 18)
FONT_BOLD_16 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 16)
FONT_BOLD_15 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 15)
FONT_BOLD_14 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 13)
FONT_BOLD_13 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 13)
FONT_BOLD_12 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 12)
FONT_BOLD_11 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 11)
FONT_BOLD_10 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 10)

FONT_REG_16 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
FONT_REG_14 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
FONT_REG_13 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)
FONT_REG_12 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)
FONT_REG_11 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 11)
FONT_REG_10 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 10)
FONT_REG_9 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 9)

MENU_ITEMS = [
    ("Dashboard", "dashboard"),
    ("Kelola Data", "kelola-data"),
    ("Laporan", "laporan"),
    ("Unit Kerja*", "unit-kerja"),
    ("Pengguna*", "users"),
    ("Backup*", "backup"),
]

def create_base_canvas(active_key="dashboard", page_title="Dashboard Eksekutif", user_name="Nama Pengguna", show_footnote=True, footnote_y=385):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLOR_BG_WHITE)
    draw = ImageDraw.Draw(img)

    # Outer Border
    draw.rectangle([12, 12, 1011, 550], outline=COLOR_BORDER, width=1)

    # Sidebar Area
    draw.rectangle([12, 12, 230, 550], fill=COLOR_SIDEBAR_BG, outline=COLOR_BORDER, width=1)

    # Topbar Area
    draw.rectangle([230, 12, 1011, 65], fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER, width=1)

    # Logo SatuNaker
    draw.text((121, 44), "LOGO SatuNaker", fill=COLOR_TEXT_DARK, font=FONT_BOLD_16, anchor="mm")

    # Sidebar Menu Buttons
    btn_y = 84
    btn_h = 34
    btn_gap = 14
    for label, key in MENU_ITEMS:
        is_active = (key == active_key)
        bg_col = COLOR_BTN_ACTIVE if is_active else COLOR_BTN_INACTIVE
        draw.rounded_rectangle([28, btn_y, 214, btn_y + btn_h], radius=6, fill=bg_col, outline=COLOR_BORDER, width=1)
        font = FONT_BOLD_14 if is_active else FONT_REG_14
        draw.text((121, btn_y + btn_h // 2), label, fill=COLOR_TEXT_DARK, font=font, anchor="mm")
        btn_y += btn_h + btn_gap

    # Topbar Content
    draw.text((256, 39), page_title, fill=COLOR_TEXT_DARK, font=FONT_BOLD_16, anchor="lm")
    draw.text((988, 39), user_name, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="rm")

    # Footnote
    if show_footnote:
        draw.text((256, footnote_y), "* Menu hanya tampil untuk Super Admin", fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")

    return img, draw

def draw_input(draw, bbox, text, is_placeholder=False):
    draw.rounded_rectangle(bbox, radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    col = COLOR_TEXT_MUTED if is_placeholder else COLOR_TEXT_DARK
    draw.text((bbox[0] + 12, (bbox[1] + bbox[3]) // 2), text, fill=col, font=FONT_REG_13, anchor="lm")

def draw_button(draw, bbox, text, is_primary=False, is_bold=True):
    bg_col = COLOR_BTN_PRIMARY if is_primary else COLOR_BTN_LIGHT
    draw.rounded_rectangle(bbox, radius=6, fill=bg_col, outline=COLOR_BORDER, width=1)
    font = FONT_BOLD_14 if is_bold else FONT_REG_13
    draw.text(((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2), text, fill=COLOR_TEXT_DARK, font=font, anchor="mm")

def draw_dropdown(draw, bbox, text):
    draw.rounded_rectangle(bbox, radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((bbox[0] + 12, (bbox[1] + bbox[3]) // 2), text, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
    ax = bbox[2] - 14
    ay = (bbox[1] + bbox[3]) // 2
    draw.polygon([(ax - 4, ay - 2), (ax + 4, ay - 2), (ax, ay + 3)], fill=COLOR_BORDER)

def save_wireframe(img, filename):
    out_dir_local = r'd:\Magang\sistem-satudata-dinperinnaker\document\images\wireframes'
    out_dir_brain = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54\wireframes'
    out_dir_root = r'C:\Users\LENOVO\.gemini\antigravity\brain\afd761e0-7192-416d-90e8-ca2ff99eeb54'

    os.makedirs(out_dir_local, exist_ok=True)
    os.makedirs(out_dir_brain, exist_ok=True)
    os.makedirs(out_dir_root, exist_ok=True)

    p1 = os.path.join(out_dir_local, filename)
    p2 = os.path.join(out_dir_brain, filename)
    p3 = os.path.join(out_dir_root, filename)

    img.save(p1)
    img.save(p2)
    img.save(p3)
    print(f"Generated: {filename}")

# =============================================================
# 1. Wireframe 01: Halaman Login
# =============================================================
def generate_wireframe_01_login():
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(244, 245, 247))
    draw = ImageDraw.Draw(img)

    # Browser Outer Frame
    draw.rectangle([12, 12, 1011, 550], fill=(244, 245, 247), outline=COLOR_BORDER, width=1)

    # Browser Header / Titlebar
    draw.rectangle([12, 12, 1011, 48], fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER, width=1)
    # Window circles
    draw.ellipse([24, 24, 34, 34], fill=(200, 200, 200), outline=COLOR_BORDER)
    draw.ellipse([40, 24, 50, 34], fill=(200, 200, 200), outline=COLOR_BORDER)
    draw.ellipse([56, 24, 66, 34], fill=(200, 200, 200), outline=COLOR_BORDER)
    # URL bar
    draw.rounded_rectangle([150, 20, 874, 40], radius=4, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((160, 30), "http://localhost:3000/login - SatuNaker DINPERINNAKER Purbalingga", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")

    # Centered Login Card
    cx0, cy0, cx1, cy1 = 312, 68, 712, 532
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=8, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)

    # Logo & Brand Header
    draw.rounded_rectangle([472, 85, 552, 125], radius=6, fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER)
    draw.text((512, 105), "LOGO", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="mm")

    draw.text((512, 142), "SatuNaker Purbalingga", fill=COLOR_TEXT_DARK, font=FONT_BOLD_16, anchor="mm")
    draw.text((512, 160), "Sistem Informasi Terpadu Satu Data Ketenagakerjaan", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="mm")
    draw.line([342, 175, 682, 175], fill=COLOR_TABLE_DIVIDER, width=1)

    # Form Fields
    draw.text((342, 192), "Email atau Nama Pengguna", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [342, 205, 682, 240], "contoh@dinperinnaker.go.id", is_placeholder=True)

    draw.text((342, 258), "Kata Sandi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [342, 271, 682, 306], "••••••••••••••••")

    # Options Row
    draw.rectangle([342, 320, 354, 332], outline=COLOR_BORDER, fill=COLOR_BG_WHITE)
    draw.text((362, 326), "Ingat sesi login saya", fill=COLOR_TEXT_DARK, font=FONT_REG_11, anchor="lm")
    draw.text((682, 326), "Lupa kata sandi?", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="rm")

    # Login Button
    draw_button(draw, [342, 350, 682, 390], "Masuk ke Sistem", is_primary=True, is_bold=True)

    # RBAC Callout Note
    draw.rounded_rectangle([332, 408, 692, 514], radius=6, fill=COLOR_CARD_BG, outline=COLOR_TABLE_DIVIDER, width=1)
    draw.text((344, 424), "Klasifikasi Hak Akses Sistem (RBAC):", fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="lm")
    draw.text((344, 444), "- Super Admin : Akses penuh data dinas, master unit, user & backup", fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="lm")
    draw.text((344, 464), "- Admin Bidang : Akses terisolasi otomatis sesuai bidang/unit kerja", fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="lm")
    draw.text((344, 484), "- Eksekutif    : Pratinjau dashboard & cetak rekapitulasi kop resmi", fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="lm")

    save_wireframe(img, "wireframe_01_login.png")

# =============================================================
# 2. Wireframe 02: Halaman Dashboard
# =============================================================
def generate_wireframe_02_dashboard():
    img, draw = create_base_canvas(
        active_key="dashboard",
        page_title="Dashboard Eksekutif SatuNaker",
        user_name="Havisda M. (Super Admin)",
        show_footnote=True,
        footnote_y=515
    )

    # Top Controls Bar
    draw.text((256, 102), "Filter Periode:", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw_dropdown(draw, [345, 84, 455, 120], "2026")

    draw.text((475, 102), "Unit Kerja:", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw_dropdown(draw, [550, 84, 820, 120], "Semua Unit Kerja (Global)")

    draw_button(draw, [840, 84, 994, 120], "Refresh Data", is_primary=False, is_bold=False)

    # 4 KPI Cards
    kpis = [
        ("Total Data Sektoral", "128", "Indikator"),
        ("Unit Kerja Terdata", "7", "Bidang Dinas"),
        ("Data Dukung Valid", "100%", "Google Drive"),
        ("Pembaruan Terakhir", "Hari ini", "09:30 WIB")
    ]
    card_w = 175
    gap = 9
    start_x = 256
    for i, (title, val, sub) in enumerate(kpis):
        x0 = start_x + i * (card_w + gap)
        x1 = x0 + card_w
        draw.rounded_rectangle([x0, 134, x1, 202], radius=6, fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
        draw.text((x0 + 12, 148), title, fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")
        draw.text((x0 + 12, 172), val, fill=COLOR_TEXT_DARK, font=FONT_BOLD_18, anchor="lm")
        draw.text((x0 + 12, 190), sub, fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="lm")

    # Chart 1: Left Card (Tren Volume Data)
    draw.rounded_rectangle([256, 216, 616, 495], radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((272, 236), "Tren Volume Data Sektoral (2022 - 2026)", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((272, 252), "Pertumbuhan akumulasi indikator terdata per tahun", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")
    draw.line([272, 262, 600, 262], fill=COLOR_TABLE_DIVIDER, width=1)

    # Bar chart mockup
    draw.line([305, 280, 305, 450], fill=COLOR_BORDER, width=1) # Y axis
    draw.line([305, 450, 585, 450], fill=COLOR_BORDER, width=1) # X axis

    bars = [("2022", 45, 60), ("2023", 68, 90), ("2024", 88, 115), ("2025", 110, 140), ("2026", 128, 160)]
    bx = 330
    for yr, val, bh in bars:
        draw.rounded_rectangle([bx, 450 - bh, bx + 32, 450], radius=3, fill=COLOR_BTN_ACTIVE, outline=COLOR_BORDER)
        draw.text((bx + 16, 442 - bh), str(val), fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="mm")
        draw.text((bx + 16, 464), yr, fill=COLOR_TEXT_DARK, font=FONT_REG_11, anchor="mm")
        bx += 52

    # Chart 2: Right Card (Distribusi Unit Kerja)
    draw.rounded_rectangle([634, 216, 994, 495], radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((650, 236), "Distribusi Indikator per Bidang / Unit", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((650, 252), "Proporsi kepemilikan indikator data aktif", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")
    draw.line([650, 262, 978, 262], fill=COLOR_TABLE_DIVIDER, width=1)

    units_data = [
        ("Hubungan Industrial", 32, 190),
        ("Penempatan Tenaga Kerja", 28, 165),
        ("Sekretariat Dinas", 24, 140),
        ("Pelatihan Kerja (BLK)", 22, 130),
        ("Perindustrian & Agro", 22, 130)
    ]
    uy = 285
    for uname, cnt, bar_len in units_data:
        draw.text((650, uy), uname, fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
        draw.text((978, uy), f"{cnt} Data", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="rm")
        # Bar track
        draw.rounded_rectangle([650, uy + 8, 978, uy + 18], radius=4, fill=(240, 240, 240), outline=COLOR_TABLE_DIVIDER)
        draw.rounded_rectangle([650, uy + 8, 650 + bar_len, uy + 18], radius=4, fill=COLOR_BTN_ACTIVE, outline=COLOR_BORDER)
        uy += 40

    save_wireframe(img, "wireframe_02_dashboard.png")

# =============================================================
# 3. Wireframe 03: Kelola Data Sektoral
# =============================================================
def draw_kelola_data_content(draw):
    # Controls Row
    draw_input(draw, [256, 88, 500, 124], "Cari nama data...", is_placeholder=True)
    draw_dropdown(draw, [512, 88, 654, 124], "Unit Kerja")
    draw_dropdown(draw, [666, 88, 782, 124], "Status")
    draw_button(draw, [846, 88, 994, 124], "+ Tambah Data", is_primary=True, is_bold=True)

    # Table
    table_x0 = 256
    table_x1 = 994
    table_y0 = 144

    # Header Row
    draw.rectangle([table_x0, table_y0, table_x1, table_y0 + 40], fill=COLOR_TABLE_HEADER, outline=COLOR_BORDER, width=1)
    draw.text((268, table_y0 + 20), "No", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((304, table_y0 + 20), "Nama Data", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((562, table_y0 + 20), "Tahun", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((622, table_y0 + 20), "Jumlah", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((712, table_y0 + 20), "Data Dukung", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((854, table_y0 + 20), "Aksi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")

    # Rows
    rows_data = [
        ("1", "Jumlah tenaga kerja di-PHK", "2026", "120 orang"),
        ("2", "Jumlah tenaga kerja asing", "2026", "45 orang"),
        ("3", "Jumlah pencari kerja terdaftar", "2026", "3.200 orang")
    ]
    ry = table_y0 + 40
    row_h = 48
    for no, nama, thn, jml in rows_data:
        draw.rectangle([table_x0, ry, table_x1, ry + row_h], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
        draw.text((268, ry + row_h // 2), no, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((304, ry + row_h // 2), nama, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((562, ry + row_h // 2), thn, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((622, ry + row_h // 2), jml, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")

        # Button Buka Drive
        draw.rounded_rectangle([712, ry + 9, 836, ry + 39], radius=6, fill=COLOR_BTN_LIGHT, outline=COLOR_BORDER, width=1)
        draw.text((774, ry + row_h // 2), "Buka Drive", fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="mm")

        # Aksi text
        draw.text((854, ry + row_h // 2), "Edit | Hapus", fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        ry += row_h

def generate_wireframe_03_kelola_data():
    img, draw = create_base_canvas(
        active_key="kelola-data",
        page_title="Kelola Data Sektoral",
        user_name="Nama Pengguna",
        show_footnote=True,
        footnote_y=385
    )
    draw_kelola_data_content(draw)
    save_wireframe(img, "wireframe_03_kelola_data.png")

# =============================================================
# 4. Wireframe 04: Modal Form Tambah Data
# =============================================================
def generate_wireframe_04_modal_tambah():
    # Base canvas underlying with actual kelola data contents
    img, draw = create_base_canvas(
        active_key="kelola-data",
        page_title="Kelola Data Sektoral",
        user_name="Nama Pengguna",
        show_footnote=True,
        footnote_y=385
    )
    draw_kelola_data_content(draw)

    # Draw dimmed overlay over the main area
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 75))
    img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(img)

    # Modal Dialog Box
    mx0, my0, mx1, my1 = 285, 45, 785, 525
    draw.rounded_rectangle([mx0, my0, mx1, my1], radius=8, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)

    # Modal Header
    draw.rounded_rectangle([mx0, my0, mx1, my0 + 48], radius=8, fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER, width=1)
    draw.rectangle([mx0, my0 + 20, mx1, my0 + 48], fill=COLOR_TOPBAR_BG)
    draw.line([mx0, my0 + 48, mx1, my0 + 48], fill=COLOR_BORDER, width=1)
    draw.text((mx0 + 20, my0 + 24), "Tambah Data Sektoral Baru", fill=COLOR_TEXT_DARK, font=FONT_BOLD_16, anchor="lm")
    draw.text((mx1 - 24, my0 + 24), "X", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="mm")

    # Form Fields
    # Field 1: Nama Data
    draw.text((mx0 + 20, my0 + 66), "Nama Data Sektoral *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [mx0 + 20, my0 + 78, mx1 - 20, my0 + 112], "Jumlah Tenaga Kerja Terserap Sektor Industri")

    # Field 2 & 3: Satuan & Tahun
    draw.text((mx0 + 20, my0 + 130), "Satuan Pengukuran *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [mx0 + 20, my0 + 142, mx0 + 230, my0 + 176], "Orang")

    draw.text((mx0 + 250, my0 + 130), "Tahun Pendataan *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_dropdown(draw, [mx0 + 250, my0 + 142, mx1 - 20, my0 + 176], "2026")

    # Field 4: Unit Kerja (Locked Guard)
    draw.text((mx0 + 20, my0 + 194), "Unit Kerja / Bidang (Terkunci Otomatis Sesuai Akun) *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw.rounded_rectangle([mx0 + 20, my0 + 206, mx1 - 20, my0 + 240], radius=6, fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    draw.text((mx0 + 32, my0 + 223), "[Terkunci] Bidang Hubungan Industrial & Syarat Kerja", fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")

    # Field 5: Jumlah
    draw.text((mx0 + 20, my0 + 258), "Jumlah / Capaian Realisasi *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [mx0 + 20, my0 + 270, mx1 - 20, my0 + 304], "450")

    # Field 6: Google Drive Link
    draw.text((mx0 + 20, my0 + 322), "Tautan Bukti Dukung (Google Drive) *", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="lm")
    draw_input(draw, [mx0 + 20, my0 + 334, mx1 - 20, my0 + 368], "https://drive.google.com/file/d/1A2b3C_sample_sk/view")

    # Hint callout
    draw.rounded_rectangle([mx0 + 20, my0 + 382, mx1 - 20, my0 + 418], radius=6, fill=COLOR_CARD_BG, outline=COLOR_TABLE_DIVIDER, width=1)
    draw.text((mx0 + 30, my0 + 400), "[!] Wajib menyertakan tautan Google Drive berkas SK / bukti dinas yang valid.", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")

    # Footer Actions
    draw.line([mx0, my1 - 60, mx1, my1 - 60], fill=COLOR_BORDER, width=1)
    draw_button(draw, [mx1 - 220, my1 - 48, mx1 - 130, my1 - 14], "Batal", is_primary=False, is_bold=False)
    draw_button(draw, [mx1 - 120, my1 - 48, mx1 - 20, my1 - 14], "Simpan Data", is_primary=True, is_bold=True)

    save_wireframe(img, "wireframe_04_modal_tambah.png")

# =============================================================
# 5. Wireframe 05: Halaman Laporan & Ekspor
# =============================================================
def generate_wireframe_05_laporan():
    img, draw = create_base_canvas(
        active_key="laporan",
        page_title="Pusat Rekapitulasi Laporan",
        user_name="Nama Pengguna",
        show_footnote=True,
        footnote_y=485
    )

    # Top Controls Bar
    draw_dropdown(draw, [256, 86, 380, 122], "Tahun: 2026")
    draw_dropdown(draw, [392, 86, 600, 122], "Unit: Semua Bidang")
    draw_button(draw, [612, 86, 700, 122], "Filter", is_primary=False, is_bold=False)

    # Action Buttons Right
    draw_button(draw, [714, 86, 846, 122], "Ekspor Excel (.xlsx)", is_primary=False, is_bold=True)
    draw_button(draw, [858, 86, 994, 122], "Cetak Ber-Kop Resmi", is_primary=True, is_bold=True)

    # Summary Info Card
    draw.rounded_rectangle([256, 136, 994, 176], radius=6, fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    draw.text((272, 156), "Ringkasan Laporan: Terpilih 128 Data dari 7 Unit Kerja  |  Status Kelengkapan Data Dukung: 100% Valid Drive", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")

    # Table
    table_x0 = 256
    table_x1 = 994
    table_y0 = 190

    # Header
    draw.rectangle([table_x0, table_y0, table_x1, table_y0 + 38], fill=COLOR_TABLE_HEADER, outline=COLOR_BORDER, width=1)
    draw.text((268, table_y0 + 19), "No", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((304, table_y0 + 19), "Unit Kerja / Bidang", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((580, table_y0 + 19), "Jumlah Data", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((690, table_y0 + 19), "Status Dukung", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((820, table_y0 + 19), "Pembaruan", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((930, table_y0 + 19), "Aksi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")

    rows = [
        ("1", "Sekretariat Dinas", "24 Indikator", "Lengkap (100%)", "19 Nov 2026"),
        ("2", "Bidang Hubungan Industrial & Syarat Kerja", "32 Indikator", "Lengkap (100%)", "19 Nov 2026"),
        ("3", "Bidang Penempatan & Perluasan Tenaga Kerja", "28 Indikator", "Lengkap (100%)", "18 Nov 2026"),
        ("4", "Bidang Pelatihan Kerja & Standardisasi (BLK)", "22 Indikator", "Lengkap (100%)", "18 Nov 2026"),
        ("5", "Bidang Perindustrian & Komoditas Agro", "22 Indikator", "Lengkap (100%)", "17 Nov 2026")
    ]
    ry = table_y0 + 38
    row_h = 44
    for no, uname, jdata, sduk, updatetime in rows:
        draw.rectangle([table_x0, ry, table_x1, ry + row_h], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
        draw.text((268, ry + row_h // 2), no, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
        draw.text((304, ry + row_h // 2), uname, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
        draw.text((580, ry + row_h // 2), jdata, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
        draw.text((690, ry + row_h // 2), sduk, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
        draw.text((820, ry + row_h // 2), updatetime, fill=COLOR_TEXT_MUTED, font=FONT_REG_12, anchor="lm")

        # Action pill
        draw.rounded_rectangle([915, ry + 8, 985, ry + 36], radius=4, fill=COLOR_BTN_LIGHT, outline=COLOR_BORDER)
        draw.text((950, ry + row_h // 2), "Lihat", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="mm")
        ry += row_h

    save_wireframe(img, "wireframe_05_laporan.png")

# =============================================================
# 6. Wireframe 06: Pratinjau Cetak Ber-Kop Resmi
# =============================================================
def generate_wireframe_06_cetak_kop():
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(235, 236, 239))
    draw = ImageDraw.Draw(img)

    # Outer Browser / Print Frame
    draw.rectangle([12, 12, 1011, 550], fill=(235, 236, 239), outline=COLOR_BORDER, width=1)

    # Top Control Bar
    draw.rectangle([12, 12, 1011, 52], fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER, width=1)
    draw.text((28, 32), "Pratinjau Cetak Dokumen Ber-Kop Resmi (DINPERINNAKER)", fill=COLOR_TEXT_DARK, font=FONT_BOLD_15, anchor="lm")
    draw_button(draw, [650, 18, 810, 46], "<- Kembali ke Laporan", is_primary=False, is_bold=False)
    draw_button(draw, [824, 18, 994, 46], "[Cetak] Cetak / Unduh PDF", is_primary=True, is_bold=True)

    # Simulated A4 Sheet (Centered)
    sx0, sy0, sx1, sy1 = 200, 62, 824, 542
    draw.rectangle([sx0, sy0, sx1, sy1], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)

    # KOP SURAT RESMI
    # Logo Box
    draw.rectangle([sx0 + 24, sy0 + 14, sx0 + 74, sy0 + 64], fill=COLOR_TOPBAR_BG, outline=COLOR_BORDER)
    draw.text((sx0 + 49, sy0 + 39), "LOGO", fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="mm")

    # Dinas Header
    cx = (sx0 + sx1) // 2 + 20
    draw.text((cx, sy0 + 18), "PEMERINTAH KABUPATEN PURBALINGGA", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="mm")
    draw.text((cx, sy0 + 34), "DINAS PERINDUSTRIAN DAN TENAGA KERJA", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="mm")
    draw.text((cx, sy0 + 49), "Jalan Mayjen Sungkono No. 34 Purbalingga, Jawa Tengah Kode Pos 53311", fill=COLOR_TEXT_DARK, font=FONT_REG_9, anchor="mm")
    draw.text((cx, sy0 + 61), "Pos-el: dinperinnaker@purbalinggakab.go.id | Laman: dinperinnaker.purbalinggakab.go.id", fill=COLOR_TEXT_DARK, font=FONT_REG_9, anchor="mm")

    # Double Line Kop
    draw.line([sx0 + 20, sy0 + 72, sx1 - 20, sy0 + 72], fill=COLOR_TEXT_DARK, width=2)
    draw.line([sx0 + 20, sy0 + 75, sx1 - 20, sy0 + 75], fill=COLOR_TEXT_DARK, width=1)

    # Document Title
    draw.text(((sx0 + sx1) // 2, sy0 + 94), "LAPORAN REKAPITULASI DATA SEKTORAL KETENAGAKERJAAN", fill=COLOR_TEXT_DARK, font=FONT_BOLD_12, anchor="mm")
    draw.text(((sx0 + sx1) // 2, sy0 + 109), "TAHUN ANGGARAN 2026", fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="mm")

    # Formal Table
    tx0 = sx0 + 20
    tx1 = sx1 - 20
    ty0 = sy0 + 124

    draw.rectangle([tx0, ty0, tx1, ty0 + 26], fill=COLOR_TABLE_HEADER, outline=COLOR_TEXT_DARK, width=1)
    draw.text((tx0 + 10, ty0 + 13), "No", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")
    draw.text((tx0 + 36, ty0 + 13), "Nama Indikator Data Sektoral", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")
    draw.text((tx0 + 290, ty0 + 13), "Unit Kerja", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")
    draw.text((tx0 + 420, ty0 + 13), "Satuan", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")
    draw.text((tx0 + 490, ty0 + 13), "Realisasi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")

    doc_rows = [
        ("1", "Jumlah Tenaga Kerja di-PHK", "Hub. Industrial", "Orang", "120"),
        ("2", "Tenaga Kerja Asing (TKA) Terdata", "Hub. Industrial", "Orang", "45"),
        ("3", "Pencari Kerja Terdaftar (Kartu AK-1)", "Penempatan TK", "Orang", "3.200"),
        ("4", "Peserta Pelatihan Kerja Vokasi BLK", "Pelatihan Kerja", "Orang", "480"),
        ("5", "Perusahaan Wajib Lapor Ketenagakerjaan", "Hub. Industrial", "Badan", "310"),
        ("6", "Kasus Perselisihan Industrial Selesai", "Hub. Industrial", "Kasus", "8")
    ]
    dry = ty0 + 26
    drow_h = 24
    for no, nama, unit, sat, real in doc_rows:
        draw.rectangle([tx0, dry, tx1, dry + drow_h], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
        draw.text((tx0 + 10, dry + drow_h // 2), no, fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
        draw.text((tx0 + 36, dry + drow_h // 2), nama, fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
        draw.text((tx0 + 290, dry + drow_h // 2), unit, fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
        draw.text((tx0 + 420, dry + drow_h // 2), sat, fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
        draw.text((tx0 + 490, dry + drow_h // 2), real, fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
        dry += drow_h

    # Signature Block (Right Aligned)
    sig_x = sx1 - 200
    sig_y = dry + 22
    draw.text((sig_x, sig_y), "Purbalingga, 19 November 2026", fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
    draw.text((sig_x, sig_y + 14), "Kepala Dinas Perindustrian dan Tenaga Kerja", fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")
    draw.text((sig_x, sig_y + 26), "Kabupaten Purbalingga", fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")

    # Stempel / Sign Area
    draw.text((sig_x + 10, sig_y + 54), "[ Cap Dinas & Tanda Tangan ]", fill=COLOR_TEXT_MUTED, font=FONT_REG_9, anchor="lm")

    draw.text((sig_x, sig_y + 84), "Drs. BAMBANG WIDJONARKO, M.Si.", fill=COLOR_TEXT_DARK, font=FONT_BOLD_10, anchor="lm")
    draw.line([sig_x, sig_y + 92, sig_x + 185, sig_y + 92], fill=COLOR_TEXT_DARK, width=1)
    draw.text((sig_x, sig_y + 98), "Pembina Utama Muda", fill=COLOR_TEXT_DARK, font=FONT_REG_9, anchor="lm")
    draw.text((sig_x, sig_y + 110), "NIP. 19700101 199503 1 001", fill=COLOR_TEXT_DARK, font=FONT_REG_9, anchor="lm")

    save_wireframe(img, "wireframe_06_cetak_kop_resmi.png")

# =============================================================
# 7. Wireframe 07: Master Unit Kerja
# =============================================================
def generate_wireframe_07_unit_kerja():
    img, draw = create_base_canvas(
        active_key="unit-kerja",
        page_title="Kelola Master Unit Kerja (Super Admin)",
        user_name="Super Admin",
        show_footnote=True,
        footnote_y=440
    )

    # Controls Row
    draw_input(draw, [256, 88, 550, 124], "Cari unit kerja...", is_placeholder=True)
    draw_dropdown(draw, [565, 88, 730, 124], "Semua Kategori")
    draw_button(draw, [790, 88, 994, 124], "+ Tambah Unit Kerja", is_primary=True, is_bold=True)

    # Table
    table_x0 = 256
    table_x1 = 994
    table_y0 = 144

    draw.rectangle([table_x0, table_y0, table_x1, table_y0 + 40], fill=COLOR_TABLE_HEADER, outline=COLOR_BORDER, width=1)
    draw.text((268, table_y0 + 20), "No", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((310, table_y0 + 20), "Kode", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((420, table_y0 + 20), "Nama Unit Kerja / Bidang", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((720, table_y0 + 20), "Jumlah Data", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((865, table_y0 + 20), "Aksi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")

    units = [
        ("1", "SEKRE", "Sekretariat Dinas", "24 Indikator"),
        ("2", "HI", "Bidang Hubungan Industrial & Syarat Kerja", "32 Indikator"),
        ("3", "PENTA", "Bidang Penempatan & Perluasan Tenaga Kerja", "28 Indikator"),
        ("4", "LATVOK", "Bidang Pelatihan Kerja & Standardisasi (BLK)", "22 Indikator"),
        ("5", "IND", "Bidang Perindustrian & Komoditas Agro", "22 Indikator")
    ]
    ry = table_y0 + 40
    row_h = 48
    for no, kode, uname, jdata in units:
        draw.rectangle([table_x0, ry, table_x1, ry + row_h], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
        draw.text((268, ry + row_h // 2), no, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((310, ry + row_h // 2), kode, fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
        draw.text((420, ry + row_h // 2), uname, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((720, ry + row_h // 2), jdata, fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        draw.text((865, ry + row_h // 2), "Edit | Hapus", fill=COLOR_TEXT_DARK, font=FONT_REG_14, anchor="lm")
        ry += row_h

    save_wireframe(img, "wireframe_07_unit_kerja.png")

# =============================================================
# 8. Wireframe 08: Manajemen Pengguna & RBAC
# =============================================================
def generate_wireframe_08_manajemen_pengguna():
    img, draw = create_base_canvas(
        active_key="users",
        page_title="Manajemen Pengguna & RBAC",
        user_name="Super Admin",
        show_footnote=True,
        footnote_y=440
    )

    # Controls Row
    draw_input(draw, [256, 88, 550, 124], "Cari nama / email pengguna...", is_placeholder=True)
    draw_dropdown(draw, [565, 88, 730, 124], "Semua Peran")
    draw_button(draw, [790, 88, 994, 124], "+ Tambah Pengguna", is_primary=True, is_bold=True)

    # Table
    table_x0 = 256
    table_x1 = 994
    table_y0 = 144

    draw.rectangle([table_x0, table_y0, table_x1, table_y0 + 40], fill=COLOR_TABLE_HEADER, outline=COLOR_BORDER, width=1)
    draw.text((268, table_y0 + 20), "No", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((298, table_y0 + 20), "Nama Lengkap", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((455, table_y0 + 20), "Email Akun", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((645, table_y0 + 20), "Unit Kerja Terikat", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((805, table_y0 + 20), "Peran (Role)", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")
    draw.text((915, table_y0 + 20), "Aksi", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="lm")

    users = [
        ("1", "Havisda Mei Khairil", "admin.utama@purbalingga.go.id", "Semua Unit (Global)", "[Super Admin]"),
        ("2", "Budi Santoso, S.E.", "admin.hi@purbalingga.go.id", "Hubungan Industrial", "[Admin Bidang]"),
        ("3", "Siti Rahmawati, S.Kom", "admin.penta@purbalingga.go.id", "Penempatan Tenaga Kerja", "[Admin Bidang]"),
        ("4", "Ahmad Fadli, S.T.", "admin.latvok@purbalingga.go.id", "Pelatihan Vokasi (BLK)", "[Admin Bidang]"),
        ("5", "Tri Wahyuni, S.Sos", "admin.sekre@purbalingga.go.id", "Sekretariat Dinas", "[Admin Bidang]")
    ]
    ry = table_y0 + 40
    row_h = 48
    for no, name, email, unit, role in users:
        draw.rectangle([table_x0, ry, table_x1, ry + row_h], fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
        draw.text((268, ry + row_h // 2), no, fill=COLOR_TEXT_DARK, font=FONT_REG_13, anchor="lm")
        draw.text((298, ry + row_h // 2), name, fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="lm")
        draw.text((455, ry + row_h // 2), email, fill=COLOR_TEXT_DARK, font=FONT_REG_11, anchor="lm")
        draw.text((645, ry + row_h // 2), unit, fill=COLOR_TEXT_DARK, font=FONT_REG_11, anchor="lm")
        draw.text((805, ry + row_h // 2), role, fill=COLOR_TEXT_DARK, font=FONT_BOLD_11, anchor="lm")
        draw.text((915, ry + row_h // 2), "Edit | Reset", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
        ry += row_h

    save_wireframe(img, "wireframe_08_manajemen_pengguna.png")

# =============================================================
# 9. Wireframe 09: Backup & Restore Database
# =============================================================
def generate_wireframe_09_backup_restore():
    img, draw = create_base_canvas(
        active_key="backup",
        page_title="Cadangan & Pemulihan Database",
        user_name="Super Admin",
        show_footnote=True,
        footnote_y=485
    )

    # 2 Feature Cards Side by Side
    # Left Card: Backup
    draw.rounded_rectangle([256, 88, 614, 465], radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((276, 114), "[Backup] Cadangkan Database (JSON)", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((276, 134), "Simpan salinan data sektoral dan struktur sistem", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")
    draw.line([276, 148, 594, 148], fill=COLOR_TABLE_DIVIDER, width=1)

    # Info box
    draw.rounded_rectangle([276, 165, 594, 305], radius=6, fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    draw.text((292, 185), "Status Basis Data  : Terkoneksi & Normal", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
    draw.text((292, 210), "Total Data Sektoral: 128 Rekaman", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
    draw.text((292, 235), "Total Master Unit  : 7 Bidang Dinas", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
    draw.text((292, 260), "Format Ekspor      : JavaScript Object Notation (.json)", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="lm")
    draw.text((292, 285), "Terakhir Backup    : 18 Nov 2026, 17:00 WIB", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")

    draw.text((276, 330), "* Berkas cadangan terenkripsi dan dapat dipulihkan kapan saja.", fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="lm")
    draw_button(draw, [276, 385, 594, 435], "Unduh Berkas Cadangan (.json)", is_primary=True, is_bold=True)

    # Right Card: Restore
    draw.rounded_rectangle([636, 88, 994, 465], radius=6, fill=COLOR_BG_WHITE, outline=COLOR_BORDER, width=1)
    draw.text((656, 114), "[Restore] Pulihkan Database (JSON)", fill=COLOR_TEXT_DARK, font=FONT_BOLD_14, anchor="lm")
    draw.text((656, 134), "Kembalikan data dinas dari berkas cadangan", fill=COLOR_TEXT_MUTED, font=FONT_REG_11, anchor="lm")
    draw.line([656, 148, 974, 148], fill=COLOR_TABLE_DIVIDER, width=1)

    # Upload Dropzone Area
    draw.rounded_rectangle([656, 165, 974, 290], radius=6, fill=(250, 250, 250), outline=COLOR_BORDER, width=1)
    draw.text((815, 205), "[ Upload Area ]", fill=COLOR_TEXT_DARK, font=FONT_BOLD_13, anchor="mm")
    draw.text((815, 228), "Klik atau seret berkas backup (.json) ke sini", fill=COLOR_TEXT_DARK, font=FONT_REG_12, anchor="mm")
    draw.text((815, 255), "Maksimal ukuran berkas cadangan: 50 MB", fill=COLOR_TEXT_MUTED, font=FONT_REG_10, anchor="mm")

    # Warning callout
    draw.rounded_rectangle([656, 310, 974, 360], radius=6, fill=COLOR_CARD_BG, outline=COLOR_TABLE_DIVIDER, width=1)
    draw.text((668, 335), "[Perhatian] Pemulihan akan menimpa rekaman data yang cocok.", fill=COLOR_TEXT_DARK, font=FONT_REG_10, anchor="lm")

    draw_button(draw, [656, 385, 974, 435], "Jalankan Pemulihan Database", is_primary=False, is_bold=True)

    save_wireframe(img, "wireframe_09_backup_restore.png")

# =============================================================
# Run All Generators
# =============================================================
if __name__ == '__main__':
    print("Generating complete SatuNaker wireframe images...")
    generate_wireframe_01_login()
    generate_wireframe_02_dashboard()
    generate_wireframe_03_kelola_data()
    generate_wireframe_04_modal_tambah()
    generate_wireframe_05_laporan()
    generate_wireframe_06_cetak_kop()
    generate_wireframe_07_unit_kerja()
    generate_wireframe_08_manajemen_pengguna()
    generate_wireframe_09_backup_restore()
    print("All 9 wireframes regenerated successfully with polished visuals!")
