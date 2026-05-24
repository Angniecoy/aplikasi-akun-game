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
                "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"
            ]
            kolom_tersedia = [kol for kol in urutan_kolom if kol in df.columns]
            df = df[kolom_tersedia]
        else:
            df = pd.DataFrame(columns=["id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu_pilihan = st.sidebar.radio("Menu Utama:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"], label_visibility="collapsed")
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Sistem MFF Pro v2.5")
    if st.sidebar.button("🚪 Logout Sistem", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>", unsafe_allow_html=True)
    st.caption("Akses Aman • Analitik Real-time • Data Sinkronisasi Cloud")
    st.markdown("<br>", unsafe_allow_html=True)

    if menu_pilihan == "📊 Dashboard Analitik":
        # ... (Dashboard asli Anda) ...
        st.info("Dashboard Analitik sedang dimuat.")

    elif menu_pilihan == "📝 Input Transaksi":
        # ... (Input asli Anda) ...
        st.info("Form Input Transaksi.")

    elif menu_pilihan == "🗄️ Database & Manajemen":
        # ... (Dataframe dan search asli Anda) ...
        st.dataframe(df, use_container_width=True)
        
        with st.expander("⚙️ Kelola Data Spesifik (Edit / Hapus)"):
            eid = st.selectbox("Pilih ID Akun:", df['id'].tolist(), key="select_edit")
            row_edit = df[df['id'] == eid].iloc[0]
            
            with st.form(f"edit_form_{eid}"):
                c1, c2 = st.columns(2)
                with c1:
                    eg = st.text_input("Game", value=row_edit['nama_game'], key=f"eg_{eid}")
                    ehb = st.number_input("Harga Beli", value=float(row_edit['harga_beli']), key=f"ehb_{eid}")
                with c2:
                    ehj = st.number_input("Harga Jual", value=float(row_edit['harga_jual']), key=f"ehj_{eid}")
                    # --- FITUR EDIT SCREENSHOT ---
                    ss_edit = st.file_uploader("🖼️ Update Screenshot Baru", type=['png', 'jpg', 'jpeg'], key=f"ss_{eid}")
                
                if st.form_submit_button("💾 Update Seluruh Data", use_container_width=True, key=f"btn_{eid}"):
                    upd = {"nama_game": eg, "harga_beli": ehb, "harga_jual": ehj}
                    if ss_edit:
                        fname = f"edit_{eid}_{ss_edit.name}".replace(" ","_")
                        supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                        upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                    supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                    st.success("Data berhasil diupdate!"); st.rerun()