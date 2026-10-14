import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="MFF Database Pro", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- 2. DESAIN UI KUSTOM (THEME: CLEAN PROFESSIONAL DASHBOARD) ---
background_image_url = "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?q=80&w=2071&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    /* Background Utama ala Enterprise Clean */
    .stApp {{
        background-color: #f4f7f6;
        background-image: linear-gradient(rgba(244, 247, 246, 0.92), rgba(244, 247, 246, 0.92)), url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > header {{ background-color: transparent; }}
    
    /* Container Konten Utama */
    .block-container {{
        background-color: #ffffff; 
        padding: 2rem 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
        border: 1px solid #e2e8f0;
    }}

    /* Sidebar Profesional Bergaya Gelap Elegan */
    [data-testid="stSidebar"] {{
        background: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #f8fafc !important;
    }}

    /* Judul Utama */
    .dashboard-title {{
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0px;
    }}

    /* Kotak Metrik Bersih (Card Style) */
    [data-testid="stMetric"] {{
        background: #ffffff;
        border: 1px solid #e2e8f0; 
        padding: 16px; 
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
    }}
    [data-testid="stMetric"]:hover {{
        border-color: #3b82f6;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }}
    [data-testid="stMetric"] label {{
        color: #64748b !important;
        font-weight: 500 !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: #0f172a !important;
        font-weight: 700 !important;
    }}

    /* Banner Informatif Biru */
    .hero-banner {{
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: white;
        margin-top: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
    }}
    .hero-banner h3 {{
        margin: 0;
        font-weight: 700;
        font-size: 22px;
        color: white;
    }}
    .hero-banner p {{
        margin: 8px 0 0 0;
        color: #e0e7ff;
        font-size: 14px;
    }}

    /* Tombol Kustom */
    .stButton button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        transition: all 0.2s ease !important;
    }}
    .stButton button:hover {{
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
        background-color: #eff6ff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. KONEKSI SUPABASE ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 4. SISTEM KEAMANAN ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "131313":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='color: #0f172a;'>🔒 © 2026 NiFa. All Rights Reserved.</h2>", unsafe_allow_html=True)
        st.info("Tetap lapar, tetap bodoh.")
        st.text_input("Enter your password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='color: #0f172a;'>🔒 © 2026 NiFa. All Rights Reserved.</h2>", unsafe_allow_html=True)
        st.text_input("Enter your password:", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Wrong password. Please try again..")
        return False
    return True

# --- 5. APLIKASI UTAMA ---
if check_password():
    
    try:
        response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(
                lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual"
            )
            urutan_kolom = [
                "id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", 
                "nama_penjual", "email_akun", "password_akun", "wa_penjual", 
                "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", 
                "akun_fb", "harga_jual", "keterangan", "screenshot"
            ]
            kolom_tersedia = [kol for kol in urutan_kolom if kol in df.columns]
            df = df[kolom_tersedia]
        else:
            df = pd.DataFrame(columns=["id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    # --- MENU SIDEBAR ---
    st.sidebar.markdown("### 🏛️ MFF BANK SYSTEM")
    st.sidebar.caption("Digitalisasi & Manajemen Akun")
    st.sidebar.markdown("---")
    
    if "menu_aktif" not in st.session_state:
        st.session_state["menu_aktif"] = "📊 Dashboard"

    menu_pilihan = st.sidebar.radio(
        "Menu Utama:",
        ["📊 Dashboard", "📝 Input Transaksi", "🗄️ Database MFF", "👥 Antrian Buyer"],
        index=["📊 Dashboard", "📝 Input Transaksi", "🗄️ Database MFF", "👥 Antrian Buyer"].index(st.session_state["menu_aktif"]),
        label_visibility="collapsed"
    )
    st.session_state["menu_aktif"] = menu_pilihan
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Super Admin • MFF Pro v3.0")
    if st.sidebar.button("🚪 Logout Sistem", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # Header Atas Ala Dashboard Perusahaan
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown("<p class='dashboard-title'>Dashboard Ringkasan</p>", unsafe_allow_html=True)
    with top_col2:
        tanggal_sekarang = datetime.today().strftime('%A, %d %B %Y')
        st.markdown(f"<p style='text-align: right; color: #64748b; font-size: 13px; margin: 0;'>{tanggal_sekarang}<br><b>MFF Management Division</b></p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # HALAMAN 1: DASHBOARD
    # ==========================================
    if menu_pilihan == "📊 Dashboard":
        if not df.empty:
            df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
            df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
            df['profit_per_akun'] = df['harga_jual'] - df['harga_beli'] 

            stok = len(df[df['harga_jual'] == 0])
            terjual = len(df[df['harga_jual'] > 0])
            modal = df['harga_beli'].sum()
            nilai_stok = df[df['harga_jual'] == 0]['harga_beli'].sum()
            total_profit = df[df['harga_jual'] > 0]['profit_per_akun'].sum()

            tanggal_hari_ini = datetime.today().strftime('%Y-%m-%d')
            df_terjual = df[(df['harga_jual'] > 0) & (df['tanggal_jual'] != "-") & (df['tanggal_jual'].notna())].copy()
            df_terjual['tanggal_jual_str'] = pd.to_datetime(df_terjual['tanggal_jual'], errors='coerce').dt.strftime('%Y-%m-%d')
            profit_hari_ini = df_terjual[df_terjual['tanggal_jual_str'] == tanggal_hari_ini]['profit_per_akun'].sum()

            # Kartu Metrik Ringkasan (4 Kolom Elegan)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📦 TOTAL STOK", f"{stok} Akun")
            c2.metric("✅ TERJUAL", f"{terjual} Akun")
            c3.metric("💳 MODAL MUTER", f"Rp {modal:,.0f}")
            c4.metric("💰 PROFIT BERSIH", f"Rp {total_profit:,.0f}")

            # Banner Informatif
            st.markdown(
                """
                <div class="hero-banner">
                    <h3>Bank Data & Manajemen Akun Game MFF</h3>
                    <p>Pusat digitalisasi inventaris akun, rekapitulasi modal, dan pemantauan profit harian serta bulanan secara terpusat dan real-time.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- RESUME PROFIT BULANAN ---
            st.markdown("### 📅 Resume Profit Bulanan")
            if not df_terjual.empty:
                df_terjual['bulan_jual'] = pd.to_datetime(df_terjual['tanggal_jual'], errors='coerce').dt.to_period('M').astype(str)
                daftar_bulan = sorted(df_terjual['bulan_jual'].unique(), reverse=True)
                
                col_sel_bln, col_kosong = st.columns([1, 2])
                with col_sel_bln:
                    pilih_bulan = st.selectbox("🎯 Pilih Periode Bulan:", daftar_bulan)
                
                df_bulan_pilihan = df_terjual[df_terjual['bulan_jual'] == pilih_bulan]
                total_profit_bulan_ini = df_bulan_pilihan['profit_per_akun'].sum()
                jumlah_terjual_bulan_ini = len(df_bulan_pilihan)
                
                mb1, mb2 = st.columns(2)
                mb1.metric(f"📦 Akun Terjual ({pilih_bulan})", f"{jumlah_terjual_bulan_ini} Akun")
                mb2.metric(f"💰 Total Profit Bulan {pilih_bulan}", f"Rp {total_profit_bulan_ini:,.0f}")
                
                with st.expander(f"🔍 Lihat Rincian Transaksi Bulan {pilih_bulan}"):
                    tabel_detail_bulan = df_bulan_pilihan[["id", "tanggal_jual", "nama_game", "nama_pembeli", "harga_jual", "profit_per_akun"]].copy()
                    tabel_detail_bulan['harga_jual'] = tabel_detail_bulan['harga_jual'].apply(lambda x: f"Rp {x:,.0f}")
                    tabel_detail_bulan['profit_per_akun'] = tabel_detail_bulan['profit_per_akun'].apply(lambda x: f"Rp {x:,.0f}")
                    tabel_detail_bulan.columns = ["ID", "Tanggal Jual", "Game", "Pembeli", "Harga Jual", "Profit Bersih"]
                    st.dataframe(tabel_detail_bulan, use_container_width=True, hide_index=True)
            else:
                st.info("Belum ada data penjualan bulanan untuk dirangkum.")

            st.markdown("---")
            st.markdown("### 📈 Grafik Pertumbuhan Profit Harian")
            if not df_terjual.empty:
                profit_harian = df_terjual.groupby('tanggal_jual_str')['profit_per_akun'].sum()
                st.area_chart(profit_harian, use_container_width=True, color="#3b82f6")
            else:
                st.info("Belum ada data penjualan untuk ditampilkan di grafik.")
        else:
            st.info("Sistem belum memiliki data transaksi untuk dianalisis.")

    # ==========================================
    # HALAMAN 2: INPUT TRANSAKSI
    # ==========================================
    elif menu_pilihan == "📝 Input Transaksi":
        st.markdown("### 📝 Form Input Transaksi Baru")
        with st.form("main_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("🛒 Pembelian (Dari Seller)")
                t_beli = st.date_input("Tanggal Beli")
                game = st.text_input("Nama Game*")
                col_em, col_pw = st.columns(2)
                with col_em: email = st.text_input("Email Akun*")
                with col_pw: pass_akun = st.text_input("Password Akun*")
                seller = st.text_input("Nama Penjual")
                col_was, col_fbs = st.columns(2)
                with col_was: wa_seller = st.text_input("WA Penjual")
                with col_fbs: fb_seller = st.text_input("FB Penjual")
                h_beli = st.number_input("Harga Beli (Rp)*", min_value=0)
                ss = st.file_uploader("Upload Bukti Screenshot", type=['png', 'jpg', 'jpeg'])
                
            with col_b:
                st.subheader("💰 Penjualan (Ke Customer)")
                t_jual = st.date_input("Tanggal Jual", value=None)
                buyer = st.text_input("Nama Pembeli")
                col_wab, col_fbb = st.columns(2)
                with col_wab: wa_buyer = st.text_input("WA Pembeli")
                with col_fbb: fb_buyer = st.text_input("FB Pembeli")
                h_jual = st.number_input("Harga Jual (Rp)", min_value=0)
                keterangan = st.text_area("Keterangan Tambahan")

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.form_submit_button("💾 Simpan Data ke Cloud Database", use_container_width=True):
                url = "-"
                if ss:
                    try:
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        fname = f"{timestamp}_{game}_{ss.name}".replace(" ","_")
                        supabase.storage.from_("screenshots").upload(fname, ss.getvalue())
                        url = supabase.storage.from_("screenshots").get_public_url(fname)
                    except: pass
                
                payload = {
                    "tanggal_beli": str(t_beli), "nama_game": game, "email_akun": email, "password_akun": pass_akun, 
                    "nama_penjual": seller, "wa_penjual": wa_seller, "fb_penjual": fb_seller,
                    "harga_beli": float(h_beli), "tanggal_jual": str(t_jual) if t_jual else "-",
                    "nama_pembeli": buyer, "no_wa": wa_buyer, "akun_fb": fb_buyer, "harga_jual": float(h_jual), 
                    "keterangan": keterangan, "screenshot": url
                }
                supabase.table("pendataan_akun").insert(payload).execute()
                st.success("✅ Transaksi Berhasil Disimpan!")
                st.rerun()

    # ==========================================
    # HALAMAN 3: DATABASE MFF
    # ==========================================
    elif menu_pilihan == "🗄️ Database MFF":
        st.markdown("### 🗄️ Pusat Database & Manajemen Akun")
        
        col_search, col_filter, col_export = st.columns([2, 1, 1])
        with col_search:
            search_query = st.text_input("🔍 Cari Akun:", placeholder="Ketik email atau nama...")
        with col_filter:
            filter_status = st.selectbox("🚦 Filter Status", ["Semua Data", "🟢 Tersedia", "🔴 Terjual"])
        with col_export:
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Excel/CSV", data=csv, file_name=f"Database_MFF_{datetime.today().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
        
        df_display = df.copy()
        if filter_status != "Semua Data":
            df_display = df_display[df_display['status_stok'] == filter_status]
        if search_query:
            mask = df_display.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            df_display = df_display[mask]
        
        st.dataframe(
            df_display,
            use_container_width=True, hide_index=True, 
            column_config={
                "harga_jual": st.column_config.NumberColumn("Harga Jual", format="Rp %d"),
                "keterangan": st.column_config.TextColumn("Keterangan", width="medium"),
                "screenshot": st.column_config.LinkColumn("Screenshot", display_text="Lihat Gambar", help="Klik untuk membuka gambar di tab baru"),
                "profit_per_akun": None 
            }
        )
        
        st.markdown("---")
        st.markdown("### 🖼️ Viewer Media & 📢 Generator Teks")
        if not df.empty:
            pilih_id_media = st.selectbox("🎯 Pilih ID Akun untuk melihat gambar atau membuat teks promosi:", df['id'].tolist(), key="select_media")
            row_media = df[df['id'] == pilih_id_media].iloc[0]
            
            col_view, col_share = st.columns(2)
            with col_view:
                st.subheader("🖼️ Viewer Screenshot")
                if str(row_media['screenshot']).startswith("http"):
                    st.image(row_media['screenshot'], caption=f"Bukti Transaksi ID: {pilih_id_media}", use_container_width=True)
                else:
                    st.info("Tidak ada screenshot untuk akun ini.")
            
            with col_share:
                st.subheader("📢 Format Cetak Share Teks")
                status_raw = row_media['status_stok']
                if "Tersedia" in status_raw:
                    teks_laporan = (
                        f"🎮 **READY STOCK ACCOUNT** 🎮\n"
                        f"-----------------------------------\n"
                        f"🆔 ID Ref: {row_media['id']}\n"
                        f"📌 Game: {row_media['nama_game']}\n"
                        f"✉️ Email: {row_media['email_akun']}\n"
                        f"🔒 Status: AMAN & TERPERCAYA\n"
                        f"-----------------------------------\n"
                        f"DM / WA untuk info harga terbaik! 🔥"
                    )
                else:
                    teks_laporan = (
                        f"✅ **TRANSAKSI SUKSES (SOLD OUT)** ✅\n"
                        f"-----------------------------------\n"
                        f"🆔 ID Ref: {row_media['id']}\n"
                        f"📌 Game: {row_media['nama_game']}\n"
                        f"👤 Buyer: {row_media['nama_pembeli']}\n"
                        f"💰 Nominal Jual: Rp {pd.to_numeric(row_media['harga_jual']):,.0f}\n"
                        f"-----------------------------------\n"
                        f"Maturnuwun! Percayakan kebutuhan game Anda hanya di © 2026 NiFa. 🙏🌟"
                    )
                st.code(teks_laporan, language="text")

        st.markdown("---")
        st.markdown("### ⚙️ Kelola Data Spesifik (Edit / Hapus)")
        if not df.empty:
            tab_edit, tab_hapus = st.tabs(["📝 Edit Data", "🗑️ Hapus Data"])
            
            with tab_edit:
                eid = st.selectbox("Pilih ID Akun yang ingin Anda edit:", df['id'].tolist(), key="select_edit")
                row_edit = df[df['id'] == eid].iloc[0]
                
                with st.form(f"edit_form_{eid}"):
                    st.info(f"Perbarui rincian data untuk ID: {eid}")
                    e_col1, e_col2 = st.columns(2)
                            
                    with e_col1:
                        st.caption("🛍️ PEMBELIAN (MODAL)")
                        try: val_tb = datetime.strptime(str(row_edit['tanggal_beli']), "%Y-%m-%d").date()
                        except: val_tb = datetime.today().date()
                        etb = st.date_input("Tanggal Beli", value=val_tb)
                        eg = st.text_input("Game", value=row_edit['nama_game'])
                        ee = st.text_input("Email", value=row_edit['email_akun'])
                        epa = st.text_input("Password Akun", value=row_edit.get('password_akun','-')) 
                        es = st.text_input("Seller", value=row_edit.get('nama_penjual',''))
                        ews = st.text_input("WA Seller", value=row_edit.get('wa_penjual',''))
                        efs = st.text_input("FB Seller", value=row_edit.get('fb_penjual',''))
                        ehb = st.number_input("Harga Beli", value=float(row_edit['harga_beli']))
                                
                    with e_col2:
                        st.caption("💰 PENJUALAN (PROFIT)")
                        try: val_tj = datetime.strptime(str(row_edit['tanggal_jual']), "%Y-%m-%d").date()
                        except: val_tj = None
                        etj = st.date_input("Tanggal Jual", value=val_tj)
                        eb = st.text_input("Nama Pembeli", value=row_edit.get('nama_pembeli', ''))
                        ewb = st.text_input("No WA Pembeli", value=row_edit.get('no_wa', ''))
                        efb = st.text_input("Akun FB Pembeli", value=row_edit.get('akun_fb', ''))
                        ehj = st.number_input("💵 Harga Jual", value=float(row_edit['harga_jual']))
                        eketerangan = st.text_area("Keterangan", value=row_edit.get('keterangan', ''))
                        new_ss = st.file_uploader("Ganti Screenshot (Opsional)", type=['png', 'jpg', 'jpeg'])
                                
                    if st.form_submit_button("💾 Update Seluruh Data", use_container_width=True):
                        url_final = row_edit['screenshot'] 
                        if new_ss:
                            try:
                                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                                fname = f"{timestamp}_{eg}_{new_ss.name}".replace(" ", "_")
                                supabase.storage.from_("screenshots").upload(fname, new_ss.getvalue())
                                url_final = supabase.storage.from_("screenshots").get_public_url(fname)
                            except Exception as e:
                                st.error(f"Gagal upload gambar: {e}")

                        upd = {
                            "tanggal_beli": str(etb), "nama_game": eg, "email_akun": ee, "password_akun": epa,
                            "nama_penjual": es, "wa_penjual": ews, "fb_penjual": efs, "harga_beli": ehb,
                            "tanggal_jual": str(etj), "nama_pembeli": eb, "no_wa": ewb, "akun_fb": efb,
                            "harga_jual": ehj, "keterangan": eketerangan, "screenshot": url_final
                        }
                        supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                        st.success("Data berhasil diupdate!")
                        st.rerun()

            with tab_hapus:
                did = st.number_input("Masukkan ID yang akan dihapus:", min_value=0, step=1, value=int(df['id'].iloc[0]) if not df.empty else 0)
                if st.button("🚨 Hapus Permanen", type="primary"):
                    supabase.table("pendataan_akun").delete().eq("id", did).execute()
                    st.success(f"ID {did} Terhapus!")
                    st.rerun()

    # ==========================================
    # HALAMAN 4: ANTRIAN BUYER
    # ==========================================
    elif menu_pilihan == "👥 Antrian Buyer":
        st.markdown("### 👥 Detail Antrian Buyer")
        st.info("Kelola, pantau, edit, dan hapus daftar antrian calon pembeli akun game.")
        
        with st.form("form_antrian_buyer", clear_on_submit=True):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                nama_calon_buyer = st.text_input("Nama Calon Buyer*")
                kontak_buyer = st.text_input("No WA / Kontak*")
                input_akun_fb = st.text_input("Akun FB Buyer")
            with col_b2:
                game_diincar = st.text_input("Game / Akun yang Diincar*")
                catatan_buyer = st.text_area("Catatan / Request Khusus")
            
            if st.form_submit_button("➕ Tambah ke Antrian", use_container_width=True):
                if nama_calon_buyer and game_diincar:
                    try:
                        payload_buyer = {
                            "tanggal_input": datetime.today().strftime('%Y-%m-%d'),
                            "nama_buyer": nama_calon_buyer, "kontak": kontak_buyer,
                            "game_diincar": game_diincar, "catatan": catatan_buyer if catatan_buyer else "-",
                            "akun_fb": input_akun_fb if input_akun_fb else "-"
                        }
                        supabase.table("antrian_buyer").insert(payload_buyer).execute()
                        st.success(f"Berhasil menambahkan {nama_calon_buyer} ke dalam antrian buyer!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menyimpan antrian: {e}")
                else:
                    st.warning("Mohon lengkapi Nama Calon Buyer dan Game yang diincar.")

        st.markdown("---")
        st.markdown("### 📋 Daftar Tabel Antrian Buyer Aktif")
        
        try:
            res_buyer = supabase.table("antrian_buyer").select("*").order('id', desc=True).execute()
            if res_buyer.data:
                df_buyer = pd.DataFrame(res_buyer.data)
                kolom_buyer_order = ["id", "tanggal_input", "nama_buyer", "kontak", "game_diincar", "catatan", "akun_fb"]
                kolom_b_tersedia = [col for col in kolom_buyer_order if col in df_buyer.columns]
                df_buyer = df_buyer[kolom_b_tersedia]
                
                st.dataframe(df_buyer, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("### ⚙️ Kelola Antrian (Edit / Hapus)")
                tab_edit_b, tab_hapus_b = st.tabs(["📝 Edit Antrian", "🗑️ Hapus Antrian"])
                
                with tab_edit_b:
                    eid_b = st.selectbox("Pilih ID Antrian yang ingin diedit:", df_buyer['id'].tolist(), key="select_edit_buyer")
                    row_edit_b = df_buyer[df_buyer['id'] == eid_b].iloc[0]
                    
                    with st.form(f"edit_form_buyer_{eid_b}"):
                        st.info(f"Perbarui data antrian untuk ID: {eid_b}")
                        eb_col1, eb_col2 = st.columns(2)
                        
                        with eb_col1:
                            try: val_t_input = datetime.strptime(str(row_edit_b['tanggal_input']), "%Y-%m-%d").date()
                            except: val_t_input = datetime.today().date()
                            e_tgl = st.date_input("Tanggal Input", value=val_t_input)
                            e_nama = st.text_input("Nama Calon Buyer", value=row_edit_b.get('nama_buyer', ''))
                            e_kontak = st.text_input("No WA / Kontak", value=row_edit_b.get('kontak', ''))
                        
                        with eb_col2:
                            e_game = st.text_input("Game yang Diincar", value=row_edit_b.get('game_diincar', ''))
                            e_catatan = st.text_area("Catatan", value=row_edit_b.get('catatan', ''))
                            e_akunfb = st.text_input("Akun FB", value=row_edit_b.get('akun_fb', '') if pd.notna(row_edit_b.get('akun_fb')) else '')
                        
                        if st.form_submit_button("💾 Update Data Antrian", use_container_width=True):
                            upd_buyer = {
                                "tanggal_input": str(e_tgl), "nama_buyer": e_nama, "kontak": e_kontak,
                                "game_diincar": e_game, "catatan": e_catatan, "akun_fb": e_akunfb
                            }
                            supabase.table("antrian_buyer").update(upd_buyer).eq("id", eid_b).execute()
                            st.success("Data antrian berhasil diperbarui!")
                            st.rerun()

                with tab_hapus_b:
                    did_b = st.number_input("Masukkan ID Antrian yang akan dihapus:", min_value=0, step=1, value=int(df_buyer['id'].iloc[0]))
                    if st.button("🚨 Hapus Permanen Antrian", type="primary", key="btn_hapus_buyer"):
                        supabase.table("antrian_buyer").delete().eq("id", did_b).execute()
                        st.success(f"ID Antrian {did_b} berhasil dihapus!")
                        st.rerun()
            else:
                st.info("Belum ada data antrian buyer saat ini.")
        except Exception as e:
            st.warning(f"Gagal memuat data antrian: {e}")