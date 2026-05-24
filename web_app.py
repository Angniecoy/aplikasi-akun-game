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
    html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
    .stApp {{ background-image: url("{background_image_url}"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .stApp > header {{ background-color: transparent; }}
    .block-container {{ background-color: rgba(14, 17, 23, 0.85); padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px); margin-top: 2rem; border: 1px solid rgba(255, 255, 255, 0.05); }}
    [data-testid="stSidebar"] {{ background: linear-gradient(180deg, #0b0f19 0%, #161b22 100%) !important; border-right: 1px solid rgba(255, 255, 255, 0.05) !important; position: relative; overflow: hidden; }}
    .glowing-title {{ font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; text-shadow: 0px 0px 20px rgba(0, 201, 255, 0.3); }}
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

# --- 5. APLIKASI UTAMA ---
if check_password():
    response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
    df = pd.DataFrame(response.data)
    df['status_stok'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0).apply(lambda x: "🟢 Tersedia" if x == 0 else "🔴 Terjual")
    
    st.sidebar.markdown("### ⚙️ Sistem Navigasi")
    menu_pilihan = st.sidebar.radio("Menu Utama:", ["📊 Dashboard Analitik", "📝 Input Transaksi", "🗄️ Database & Manajemen"], label_visibility="collapsed")
    if st.sidebar.button("🚪 Logout Sistem", use_container_width=True): st.session_state.clear(); st.rerun()

    st.markdown("<h1 class='glowing-title'>☁️ MFF Database Manajemen Buy & Sell</h1>", unsafe_allow_html=True)
    
    if menu_pilihan == "🗄️ Database & Manajemen":
        st.markdown("### 🗄️ Pusat Database")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### ⚙️ Kelola Data Spesifik (Edit / Hapus)")
        tab_edit, tab_hapus = st.tabs(["📝 Edit Data", "🗑️ Hapus Data"])
        
        with tab_edit:
            eid = st.selectbox("Pilih ID Akun:", df['id'].tolist(), key="select_edit")
            row_edit = df[df['id'] == eid].iloc[0]
            
            with st.form(f"edit_form_{eid}"):
                c1, c2 = st.columns(2)
                with c1:
                    eg = st.text_input("Game", value=row_edit['nama_game'], key=f"eg_{eid}")
                    ehb = st.number_input("Harga Beli", value=float(row_edit['harga_beli']), key=f"ehb_{eid}")
                with c2:
                    ehj = st.number_input("Harga Jual", value=float(row_edit['harga_jual']), key=f"ehj_{eid}")
                    ss_edit = st.file_uploader("🖼️ Update Screenshot Baru", type=['png', 'jpg', 'jpeg'], key=f"ss_{eid}")
                
                if st.form_submit_button("💾 Update Seluruh Data", use_container_width=True, key=f"btn_{eid}"):
                    upd = {"nama_game": eg, "harga_beli": ehb, "harga_jual": ehj}
                    if ss_edit:
                        fname = f"edit_{eid}_{ss_edit.name}".replace(" ","_")
                        supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                        upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                    supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                    st.success("Data berhasil diupdate!"); st.rerun()

        with tab_hapus:
            did = st.number_input("ID yang dihapus:", min_value=0, step=1, key="del_id")
            if st.button("🚨 Hapus Permanen"):
                supabase.table("pendataan_akun").delete().eq("id", did).execute()
                st.rerun()