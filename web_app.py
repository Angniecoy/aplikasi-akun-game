import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PENGATURAN HALAMAN ---
st.set_page_config(page_title="MFF Database", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- 2. DESAIN UI ---
st.markdown("""
    <style>
    .glowing-title { font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# --- 3. KONEKSI ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 4. KEAMANAN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h1 class='glowing-title'>🔒 Copyright Fani</h1>", unsafe_allow_html=True)
        st.text_input("Password:", type="password", key="password")
        if st.button("Login"):
            if st.session_state["password"] == "131313":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("Password Salah")
        return False
    return st.session_state["password_correct"]

# --- 5. APLIKASI UTAMA ---
if check_password():
    # Ambil Data
    response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(response.data) if response.data else pd.DataFrame()
    
    if not df.empty:
        df['tgl_jual_dt'] = pd.to_datetime(df['tanggal_jual'], errors='coerce')
        df['bulan_tahun'] = df['tgl_jual_dt'].dt.to_period('M').astype(str)
        df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
        df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        df['profit_per_akun'] = df['harga_jual'] - df['harga_beli']

    # --- SIDEBAR ---
    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu_pilihan = st.sidebar.radio("Menu Utama:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Filter Waktu")
    daftar_bulan = sorted(df['bulan_tahun'].dropna().unique(), reverse=True) if not df.empty else []
    pilih_bulan = st.sidebar.selectbox("Pilih Bulan Transaksi:", ["Semua Bulan"] + daftar_bulan)
    
    # Filter Data (df_filter selalu mengikuti pilihan bulan)
    df_filter = df[df['bulan_tahun'] == pilih_bulan].copy() if pilih_bulan != "Semua Bulan" else df.copy()

    # --- KONTEN UTAMA ---
    st.markdown("<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>", unsafe_allow_html=True)
    st.caption("Akses Aman • Analitik Real-time • Data Sinkronisasi Cloud")

    if menu_pilihan == "📊 Dashboard Analitik":
        st.markdown("### 📊 Ringkasan Eksekutif")
        tab_bulan, tab_all = st.tabs(["📅 Fokus Bulan Ini", "🌐 Laporan Keseluruhan"])
        
        with tab_bulan:
            st.markdown(f"#### Data Khusus: **{pilih_bulan}**")
            if not df_filter.empty:
                stok = len(df_filter[df_filter['harga_jual'] == 0])
                terjual = len(df_filter[df_filter['harga_jual'] > 0])
                profit = df_filter[df_filter['harga_jual'] > 0]['profit_per_akun'].sum()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("📦 In Stock", f"{stok} Akun")
                c2.metric("✅ Terjual", f"{terjual} Akun")
                c3.metric("💰 Profit", f"Rp {profit:,.0f}")
                
                st.markdown("### 📈 Grafik Omzet Harian")
                st.area_chart(df_filter.groupby('tanggal_jual')['harga_jual'].sum())
            else:
                st.info("Belum ada data untuk bulan yang dipilih.")
        
        with tab_all:
            st.markdown("### 📊 Ringkasan Semua Data")
            st.metric("💳 Total Modal Muter (All-Time)", f"Rp {df['harga_beli'].sum():,.0f}")
            st.bar_chart(df.groupby('bulan_tahun')['harga_jual'].sum())

    elif menu_pilihan == "📝 Input Transaksi":
        # (Sisa kode Input Transaksi Anda tetap di sini)
        st.info("Form Input Transaksi...") 

    elif menu_pilihan == "🗄️ Database & Manajemen":
        # (Sisa kode Database Anda tetap di sini)
        st.info("Tabel Database...")