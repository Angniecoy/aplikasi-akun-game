import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

background_image_url = "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?q=80&w=2071&auto=format&fit=crop"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
    .stApp {{ background-image: url("{background_image_url}"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .glowing-title {{ font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
    if not st.session_state.password_correct:
        p = st.text_input("Password:", type="password")
        if p == "131313": st.session_state.password_correct = True; st.rerun()
        return False
    return True

if check_password():
    res = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(res.data)
    df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual")
    
    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu_pilihan = st.sidebar.radio("Menu Utama:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"], label_visibility="collapsed")
    
    if st.sidebar.button("🚪 Logout Sistem"): st.session_state.clear(); st.rerun()
    st.markdown("<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if menu_pilihan == "📊 Dashboard Analitik":
        st.markdown("### 📊 Ringkasan Eksekutif")
        st.metric("📦 In Stock", len(df[df['harga_jual'] == 0]))
        st.metric("💰 Total Profit", f"Rp {df[df['harga_jual'] > 0]['harga_jual'].sum():,.0f}")

    elif menu_pilihan == "📝 Input Transaksi":
        with st.form("main_form", clear_on_submit=True):
            game = st.text_input("Nama Game")
            h_jual = st.number_input("Harga Jual", min_value=0)
            ss = st.file_uploader("Upload Screenshot", type=['png', 'jpg'])
            if st.form_submit_button("Simpan"):
                url = "-"
                if ss:
                    fname = f"{game}_{ss.name}".replace(" ","_")
                    supabase.storage.from_("screenshots").upload(fname, ss.getvalue())
                    url = supabase.storage.from_("screenshots").get_public_url(fname)
                supabase.table("pendataan_akun").insert({"nama_game": game, "harga_jual": h_jual, "screenshot": url}).execute()
                st.rerun()

    elif menu_pilihan == "🗄️ Database & Manajemen":
        eid = st.selectbox("Pilih ID Akun:", df['id'].tolist())
        row_edit = df[df['id'] == eid].iloc[0]
        with st.form(f"edit_{eid}"):
            eg = st.text_input("Game", row_edit['nama_game'])
            ehj = st.number_input("Harga Jual", float(row_edit['harga_jual']))
            # --- FITUR EDIT SCREENSHOT ---
            ss_edit = st.file_uploader("🖼️ Update Screenshot Baru", type=['png', 'jpg'])
            if st.form_submit_button("Update Data"):
                upd = {"nama_game": eg, "harga_jual": ehj}
                if ss_edit:
                    fname = f"edit_{eid}_{ss_edit.name}".replace(" ","_")
                    supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                    upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                st.success("Update Berhasil!"); st.rerun()