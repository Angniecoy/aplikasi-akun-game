import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- KONFIGURASI SUPABASE ---
# Gunakan data yang sudah Anda miliki sebelumnya
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Sistem Akun Game", page_icon="🎮", layout="wide")
st.title("☁️ Sistem Manajemen Bisnis Akun Game (Pro Cloud)")
st.markdown("---")

# 1. BACA DATABASE
try:
    response = supabase.table("pendataan_akun").select("*").order('id').execute()
    df = pd.DataFrame(response.data) if response.data else pd.DataFrame(columns=["id", "tanggal_beli", "nama_game", "email_akun", "nama_penjual", "harga_beli", "tanggal_jual", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
except Exception as e:
    st.error(f"Koneksi gagal: {e}")
    st.stop()

# 2. DASHBOARD KEUANGAN
df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)

stok = len(df[df['harga_jual'] == 0])
terjual = len(df[df['harga_jual'] > 0])
total_modal = df['harga_beli'].sum()
stok_rp = df[df['harga_jual'] == 0]['harga_beli'].sum()
profit = (df[df['harga_jual'] > 0]['harga_jual'] - df[df['harga_jual'] > 0]['harga_beli']).sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📦 In Stock", f"{stok} Akun")
col2.metric("✅ Terjual", f"{terjual} Akun")
col3.metric("💳 Total Modal", f"Rp {total_modal:,.0f}")
col4.metric("💎 Nilai Stok", f"Rp {stok_rp:,.0f}")
col5.metric("💰 Total Profit", f"Rp {profit:,.0f}")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Input Transaksi Baru", "📊 Database & Laporan"])

# --- TAB 1: FORM INPUT ---
with tab1:
    with st.form("form_tambah", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Data Pembelian")
            tgl_beli = st.date_input("Tanggal Beli")
            game = st.text_input("Nama Game*")
            email = st.text_input("Email Akun*")
            penjual = st.text_input("Password / Penjual")
            harga_beli = st.number_input("Harga Beli (Rp)*", min_value=0)
            ss_file = st.file_uploader("Upload Screenshot", type=['png', 'jpg', 'jpeg'])

        with c2:
            st.subheader("Data Penjualan")
            tgl_jual = st.date_input("Tanggal Jual", value=None)
            pembeli = st.text_input("Nama Pembeli")
            no_wa = st.text_input("No. WhatsApp")
            akun_fb = st.text_input("Akun FB")
            harga_jual = st.number_input("Harga Jual (Rp)", min_value=0)

        submitted = st.form_submit_button("💾 Simpan ke Cloud")

        if submitted:
            if not game or not email or harga_beli == 0:
                st.error("⚠️ Data wajib belum lengkap!")
            else:
                url_gambar = "-"
                # PROSES UPLOAD KE SUPABASE STORAGE
                if ss_file is not None:
                    try:
                        file_nama = f"{game}_{email}_{ss_file.name}".replace(" ", "_")
                        # Upload file mentah ke bucket 'screenshots'
                        supabase.storage.from_("screenshots").upload(file_nama, ss_file.getvalue())
                        # Ambil Public URL-nya
                        url_gambar = supabase.storage.from_("screenshots").get_public_url(file_nama)
                    except Exception as e:
                        st.warning(f"Gagal upload gambar, tapi data teks tetap disimpan. Error: {e}")

                data_baru = {
                    "tanggal_beli": str(tgl_beli), "nama_game": game, "email_akun": email,
                    "nama_penjual": penjual, "harga_beli": float(harga_beli),
                    "tanggal_jual": str(tgl_jual) if tgl_jual else "-",
                    "nama_pembeli": pembeli, "no_wa": no_wa, "akun_fb": akun_fb,
                    "harga_jual": float(harga_jual), "screenshot": url_gambar
                }
                
                supabase.table("pendataan_akun").insert(data_baru).execute()
                st.success("✅ Berhasil! Data & Gambar tersimpan di Cloud.")
                st.rerun()

# --- TAB 2: TABEL & VIEWER ---
with tab2:
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    c_view, c_del = st.columns(2)
    
    with c_view:
        st.subheader("🖼️ Lihat Screenshot")
        df_ss = df[df['screenshot'].str.contains("http", na=False)]
        if not df_ss.empty:
            pilih_id = st.selectbox("Pilih ID Akun:", df_ss['id'].tolist())
            link_ss = df_ss[df_ss['id'] == pilih_id]['screenshot'].values[0]
            st.image(link_ss, caption=f"Bukti ID {pilih_id}", use_container_width=True)
        else:
            st.caption("Belum ada gambar yang tersimpan di Cloud.")

    with c_del:
        st.subheader("🗑️ Hapus Data")
        del_id = st.number_input("ID yang ingin dihapus:", min_value=0, step=1)
        if st.button("Hapus Permanen", type="primary"):
            supabase.table("pendataan_akun").delete().eq("id", del_id).execute()
            st.success(f"ID {del_id} terhapus!")
            st.rerun()