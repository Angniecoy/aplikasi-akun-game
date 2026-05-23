import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MFF Database", layout="wide")
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.markdown("<style>.glowing-title{color:#00C9FF; font-size:38px; font-weight:800;}</style>", unsafe_allow_html=True)

def check_password():
    if "pw" not in st.session_state: st.session_state.pw = False
    if not st.session_state.pw:
        p = st.text_input("Password:", type="password")
        if p == "131313": st.session_state.pw = True; st.rerun()
        return False
    return True

if check_password():
    res = supabase.table("pendataan_akun").select("*").execute()
    df = pd.DataFrame(res.data)
    menu = st.sidebar.radio("Menu", ["📊 Dashboard", "📝 Input", "🗄️ Database"])
    st.markdown('<h1 class="glowing-title">🎮 MFF Database</h1>', unsafe_allow_html=True)

    if menu == "📊 Dashboard":
        df['hj'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        c1, c2 = st.columns(2)
        c1.metric("📦 Stok", len(df[df['hj']==0]))
        c2.metric("✅ Terjual", len(df[df['hj']>0]))
        st.bar_chart(df[df['hj']>0].groupby('nama_game')['hj'].sum())

    elif menu == "📝 Input":
        with st.form("in"):
            game = st.text_input("Nama Game")
            h_jual = st.number_input("Harga Jual", 0)
            if st.form_submit_button("Simpan"):
                supabase.table("pendataan_akun").insert({"nama_game": game, "harga_jual": h_jual}).execute()
                st.rerun()

    elif menu == "🗄️ Database":
        eid = st.selectbox("Pilih ID untuk Edit:", df['id'].tolist())
        row = df[df['id'] == eid].iloc[0]
        with st.form("edit"):
            eg = st.text_input("Game", row['nama_game'])
            ehj = st.number_input("Harga Jual", float(row['harga_jual']))
            ss_edit = st.file_uploader("Update Screenshot", type=['png','jpg'])
            if st.form_submit_button("Update"):
                upd = {"nama_game": eg, "harga_jual": ehj}
                if ss_edit:
                    fname = f"edit_{eid}_{ss_edit.name}"
                    supabase.storage.from_("screenshots").upload(fname, ss_edit.getvalue())
                    upd["screenshot"] = supabase.storage.from_("screenshots").get_public_url(fname)
                supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                st.success("Berhasil!"); st.rerun()