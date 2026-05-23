import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- 2. DESAIN UI KUSTOM ---
background_image_url = "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?q=80&w=2071&auto=format&fit=crop"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
    .stApp {{ background-image: url("{background_image_url}"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .stApp > header {{ background-color: transparent; }}
    .block-container {{ background-color: rgba(14, 17, 23, 0.85); padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px); margin-top: 2rem; border: 1px solid rgba(255, 255, 255, 0.05); }}
    [data-testid="stSidebar"] {{ background: linear-gradient(180deg, #0b0f19 0%, #161b22 100%) !important; border-right: 1px solid rgba(255, 255, 255, 0.05) !important; position: relative; overflow: hidden; }}
    .glowing-title {{ font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; text-shadow: 0px 0px 20px rgba(0, 201, 255, 0.3); }}
    [data-testid="stMetric"] {{ background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%); border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); transition: all 0.3s ease; }}
    [data-testid="stMetric"]:hover {{ transform: translateY(-7px); border-color: rgba(0, 201, 255, 0.5); }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI & AUTH ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_password():
    def password_entered():
        if st.session_state["password"] == "131313":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else: st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.markdown("<h1 class='glowing-title'>🔒 Copyright Fani</h1>", unsafe_allow_html=True)
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("⚠️ Password salah.")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        return False
    return True

if check_password():
    try:
        response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual")
            cols = ["id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"]
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=["id", "tanggal_beli", "tanggal_jual", "status_stok", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except: st.error("Gagal konek DB"); st.stop()

    st.sidebar.markdown("### ⚙️ Navigasi")
    menu = st.sidebar.radio("Menu:", ["📊 Dashboard", "📝 Input", "🗄️ Database"], label_visibility="collapsed")
    if st.sidebar.button("🚪 Logout", use_container_width=True): st.session_state.clear(); st.rerun()
    st.markdown("<h1 class='glowing-title'>☁️ MFF Database</h1>", unsafe_allow_html=True)
    if menu == "📊 Dashboard":
        st.markdown("### 📊 Ringkasan")
        if not df.empty:
            df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
            df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
            df['profit'] = df['harga_jual'] - df['harga_beli'] 
            c1, c2, c3 = st.columns(3)
            c1.metric("📦 Stok", f"{len(df[df['harga_jual']==0])}")
            c2.metric("✅ Terjual", f"{len(df[df['harga_jual']>0])}")
            c3.metric("💰 Profit", f"Rp {df[df['harga_jual']>0]['profit'].sum():,.0f}")
            st.area_chart(df[df['harga_jual']>0].groupby('tanggal_jual')['profit'].sum(), use_container_width=True)
    elif menu == "📝 Input":
        with st.form("in", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                t_beli = st.date_input("Tanggal Beli")
                game = st.text_input("Game")
                email = st.text_input("Email")
                pas = st.text_input("Password")
                h_beli = st.number_input("Harga Beli", 0)
            with col2:
                t_jual = st.date_input("Tanggal Jual", value=None)
                buyer = st.text_input("Nama Pembeli")
                h_jual = st.number_input("Harga Jual", 0)
            if st.form_submit_button("Simpan"):
                supabase.table("pendataan_akun").insert({"tanggal_beli": str(t_beli), "nama_game": game, "email_akun": email, "password_akun": pas, "harga_beli": float(h_beli), "tanggal_jual": str(t_jual) if t_jual else "-", "nama_pembeli": buyer, "harga_jual": float(h_jual)}).execute()
                st.success("Tersimpan!"); st.rerun()
    elif menu == "🗄️ Database":
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("### ⚙️ Edit/Hapus")
        eid = st.selectbox("Pilih ID:", df['id'].tolist())
        if st.button("Hapus"): supabase.table("pendataan_akun").delete().eq("id", eid).execute(); st.rerun()