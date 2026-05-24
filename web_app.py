import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- 2. DESAIN UI KUSTOM TINGKAT LANJUT ---
background_image_url = "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?q=80&w=2071&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > header {{ background-color: transparent; }}
    
    .block-container {{
        background-color: rgba(14, 17, 23, 0.85); 
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0b0f19 0%, #161b22 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        position: relative;
        overflow: hidden;
    }}
    
    [data-testid="stSidebar"]::before {{
        content: ""; position: absolute; top: -100px; left: -100px; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0, 201, 255, 0.15) 0%, transparent 70%); border-radius: 50%; z-index: 0; pointer-events: none;
    }}

    [data-testid="stSidebar"]::after {{
        content: ""; position: absolute; bottom: -100px; right: -100px; width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(146, 254, 157, 0.1) 0%, transparent 70%); border-radius: 50%; z-index: 0; pointer-events: none;
    }}

    .stRadio > div {{ gap: 12px; position: relative; z-index: 1; }}
    .stRadio > div > label {{
        background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important; padding: 12px 15px !important; transition: all 0.3s ease !important; cursor: pointer;
    }}
    .stRadio > div > label:hover {{
        background: linear-gradient(90deg, rgba(0, 201, 255, 0.1) 0%, transparent 100%) !important;
        border-color: rgba(0, 201, 255, 0.4) !important; transform: translateX(8px);
    }}

    .glowing-title {{
        font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; text-shadow: 0px 0px 20px rgba(0, 201, 255, 0.3);
    }}

    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15); transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-7px); border-color: rgba(0, 201, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 201, 255, 0.2); background: linear-gradient(145deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
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
        st.markdown("<h1 class='glowing-title'>🔒 Copyright Fani</h1>", unsafe_allow_html=True)
        st.info("Silakan masukkan password untuk mengakses MFF Database Manajemen.")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h1 class='glowing-title'>🔒 Copyright Fani</h1>", unsafe_allow_html=True)
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Password salah. Silakan coba lagi.")
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
                "id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", 
                "email_akun", "password_akun", "wa_penjual", "fb_penjual", 
                "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "keterangan", "screenshot"
            ]
            kolom_tersedia = [kol for kol in urutan_kolom if kol in df.columns]
            df = df[kolom_tersedia]
        else:
            df = pd.DataFrame(columns=["id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    # --- MENU SIDEBAR ---
    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu_pilihan = st.sidebar.radio(
        "Menu Utama:",
        ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Sistem MFF Pro v2.5")
    if st.sidebar.button("🚪 Logout Sistem", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>", unsafe_allow_html=True)
    st.caption("Akses Aman • Analitik Real-time • Data Sinkronisasi Cloud")
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # HALAMAN 1: DASHBOARD
    # ==========================================
    if menu_pilihan == "📊 Dashboard Analitik":
        st.markdown("### 📊 Ringkasan Eksekutif")
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
            profit_hari_ini = df_terjual[df_terjual['tanggal_jual'] == tanggal_hari_ini]['profit_per_akun'].sum()

            st.markdown("#### 🚨 Notifikasi & Rekomendasi Tindakan")
            df_stok_aktif = df[df['harga_jual'] == 0].copy()
            akun_lama_count = 0
            
            if not df_stok_aktif.empty:
                try:
                    df_stok_aktif['tgl_beli_dt'] = pd.to_datetime(df_stok_aktif['tanggal_beli'], format='%Y-%m-%d', errors='coerce')
                    hari_ini_dt = pd.to_datetime(datetime.today().date())
                    df_stok_aktif['umur_stok'] = (hari_ini_dt - df_stok_aktif['tgl_beli_dt']).dt.days
                    akun_lama = df_stok_aktif[df_stok_aktif['umur_stok'] > 7]
                    akun_lama_count = len(akun_lama)
                    
                    if akun_lama_count > 0:
                        st.warning(f"⚠️ **Perhatian:** Ada **{akun_lama_count} akun** yang sudah mengendap lebih dari 7 hari belum terjual. Direkomendasikan untuk melakukan promosi ulang atau penyesuaian harga di menu Manajemen.")
                    else:
                        st.success("✅ Semua stok aktif Anda masih dalam siklus perputaran yang sehat (kurang dari 7 hari). Bagus!")
                except:
                    pass

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("📦 In Stock", f"{stok} Akun")
            c2.metric("✅ Total Terjual", f"{terjual} Akun")
            c3.metric("💳 Total Modal Muter", f"Rp {modal:,.0f}")
            st.markdown("<br>", unsafe_allow_html=True)
            c4, c5, c6 = st.columns(3)
            c4.metric("💎 Nilai Aset Mandek", f"Rp {nilai_stok:,.0f}")
            c5.metric("💰 Total Profit Bersih", f"Rp {total_profit:,.0f}")
            c6.metric("🚀 Profit Hari Ini", f"Rp {profit_hari_ini:,.0f}", delta="Cuan Masuk!" if profit_hari_ini > 0 else None)

            st.markdown("---")
            st.markdown("### 📈 Grafik Pertumbuhan Profit Harian")
            if not df_terjual.empty:
                profit_harian = df_terjual.groupby('tanggal_jual')['profit_per_akun'].sum()
                st.area_chart(profit_harian, use_container_width=True, color="#00C9FF")
            else:
                st.info("Belum ada data penjualan untuk ditampilkan di grafik.")
        else:
            st.info("Sistem belum memiliki data transaksi untuk dianalisis.")

    # ==========================================
    # HALAMAN 2: INPUT
    # ==========================================
    elif menu_pilihan == "📝 Input Transaksi":
        st.markdown("### 📝 Form Transaksi Baru")
        with st.form("main_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("🛒 Pembelian (Dari Seller)")
                t_beli = st.date_input("Tanggal Beli")
                game = st.text_input("Nama Game* (Misal: MFF)")
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
                st.caption("Abaikan bagian ini jika akun belum laku.")
                t_jual = st.date_input("Tanggal Jual", value=None)
                buyer = st.text_input("Nama Pembeli")
                col_wab, col_fbb = st.columns(2)
                with col_wab: wa_buyer = st.text_input("WA Pembeli")
                with col_fbb: fb_buyer = st.text_input("FB Pembeli")
                h_jual = st.number_input("Harga Jual (Rp)", min_value=0)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 Simpan Data ke Cloud Database", use_container_width=True):
                url = "-"
                if ss:
                    try:
                        fname = f"{game}_{ss.name}".replace(" ","_")
                        supabase.storage.from_("screenshots").upload(fname, ss.getvalue())
                        url = supabase.storage.from_("screenshots").get_public_url(fname)
                    except: pass
                payload = {
                    "tanggal_beli": str(t_beli), "nama_game": game, "email_akun": email, "password_akun": pass_akun, 
                    "nama_penjual": seller, "wa_penjual": wa_seller, "fb_penjual": fb_seller,
                    "harga_beli": float(h_beli), "tanggal_jual": str(t_jual) if t_jual else "-",
                    "nama_pembeli": buyer, "no_wa": wa_buyer, "akun_fb": fb_buyer, "harga_jual": float(h_jual), "screenshot": url
                }
                supabase.table("pendataan_akun").insert(payload).execute()
                st.success("✅ Transaksi Berhasil Disimpan!")
                st.rerun()

    # ==========================================
    # HALAMAN 3: DATABASE
    # ==========================================
    elif menu_pilihan == "🗄️ Database & Manajemen":
        st.markdown("### 🗄️ Pusat Database")
        
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
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "status_stok": st.column_config.TextColumn("Status Stok"),
                "harga_beli": st.column_config.NumberColumn("Harga Beli", format="Rp %d"),
                "harga_jual": st.column_config.NumberColumn("Harga Jual", format="Rp %d"),
                "screenshot": st.column_config.LinkColumn("Screenshot", display_text="Lihat"),
                "keterangan": st.column_config.TextColumn("Keterangan", width="medium"),
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
                        f"Maturnuwun! Percayakan kebutuhan game Anda hanya di Copyright Fani. 🙏🌟"
                    )
                st.caption("Klik tombol copy di sudut kanan atas kotak ini untuk menyalin:")
                st.code(teks_laporan, language="text")

        st.markdown("---")
        
        st.markdown("### ⚙️ Kelola Data Spesifik (Edit / Hapus)")
        if not df.empty:
            tab_edit, tab_hapus = st.tabs(["📝 Edit Data", "🗑️ Hapus Data"])
            
            with tab_edit:
                eid = st.selectbox("Pilih ID Akun:", df['id'].tolist(), key="select_edit")
                row_edit = df[df['id'] == eid].iloc[0]
            
                with st.form(f"edit_form_{eid}"):
                    st.info(f"Silakan perbarui rincian data untuk ID: {eid}")
                    c1, c2 = st.columns(2)
                
                    with c1:
                        st.caption("🛍️ PEMBELIAN (MODAL)")
                        # Menambahkan Tanggal Beli
                        t_beli = st.date_input("Tanggal Beli", value=pd.to_datetime(row_edit['tanggal_beli']).date() if row_edit['tanggal_beli'] != "-" else datetime.today(), key=f"tb_{eid}")
                        eg = st.text_input("Game", value=row_edit['nama_game'], key=f"eg_{eid}")
                        ee = st.text_input("Email Akun", value=row_edit.get('email_akun', ''), key=f"ee_{eid}")
                        epa = st.text_input("Password Akun", value=row_edit.get('password_akun', ''), key=f"epa_{eid}")
                        es = st.text_input("Nama Penjual", value=row_edit.get('nama_penjual', ''), key=f"es_{eid}")
                        ews = st.text_input("WA Penjual", value=row_edit.get('wa_penjual', ''), key=f"ews_{eid}")
                        efs = st.text_input("FB Penjual", value=row_edit.get('fb_penjual', ''), key=f"efs_{eid}")
                        ehb = st.number_input("Harga Beli", value=float(row_edit.get('harga_beli', 0)), key=f"ehb_{eid}")
                
                    with c2:
                        st.caption("💰 PENJUALAN (PROFIT)")
                        # Menambahkan Tanggal Jual
                        t_jual = st.date_input("Tanggal Jual", value=pd.to_datetime(row_edit['tanggal_jual']).date() if row_edit['tanggal_jual'] != "-" else None, key=f"tj_{eid}")
                        eb = st.text_input("Nama Pembeli", value=row_edit.get('nama_pembeli', ''), key=f"eb_{eid}")
                        ewb = st.text_input("WA Pembeli", value=row_edit.get('no_wa', ''), key=f"ewb_{eid}")
                        efb = st.text_input("FB Pembeli", value=row_edit.get('akun_fb', ''), key=f"efb_{eid}")
                        ehj = st.number_input("Harga Jual", value=float(row_edit.get('harga_jual', 0)), key=f"ehj_{eid}")
                        eketerangan = st.text_area("Keterangan", value=row_edit.get('keterangan', ''), key=f"ket_{eid}")
                        ss_edit = st.file_uploader("🖼️ Update Screenshot Baru", type=['png', 'jpg', 'jpeg'], key=f"ss_{eid}")

                    if st.form_submit_button("💾 Update Seluruh Data", use_container_width=True, key=f"btn_{eid}"):
                        upd = {
                            "tanggal_beli": str(t_beli),
                            "tanggal_jual": str(t_jual) if t_jual else "-",
                            "nama_game": eg, "email_akun": ee, "password_akun": epa,
                            "nama_penjual": es, "wa_penjual": ews, "fb_penjual": efs,
                            "harga_beli": ehb, "nama_pembeli": eb, "no_wa": ewb, 
                            "akun_fb": efb, "harga_jual": ehj, "keterangan": eketerangan
                        }
                        if ss_edit:
                            fname = f"edit_{eid}_{ss_edit.name}".replace(" ","_")
                            supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                            upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                    
                        supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                        st.success("Data berhasil diupdate!")
                        st.rerun()	
            
            with tab_hapus:
                did = st.number_input("Masukkan ID yang akan dihapus:", min_value=0, step=1, value=int(df['id'].iloc[0]))
                if st.button("🚨 Hapus Permanen", type="primary"):
                    supabase.table("pendataan_akun").delete().eq("id", did).execute()
                    st.success(f"ID {did} Terhapus!")
                    st.rerun()