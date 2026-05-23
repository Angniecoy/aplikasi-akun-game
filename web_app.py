import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- SETTING ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide")

# --- UI KUSTOM (Desain yang Anda sukai) ---
st.markdown("""
    <style>
    .glowing-title { font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNGSI DATA ---
def load_data():
    res = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(res.data)
    df['status_stok'] = df['harga_jual'].apply(lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual")
    return df

df = load_data()

# --- SIDEBAR & MENU ---
st.sidebar.markdown("### ⚙️ Sistem Navigasi")
menu = st.sidebar.radio("Menu Utama:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"])

st.markdown('<h1 class="glowing-title">☁️ MFF Database Manajemen Buy & Sell</h1>', unsafe_allow_html=True)

# --- HALAMAN DASHBOARD ---
if menu == "📊 Dashboard Analitik":
    st.markdown("### 📊 Ringkasan Eksekutif")
    if not df.empty:
        df['hj'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        c1, c2, c3 = st.columns(3)
        c1.metric("📦 Stok Tersedia", len(df[df['hj']==0]))
        c2.metric("✅ Total Terjual", len(df[df['hj']>0]))
        c3.metric("💰 Total Profit", f"Rp {df[df['hj']>0]['hj'].sum():,.0f}")
        st.area_chart(df[df['hj']>0].groupby('tanggal_jual')['hj'].sum())

# --- HALAMAN INPUT ---
elif menu == "📝 Input Transaksi":
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        game = col1.text_input("Nama Game")
        h_beli = col1.number_input("Harga Beli", 0)
        h_jual = col2.number_input("Harga Jual", 0)
        if st.form_submit_button("💾 Simpan Data"):
            supabase.table("pendataan_akun").insert({"nama_game": game, "harga_beli": h_beli, "harga_jual": h_jual}).execute()
            st.success("Tersimpan!"); st.rerun()

# --- HALAMAN DATABASE (Dengan Fitur Edit Screenshot) ---
elif menu == "🗄️ Database & Manajemen":
    st.dataframe(df, use_container_width=True)
    eid = st.selectbox("Pilih ID untuk Edit:", df['id'].tolist())
    row = df[df['id'] == eid].iloc[0]
    
    with st.form("edit_form"):
        eg = st.text_input("Game", row['nama_game'])
        ehj = st.number_input("Harga Jual", float(row['harga_jual']))
        ss_edit = st.file_uploader("🖼️ Update Screenshot Baru", type=['png', 'jpg', 'jpeg'])
        
        if st.form_submit_button("💾 Update Data"):
            upd = {"nama_game": eg, "harga_jual": ehj}
            if ss_edit:
                fname = f"edit_{eid}_{ss_edit.name}"
                supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
            supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
            st.success("Data diupdate!"); st.rerun()