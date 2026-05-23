import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- SETTING ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide")
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNGSI DATA ---
def load_data():
    response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(response.data)
    df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual")
    return df

df = load_data()

# --- SIDEBAR ---
menu = st.sidebar.radio("Menu:", ["📊 Dashboard", "📝 Input", "🗄️ Database"])
if st.sidebar.button("Logout"): st.session_state.clear(); st.rerun()

# --- HALAMAN DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("### 📊 Ringkasan Eksekutif")
    if not df.empty:
        df['hb'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
        df['hj'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        df['profit'] = df['hj'] - df['hb']
        
        # Pengingat Stok Mengendap
        st.markdown("#### 🚨 Notifikasi")
        df['tgl_b'] = pd.to_datetime(df['tanggal_beli'], errors='coerce')
        lama = df[(df['hj'] == 0) & ((datetime.now() - df['tgl_b']).dt.days > 7)]
        if not lama.empty: st.warning(f"⚠️ {len(lama)} akun sudah mengendap > 7 hari!")
        else: st.success("✅ Semua stok aman.")

        # Metrik
        c1, c2, c3 = st.columns(3)
        c1.metric("📦 Stok", f"{len(df[df['hj']==0])}")
        c2.metric("✅ Terjual", f"{len(df[df['hj']>0])}")
        c3.metric("💰 Total Profit", f"Rp {df[df['hj']>0]['profit'].sum():,.0f}")
        
        # Grafik Profit Harian
        st.markdown("### 📈 Profit Harian")
        st.area_chart(df[df['hj']>0].groupby('tanggal_jual')['profit'].sum())

# --- HALAMAN INPUT ---
elif menu == "📝 Input":
    with st.form("in", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            t_beli = st.date_input("Tanggal Beli")
            game = st.text_input("Nama Game")
            email = st.text_input("Email")
            pas = st.text_input("Password")
            h_beli = st.number_input("Harga Beli", 0)
        with col2:
            t_jual = st.date_input("Tanggal Jual", value=None)
            buyer = st.text_input("Nama Pembeli")
            h_jual = st.number_input("Harga Jual", 0)
        if st.form_submit_button("Simpan Data"):
            supabase.table("pendataan_akun").insert({
                "tanggal_beli": str(t_beli), "nama_game": game, "email_akun": email, 
                "password_akun": pas, "harga_beli": float(h_beli), 
                "tanggal_jual": str(t_jual) if t_jual else "-", 
                "nama_pembeli": buyer, "harga_jual": float(h_jual)
            }).execute()
            st.success("Tersimpan!"); st.rerun()

# --- HALAMAN DATABASE ---
elif menu == "🗄️ Database":
    st.dataframe(df, use_container_width=True)
    st.markdown("### ⚙️ Edit / Hapus Data")
    eid = st.selectbox("Pilih ID:", df['id'].tolist())
    row = df[df['id'] == eid].iloc[0]
    with st.form("edit"):
        col1, col2 = st.columns(2)
        eg = col1.text_input("Game", row['nama_game'])
        ehb = col1.number_input("Harga Beli", float(row['harga_beli']))
        ehj = col2.number_input("💵 Harga Jual", float(row['harga_jual']))
        eb = col2.text_input("Pembeli", row['nama_pembeli'])
        if st.form_submit_button("Update Data"):
            supabase.table("pendataan_akun").update({"nama_game": eg, "harga_beli": ehb, "nama_pembeli": eb, "harga_jual": ehj}).eq("id", eid).execute()
            st.rerun()
    if st.button("Hapus Data"): supabase.table("pendataan_akun").delete().eq("id", eid).execute(); st.rerun()