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
        box-shadow: 0 4px 20px rgba(0,0,0,0.15); transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s
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
                "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"
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
    st.sidebar.caption("Sistem MFF Pro v2.6")
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
                "screenshot": st.column_config