# =====================================================
# IMPORT LIBRARY
# =====================================================

import streamlit as st
import pandas as pd

from datetime import datetime
from supabase import Client, create_client


# =====================================================
# KONFIGURASI APLIKASI
# =====================================================

APP_CONFIG = {
    "page_title": "MFF Database",
    "page_icon": "🎮",
    "layout": "wide",
    "sidebar_state": "expanded",
}

BACKGROUND_IMAGE_URL = (
    "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf"
    "?q=80&w=2071&auto=format&fit=crop"
)


# =====================================================
# INISIALISASI HALAMAN
# =====================================================

def setup_page():
    """
    Mengatur konfigurasi utama Streamlit.
    """

    st.set_page_config(
        page_title=APP_CONFIG["page_title"],
        page_icon=APP_CONFIG["page_icon"],
        layout=APP_CONFIG["layout"],
        initial_sidebar_state=APP_CONFIG["sidebar_state"]
    )


# =====================================================
# CUSTOM CSS
# =====================================================

def load_css():
    """
    Seluruh styling aplikasi berada di sini.

    Jika ingin mengubah:
    - Background
    - Font
    - Sidebar
    - Card Metric
    - Efek Hover
    - Warna Tema

    Edit di fungsi ini.
    """

    st.markdown(
        f"""
        <style>

        /* =====================================================
           FONT
        ===================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap'
        );

        html,
        body,
        [class*="css"] {{
            font-family: 'Poppins', sans-serif;
        }}

        /* =====================================================
           BACKGROUND
        ===================================================== */

        .stApp {{
            background-image: url("{BACKGROUND_IMAGE_URL}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp > header {{
            background-color: transparent;
        }}

        /* =====================================================
           MAIN CONTAINER
        ===================================================== */

        .block-container {{
            background-color: rgba(14, 17, 23, 0.85);
            padding: 2.5rem;
            border-radius: 20px;
            backdrop-filter: blur(8px);

            margin-top: 2rem;

            border: 1px solid rgba(
                255,
                255,
                255,
                0.05
            );

            box-shadow:
                0 10px 40px 0 rgba(
                    0,
                    0,
                    0,
                    0.6
                );
        }}

        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    #0b0f19 0%,
                    #161b22 100%
                ) !important;

            border-right:
                1px solid rgba(
                    255,
                    255,
                    255,
                    0.05
                ) !important;

            position: relative;
            overflow: hidden;
        }}

        [data-testid="stSidebar"]::before {{
            content: "";

            position: absolute;

            top: -100px;
            left: -100px;

            width: 300px;
            height: 300px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(0, 201, 255, 0.15) 0%,
                    transparent 70%
                );

            z-index: 0;
            pointer-events: none;
        }}

        [data-testid="stSidebar"]::after {{
            content: "";

            position: absolute;

            bottom: -100px;
            right: -100px;

            width: 250px;
            height: 250px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(146, 254, 157, 0.10) 0%,
                    transparent 70%
                );

            z-index: 0;
            pointer-events: none;
        }}

        /* =====================================================
           RADIO MENU
        ===================================================== */

        .stRadio > div {{
            gap: 12px;
            position: relative;
            z-index: 1;
        }}

        .stRadio > div > label {{
            background:
                rgba(255,255,255,0.03) !important;

            border:
                1px solid rgba(
                    255,
                    255,
                    255,
                    0.05
                ) !important;

            border-radius: 12px !important;

            padding: 12px 15px !important;

            transition: all .3s ease !important;

            cursor: pointer;
        }}

        .stRadio > div > label:hover {{
            transform: translateX(8px);

            border-color:
                rgba(
                    0,
                    201,
                    255,
                    0.4
                ) !important;

            background:
                linear-gradient(
                    90deg,
                    rgba(0,201,255,0.10) 0%,
                    transparent 100%
                ) !important;
        }}

        /* =====================================================
           TITLE
        ===================================================== */

        .glowing-title {{
            font-size: 38px;
            font-weight: 800;

            background:
                linear-gradient(
                    90deg,
                    #00C9FF 0%,
                    #92FE9D 100%
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            text-shadow:
                0 0 20px rgba(
                    0,
                    201,
                    255,
                    0.3
                );
        }}

        /* =====================================================
           METRIC CARD
        ===================================================== */

        [data-testid="stMetric"] {{
            padding: 20px;

            border-radius: 16px;

            border:
                1px solid rgba(
                    255,
                    255,
                    255,
                    0.10
                );

            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,0.05) 0%,
                    rgba(255,255,255,0.01) 100%
                );

            transition:
                transform .3s ease,
                box-shadow .3s ease,
                border-color .3s ease;
        }}

        [data-testid="stMetric"]:hover {{
            transform: translateY(-7px);

            border-color:
                rgba(
                    0,
                    201,
                    255,
                    0.5
                );

            box-shadow:
                0 10px 30px rgba(
                    0,
                    201,
                    255,
                    0.2
                );
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# SUPABASE
# =====================================================

SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =====================================================
# LOGIN SYSTEM
# =====================================================

APP_PASSWORD = "131313"


def check_password():

    def password_entered():

        st.session_state["password_correct"] = (
            st.session_state["password"] == APP_PASSWORD
        )

        if st.session_state["password_correct"]:
            del st.session_state["password"]

    # Login pertama
    if "password_correct" not in st.session_state:

        st.markdown(
            "<h1 class='glowing-title'>🔒 Copyright Fani</h1>",
            unsafe_allow_html=True
        )

        st.info(
            "Silakan masukkan password untuk mengakses MFF Database Manajemen."
        )

        st.text_input(
            "Password",
            type="password",
            key="password",
            on_change=password_entered
        )

        return False

    # Password salah
    if not st.session_state["password_correct"]:

        st.markdown(
            "<h1 class='glowing-title'>🔒 Copyright Fani</h1>",
            unsafe_allow_html=True
        )

        st.text_input(
            "Password",
            type="password",
            key="password",
            on_change=password_entered
        )

        st.error("⚠️ Password salah. Silakan coba lagi.")

        return False

    return True

# =====================================================
# LOAD DATA
# =====================================================

if check_password():

    try:

        response = (
            supabase
            .table("pendataan_akun")
            .select("*")
            .order("id", desc=True)
            .execute()
        )

        if response.data:

            df = pd.DataFrame(response.data)

            # Status Stok
            df["status_stok"] = (
                pd.to_numeric(
                    df["harga_jual"],
                    errors="coerce"
                )
                .fillna(0)
                .apply(
                    lambda x:
                    "🟢 Tersedia"
                    if x == 0
                    else "🔴 Terjual"
                )
            )

            # Urutan Kolom Database
            urutan_kolom = [

                "id",
                "tanggal_beli",
                "tanggal_jual",

                "status_stok",

                "nama_game",
                "nama_penjual",

                "email_akun",
                "password_akun",

                "wa_penjual",
                "fb_penjual",

                "harga_beli",

                "nama_pembeli",
                "no_wa",
                "akun_fb",

                "harga_jual",

                "screenshot",

                # TAMBAH_KOLOM_BARU_DISINI
            ]

            df = df[
                [
                    kolom
                    for kolom in urutan_kolom
                    if kolom in df.columns
                ]
            ]

        else:

            df = pd.DataFrame(
                columns=urutan_kolom
            )

    except Exception as error:

        st.error(
            f"Gagal memuat data: {error}"
        )

        st.stop()


    # =====================================================
    # SIDEBAR MENU
    # =====================================================

    menu_pilihan = st.sidebar.radio(
        "Menu Utama",
        [
            "📊 Dashboard Analitik",
            "📝 Input Transaksi",
            "🗄️ Database & Manajemen",

            # TAMBAH_MENU_BARU_DISINI
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Sistem MFF Pro v2.5")

    if st.sidebar.button(
        "🚪 Logout Sistem",
        use_container_width=True
    ):
        st.session_state.clear()
        st.rerun()


    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        "<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>",
        unsafe_allow_html=True
    )

    st.caption(
        "Akses Aman • Analitik Real-time • Data Sinkronisasi Cloud"
    )

    st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# DASHBOARD ANALITIK
# =====================================================

if menu_pilihan == "📊 Dashboard Analitik":

    st.markdown("### 📊 Ringkasan Eksekutif")

    if not df.empty:

        # =================================================
        # PERHITUNGAN DATA
        # =================================================

        df["harga_beli"] = (
            pd.to_numeric(
                df["harga_beli"],
                errors="coerce"
            ).fillna(0)
        )

        df["harga_jual"] = (
            pd.to_numeric(
                df["harga_jual"],
                errors="coerce"
            ).fillna(0)
        )

        df["profit_per_akun"] = (
            df["harga_jual"]
            - df["harga_beli"]
        )

        # =================================================
        # KPI DASHBOARD
        # =================================================

        stok = len(
            df[df["harga_jual"] == 0]
        )

        terjual = len(
            df[df["harga_jual"] > 0]
        )

        modal = df["harga_beli"].sum()

        nilai_stok = (
            df[df["harga_jual"] == 0]
            ["harga_beli"]
            .sum()
        )

        total_profit = (
            df[df["harga_jual"] > 0]
            ["profit_per_akun"]
            .sum()
        )

        # =================================================
        # PROFIT HARI INI
        # =================================================

        tanggal_hari_ini = (
            datetime.today()
            .strftime("%Y-%m-%d")
        )

        df_terjual = df[
            (df["harga_jual"] > 0)
            & (df["tanggal_jual"] != "-")
            & (df["tanggal_jual"].notna())
        ].copy()

        profit_hari_ini = (
            df_terjual[
                df_terjual["tanggal_jual"]
                == tanggal_hari_ini
            ]["profit_per_akun"]
            .sum()
        )

        # =================================================
        # NOTIFIKASI STOK LAMA
        # =================================================

        st.markdown(
            "#### 🚨 Notifikasi & Rekomendasi Tindakan"
        )

        df_stok_aktif = (
            df[df["harga_jual"] == 0]
            .copy()
        )

        akun_lama_count = 0

        if not df_stok_aktif.empty:

            try:

                df_stok_aktif["tgl_beli_dt"] = (
                    pd.to_datetime(
                        df_stok_aktif["tanggal_beli"],
                        format="%Y-%m-%d",
                        errors="coerce"
                    )
                )

                hari_ini = pd.to_datetime(
                    datetime.today().date()
                )

                df_stok_aktif["umur_stok"] = (
                    hari_ini
                    - df_stok_aktif["tgl_beli_dt"]
                ).dt.days

                akun_lama = (
                    df_stok_aktif[
                        df_stok_aktif["umur_stok"] > 7
                    ]
                )

                akun_lama_count = len(
                    akun_lama
                )

                if akun_lama_count > 0:

                    st.warning(
                        f"⚠️ Ada {akun_lama_count} akun "
                        f"yang sudah lebih dari 7 hari "
                        f"belum terjual."
                    )

                else:

                    st.success(
                        "✅ Semua stok aktif masih "
                        "dalam siklus perputaran sehat."
                    )

            except Exception:
                pass

        # TAMBAH_WIDGET_DASHBOARD_DISINI

        # =================================================
        # KARTU STATISTIK
        # =================================================

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "📦 In Stock",
            f"{stok} Akun"
        )

        c2.metric(
            "✅ Total Terjual",
            f"{terjual} Akun"
        )

        c3.metric(
            "💳 Total Modal Muter",
            f"Rp {modal:,.0f}"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        c4, c5, c6 = st.columns(3)

        c4.metric(
            "💎 Nilai Aset Mandek",
            f"Rp {nilai_stok:,.0f}"
        )

        c5.metric(
            "💰 Total Profit Bersih",
            f"Rp {total_profit:,.0f}"
        )

        c6.metric(
            "🚀 Profit Hari Ini",
            f"Rp {profit_hari_ini:,.0f}",
            delta="Cuan Masuk!"
            if profit_hari_ini > 0
            else None
        )

        # TAMBAH_METRIC_BARU_DISINI


        # =================================================
        # GRAFIK PROFIT HARIAN
        # =================================================

        st.markdown("---")

        st.markdown(
            "### 📈 Grafik Pertumbuhan Profit Harian"
        )

        if not df_terjual.empty:

            profit_harian = (
                df_terjual
                .groupby("tanggal_jual")
                ["profit_per_akun"]
                .sum()
            )

            st.area_chart(
                profit_harian,
                use_container_width=True,
                color="#00C9FF"
            )

        else:

            st.info(
                "Belum ada data penjualan untuk ditampilkan di grafik."
            )

        # TAMBAH_GRAFIK_BARU_DISINI


    else:

        st.info(
            "Sistem belum memiliki data transaksi untuk dianalisis."
        )

# =====================================================
# INPUT TRANSAKSI
# =====================================================

elif menu_pilihan == "📝 Input Transaksi":

    st.markdown("### 📝 Form Transaksi Baru")

    with st.form(
        "main_form",
        clear_on_submit=True
    ):

        col_a, col_b = st.columns(2)

        # =============================================
        # DATA PEMBELIAN
        # =============================================

        with col_a:

            st.subheader(
                "🛒 Pembelian (Dari Seller)"
            )

            t_beli = st.date_input(
                "Tanggal Beli"
            )

            game = st.text_input(
                "Nama Game*"
            )

            email = st.text_input(
                "Email Akun*"
            )

            pass_akun = st.text_input(
                "Password Akun*"
            )

            seller = st.text_input(
                "Nama Penjual"
            )

            wa_seller = st.text_input(
                "WA Penjual"
            )

            fb_seller = st.text_input(
                "FB Penjual"
            )

            h_beli = st.number_input(
                "Harga Beli (Rp)*",
                min_value=0
            )

            ss = st.file_uploader(
                "Upload Bukti Screenshot",
                type=["png", "jpg", "jpeg"]
            )

            # TAMBAH_FIELD_PEMBELIAN_DISINI


        # =============================================
        # DATA PENJUALAN
        # =============================================

        with col_b:

            st.subheader(
                "💰 Penjualan (Ke Customer)"
            )

            st.caption(
                "Abaikan bagian ini jika akun belum laku."
            )

            t_jual = st.date_input(
                "Tanggal Jual",
                value=None
            )

            buyer = st.text_input(
                "Nama Pembeli"
            )

            wa_buyer = st.text_input(
                "WA Pembeli"
            )

            fb_buyer = st.text_input(
                "FB Pembeli"
            )

            h_jual = st.number_input(
                "Harga Jual (Rp)",
                min_value=0
            )

            # TAMBAH_FIELD_PENJUALAN_DISINI


        # =============================================
        # SIMPAN DATA
        # =============================================

        submitted = st.form_submit_button(
            "💾 Simpan Data ke Cloud Database",
            use_container_width=True
        )

        if submitted:

            url = "-"

            # =========================================
            # UPLOAD SCREENSHOT
            # =========================================

            if ss:

                try:

                    filename = (
                        f"{game}_{ss.name}"
                        .replace(" ", "_")
                    )

                    supabase.storage.from_(
                        "screenshots"
                    ).upload(
                        filename,
                        ss.getvalue()
                    )

                    url = (
                        supabase.storage
                        .from_("screenshots")
                        .get_public_url(filename)
                    )

                except Exception:
                    pass

            # =========================================
            # PAYLOAD DATABASE
            # =========================================

            payload = {

                "tanggal_beli": str(t_beli),

                "nama_game": game,

                "email_akun": email,
                "password_akun": pass_akun,

                "nama_penjual": seller,
                "wa_penjual": wa_seller,
                "fb_penjual": fb_seller,

                "harga_beli": float(h_beli),

                "tanggal_jual":
                    str(t_jual)
                    if t_jual
                    else "-",

                "nama_pembeli": buyer,
                "no_wa": wa_buyer,
                "akun_fb": fb_buyer,

                "harga_jual": float(h_jual),

                "screenshot": url,

                # TAMBAH_KOLOM_DATABASE_DISINI
            }

            supabase.table(
                "pendataan_akun"
            ).insert(
                payload
            ).execute()

            st.success(
                "✅ Transaksi Berhasil Disimpan!"
            )

            st.rerun()

# =====================================================
# DATABASE & MANAJEMEN
# =====================================================

elif menu_pilihan == "🗄️ Database & Manajemen":

    st.markdown(
        "### 🗄️ Pusat Database"
    )

    # =================================================
    # FILTER & PENCARIAN
    # =================================================

    col_search, col_filter, col_export = st.columns(
        [2, 1, 1]
    )

    with col_search:

        search_query = st.text_input(
            "🔍 Cari Akun",
            placeholder="Ketik email atau nama..."
        )

    with col_filter:

        filter_status = st.selectbox(
            "🚦 Filter Status",
            [
                "Semua Data",
                "🟢 Tersedia",
                "🔴 Terjual"
            ]

            # TAMBAH_FILTER_BARU_DISINI
        )

    # =================================================
    # EXPORT DATA
    # =================================================

    with col_export:

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        csv = (
            df
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="📥 Download Excel/CSV",
            data=csv,
            file_name=(
                f"Database_MFF_"
                f"{datetime.today().strftime('%Y%m%d')}.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )

        # TAMBAH_EXPORT_BARU_DISINI

    # =================================================
    # FILTER DATA
    # =================================================

    df_display = df.copy()

    if filter_status != "Semua Data":

        df_display = df_display[
            df_display["status_stok"]
            == filter_status
        ]

    if search_query:

        mask = (
            df_display
            .astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search_query,
                    case=False
                )
            )
            .any(axis=1)
        )

        df_display = df_display[mask]

    # TAMBAH_LOGIKA_FILTER_DISINI

    # =================================================
    # TABEL DATABASE
    # =================================================

    st.dataframe(

        df_display,

        use_container_width=True,
        hide_index=True,

        column_config={

            "id": st.column_config.NumberColumn(
                "ID",
                format="%d"
            ),

            "status_stok": st.column_config.TextColumn(
                "Status Stok"
            ),

            "harga_beli": st.column_config.NumberColumn(
                "Harga Beli",
                format="Rp %d"
            ),

            "harga_jual": st.column_config.NumberColumn(
                "Harga Jual",
                format="Rp %d"
            ),

            "screenshot": st.column_config.LinkColumn(
                "Screenshot",
                display_text="Lihat Gambar"
            ),

            "profit_per_akun": None,

            # TAMBAH_KONFIGURASI_KOLOM_DISINI
        }
    )

    # TAMBAH_WIDGET_DATABASE_DISINI

    # =================================================
    # VIEWER MEDIA & GENERATOR TEKS
    # =================================================

    st.markdown("---")

    st.markdown(
        "### 🖼️ Viewer Media & 📢 Generator Teks"
    )

    if not df.empty:

        # =============================================
        # PILIH DATA
        # =============================================

        pilih_id_media = st.selectbox(
            "🎯 Pilih ID Akun",
            df["id"].tolist(),
            key="select_media"
        )

        row_media = (
            df[df["id"] == pilih_id_media]
            .iloc[0]
        )

        col_view, col_share = st.columns(2)

        # =============================================
        # VIEWER SCREENSHOT
        # =============================================

        with col_view:

            st.subheader(
                "🖼️ Viewer Screenshot"
            )

            screenshot_url = str(
                row_media["screenshot"]
            )

            if screenshot_url.startswith("http"):

                st.image(
                    screenshot_url,
                    caption=f"Bukti Transaksi ID: {pilih_id_media}",
                    use_container_width=True
                )

            else:

                st.info(
                    "Tidak ada screenshot untuk akun ini."
                )

        # =============================================
        # GENERATOR TEKS
        # =============================================

        with col_share:

            st.subheader(
                "📢 Format Cetak Share Teks"
            )

            status_raw = row_media["status_stok"]

            # =========================================
            # TEMPLATE READY STOCK
            # =========================================

            if "Tersedia" in status_raw:

                teks_laporan = (

                    f"🎮 READY STOCK ACCOUNT 🎮\n"
                    f"-----------------------------------\n"
                    f"🆔 ID Ref: {row_media['id']}\n"
                    f"📌 Game: {row_media['nama_game']}\n"
                    f"✉️ Email: {row_media['email_akun']}\n"
                    f"🔒 Status: AMAN & TERPERCAYA\n"
                    f"-----------------------------------\n"
                    f"DM / WA untuk info harga terbaik! 🔥"

                )

            # =========================================
            # TEMPLATE SOLD OUT
            # =========================================

            else:

                teks_laporan = (

                    f"✅ TRANSAKSI SUKSES (SOLD OUT) ✅\n"
                    f"-----------------------------------\n"
                    f"🆔 ID Ref: {row_media['id']}\n"
                    f"📌 Game: {row_media['nama_game']}\n"
                    f"👤 Buyer: {row_media['nama_pembeli']}\n"
                    f"💰 Nominal Jual: Rp {pd.to_numeric(row_media['harga_jual']):,.0f}\n"
                    f"-----------------------------------\n"
                    f"Maturnuwun! Percayakan kebutuhan game Anda hanya di Copyright Fani. 🙏🌟"

                )

            st.caption(
                "Klik tombol copy di pojok kanan atas."
            )

            st.code(
                teks_laporan,
                language="text"
            )

            # TAMBAH_TEMPLATE_PROMOSI_DISINI

    # =================================================
    # KELOLA DATA
    # =================================================

    st.markdown("---")

    st.markdown(
        "### ⚙️ Kelola Data Spesifik (Edit / Hapus)"
    )

    if not df.empty:

        tab_edit, tab_hapus = st.tabs(
            [
                "📝 Edit Data",
                "🗑️ Hapus Data"
            ]
        )

        # =============================================
        # TAB EDIT DATA
        # =============================================

        with tab_edit:

            # =========================================
            # PILIH DATA
            # =========================================

            eid = st.selectbox(
                "Pilih ID Akun yang ingin diedit",
                df["id"].tolist(),
                key="select_edit"
            )

            row_edit = (
                df[df["id"] == eid]
                .iloc[0]
            )

            # =========================================
            # FORM EDIT
            # =========================================

            with st.form(f"edit_form_{eid}"):

                st.info(
                    f"Silakan perbarui rincian data untuk ID: {eid}"
                )

                e_col1, e_col2 = st.columns(2)

                # =====================================
                # DATA PEMBELIAN
                # =====================================

                with e_col1:

                    st.caption(
                        "🛍️ PEMBELIAN (MODAL)"
                    )

                    try:
                        val_tb = datetime.strptime(
                            str(row_edit["tanggal_beli"]),
                            "%Y-%m-%d"
                        ).date()

                    except Exception:
                        val_tb = datetime.today().date()

                    etb = st.date_input(
                        "Tanggal Beli",
                        value=val_tb
                    )

                    eg = st.text_input(
                        "Game",
                        value=row_edit["nama_game"]
                    )

                    ee = st.text_input(
                        "Email",
                        value=row_edit["email_akun"]
                    )

                    epa = st.text_input(
                        "Password Akun",
                        value=row_edit.get(
                            "password_akun",
                            "-"
                        )
                    )

                    es = st.text_input(
                        "Seller",
                        value=row_edit.get(
                            "nama_penjual",
                            ""
                        )
                    )

                    ews = st.text_input(
                        "WA Seller",
                        value=row_edit.get(
                            "wa_penjual",
                            ""
                        )
                    )

                    efs = st.text_input(
                        "FB Seller",
                        value=row_edit.get(
                            "fb_penjual",
                            ""
                        )
                    )

                    ehb = st.number_input(
                        "Harga Beli",
                        value=float(
                            row_edit["harga_beli"]
                        )
                    )

                    # TAMBAH_FIELD_PEMBELIAN_EDIT_DISINI

                # =====================================
                # DATA PENJUALAN
                # =====================================

                with e_col2:

                    st.caption(
                        "💰 PENJUALAN (PROFIT)"
                    )

                    try:
                        val_tj = datetime.strptime(
                            str(row_edit["tanggal_jual"]),
                            "%Y-%m-%d"
                        ).date()

                    except Exception:
                        val_tj = None

                    etj = st.date_input(
                        "Tanggal Jual",
                        value=val_tj
                    )

                    eb = st.text_input(
                        "Buyer",
                        value=row_edit["nama_pembeli"]
                    )

                    ewb = st.text_input(
                        "WA Buyer",
                        value=row_edit["no_wa"]
                    )

                    efb = st.text_input(
                        "FB Buyer",
                        value=row_edit.get(
                            "akun_fb",
                            ""
                        )
                    )

                    ehj = st.number_input(
                        "💵 Harga Jual",
                        value=float(
                            row_edit["harga_jual"]
                        )
                    )

                    # TAMBAH_FIELD_PENJUALAN_EDIT_DISINI

                # =====================================
                # TOMBOL UPDATE
                # =====================================

                st.markdown(
                    "<br>",
                    unsafe_allow_html=True
                )

                update_clicked = st.form_submit_button(
                    "💾 Update Seluruh Data",
                    use_container_width=True
                )

                if update_clicked:

                    # ===============================
                    # PAYLOAD UPDATE DATABASE
                    # ===============================

                    upd = {

                        # DATA PEMBELIAN
                        "tanggal_beli":
                            str(etb) if etb else "-",

                        "nama_game": eg,

                        "email_akun": ee,

                        "password_akun": epa,

                        "nama_penjual": es,

                        "wa_penjual": ews,

                        "fb_penjual": efs,

                        "harga_beli": ehb,

                        # DATA PENJUALAN
                        "tanggal_jual":
                            str(etj) if etj else "-",

                        "nama_pembeli": eb,

                        "no_wa": ewb,

                        "akun_fb": efb,

                        "harga_jual": ehj,

                        # TAMBAH_KOLOM_UPDATE_DISINI
                    }

                    supabase.table(
                        "pendataan_akun"
                    ).update(
                        upd
                    ).eq(
                        "id",
                        eid
                    ).execute()

                    st.success(
                        "✅ Rincian data berhasil diperbarui!"
                    )

                    st.rerun()

        # =============================================
        # TAB HAPUS DATA
        # =============================================

        with tab_hapus:

            st.warning(
                "Data yang dihapus tidak dapat dikembalikan."
            )

            did = st.number_input(
                "Masukkan ID yang akan dihapus",
                min_value=0,
                step=1,
                value=int(df["id"].iloc[0])
            )

            # =========================================
            # TOMBOL HAPUS
            # =========================================

            delete_clicked = st.button(
                "🚨 Hapus Permanen",
                type="primary",
                use_container_width=True
            )

            if delete_clicked:

                supabase.table(
                    "pendataan_akun"
                ).delete().eq(
                    "id",
                    did
                ).execute()

                st.success(
                    f"✅ ID {did} berhasil dihapus."
                )

                st.rerun()