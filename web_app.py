import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- SETTING ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- UI KUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #0e1117; }
    .glowing-title { font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# --- KONEKSI ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNGSI ---
def check_password():
    if "pw" not in st.session_state: st.session_state.pw = False
    if not st.session_state.pw:
        p = st.text_input("Password:", type="password")
        if p == "131313": st.session_state.pw = True; st.rerun()
        return False
    return True

if check_password():
    res = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(res.data)
    
    # --- SIDEBAR ---
    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu = st.sidebar.radio("Menu:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"])
    if st.sidebar.button("🚪 Logout"): st.session_state.pw = False; st.rerun()

    # --- HALAMAN ---
    if menu == "📊 Dashboard Analitik":
        st.markdown('<h1 class="glowing-title">📊 Ringkasan Eksekutif</h1>', unsafe_allow_html=True)
        st.metric("📦 Stok Tersedia", len(df[pd.to_numeric(df['harga_jual']) == 0]))
        st.metric("💰 Total Profit", f"Rp {df[pd.to_numeric(df['harga_jual']) > 0]['harga_jual'].sum():,.0f}")

    elif menu == "📝 Input Transaksi":
        st.markdown('<h1 class="glowing-title">📝 Input Transaksi</h1>', unsafe_allow_html=True)
        with st.form("input_form", clear_on_submit=True):
            game = st.text_input("Nama Game")
            hj = st.number_input("Harga Jual", 0)
            if st.form_submit_button("Simpan"):
                supabase.table("pendataan_akun").insert({"nama_game": game, "harga_jual": hj}).execute()
                st.rerun()

    elif menu == "🗄️ Database & Manajemen":
        st.markdown('<h1 class="glowing-title">🗄️ Database</h1>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        
        # EDIT FORM
        eid = st.selectbox("Pilih ID untuk Edit:", df['id'].tolist(), key="select_id")
        row = df[df['id'] == eid].iloc[0]
        
        with st.form(f"edit_{eid}"):
            eg = st.text_input("Game", row['nama_game'])
            ehj = st.number_input("Harga Jual", float(row['harga_jual']))
            ss_edit = st.file_uploader("🖼️ Update Screenshot", type=['png', 'jpg'])
            
            if st.form_submit_button("Update Data"):
                upd = {"nama_game": eg, "harga_jual": ehj}
                if ss_edit:
                    fname = f"edit_{eid}_{ss_edit.name}"
                    supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                    upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                st.success("Update Berhasil!"); st.rerun()