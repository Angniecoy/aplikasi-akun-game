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
    # Tambahkan Status Stok otomatis
    df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(
        lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual"
    )
    return df

# --- UI UTAMA ---
st.title("🎮 MFF Database Manajemen Buy & Sell")
df = load_data()

# --- SIDEBAR ---
menu = st.sidebar.radio("Menu:", ["📊 Dashboard", "📝 Input", "🗄️ Database"])
if st.sidebar.button("Logout"): st.session_state.clear(); st.rerun()

# --- HALAMAN ---
if menu == "📊 Dashboard":
    st.markdown("### 📊 Ringkasan Eksekutif")
    if not df.empty:
        df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
        df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        df['profit'] = df['harga_jual'] - df['harga_beli'] 
        c1, c2, c3 = st.columns(3)
        c1.metric("📦 Stok Tersedia", f"{len(df[df['harga_jual']==0])}")
        c2.metric("✅ Akun Terjual", f"{len(df[df['harga_jual']>0])}")
        c3.metric("💰 Total Profit", f"Rp {df[df['harga_jual']>0]['profit'].sum():,.0f}")
        st.bar_chart(df[df['harga_jual']>0].groupby('tanggal_jual')['profit'].sum())

elif menu == "📝 Input":
    with st.form("in", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            t_beli = st.date_input("Tanggal Beli")
            game = st.text_input("Nama Game")
            email = st.text_input("Email Akun")
            pas = st.text_input("Password Akun")
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

elif menu == "🗄️ Database":
    st.dataframe(df, use_container_width=True)
    st.markdown("### ⚙️ Edit / Hapus Data")
    eid = st.selectbox("Pilih ID untuk Edit:", df['id'].tolist())
    
    with st.form("edit_form"):
        row = df[df['id'] == eid].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            eg = st.text_input("Game", value=row['nama_game'])
            ee = st.text_input("Email", value=row['email_akun'])
            ehb = st.number_input("Harga Beli", value=float(row['harga_beli']))
        with col2:
            eb = st.text_input("Buyer", value=row['nama_pembeli'])
            ehj = st.number_input("💵 Harga Jual", value=float(row['harga_jual']))
        
        if st.form_submit_button("Update Data"):
            supabase.table("pendataan_akun").update({
                "nama_game": eg, "email_akun": ee, "harga_beli": ehb, 
                "nama_pembeli": eb, "harga_jual": ehj
            }).eq("id", eid).execute()
            st.success("Data diupdate!"); st.rerun()
            
    if st.button("Hapus Data Ini"):
        supabase.table("pendataan_akun").delete().eq("id", eid).execute(); st.rerun()