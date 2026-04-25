import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- 1. PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="Sistem Akun Game Pro", page_icon="🎮", layout="wide")

# --- 2. DESAIN UI KUSTOM (BACKGROUND & GLASSMORPHISM) ---
background_image_url = "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?q=80&w=2071&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > header {{
        background-color: transparent;
    }}
    .block-container {{
        background-color: rgba(14, 17, 23, 0.85); 
        padding-top: 2rem;
        padding-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        margin-top: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. KONEKSI SUPABASE ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 4. SISTEM KEAMANAN (LOGIN) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Akses Terbatas")
        st.info("Silakan masukkan password untuk masuk ke dalam sistem.")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Akses Terbatas")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Password salah. Silakan coba lagi.")
        return False
    else:
        return True

# --- 5. APLIKASI UTAMA ---
if check_password():
    st.title("☁️ Sistem Manajemen Bisnis Akun Game (Pro Cloud)")
    st.caption("Akses Aman • Sinkronisasi Sydney Server • Cloud Storage Aktif")

    try:
        response = supabase.table("pendataan_akun").select("*").order('id').execute()
        df = pd.DataFrame(response.data) if response.data else pd.DataFrame(columns=["id", "tanggal_beli", "nama_game", "email_akun", "nama_penjual", "harga_beli", "tanggal_jual", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    # DASHBOARD
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

    # --- TAB 1: INPUT DATA ---
    with tab1:
        with st.form("form_tambah", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🛒 Data Pembelian (Modal)")
                tgl_beli = st.date_input("Tanggal Beli")
                game = st.text_input("Nama Game*")
                email = st.text_input("Email Akun*")
                penjual = st.text_input("Password / Nama Penjual")
                # Penambahan field di sini sesuai permintaan Anda:
                wa_penjual = st.text_input("No. WhatsApp Penjual")
                fb_penjual = st.text_input("Akun FB Penjual")
                harga_beli = st.number_input("Harga Beli (Rp)*", min_value=0)
                ss_file = st.file_uploader("Upload Bukti Pembelian", type=['png', 'jpg', 'jpeg'])
            with c2:
                st.subheader("💰 Data Penjualan (Customer)")
                tgl_jual = st.date_input("Tanggal Jual", value=None)
                pembeli = st.text_input("Nama Pembeli")
                harga_jual = st.number_input("Harga Jual (Rp)", min_value=0)

            if st.form_submit_button("💾 Simpan ke Cloud"):
                if not game or not email or harga_beli == 0:
                    st.error("⚠️ Nama Game, Email, dan Harga Beli wajib diisi!")
                else:
                    url_gambar = "-"
                    if ss_file:
                        try:
                            file_nama = f"{game}_{email}_{ss_file.name}".replace(" ", "_")
                            supabase.storage.from_("screenshots").upload(file_nama, ss_file.getvalue())
                            url_gambar = supabase.storage.from_("screenshots").get_public_url(file_nama)
                        except: pass
                    
                    data_baru = {
                        "tanggal_beli": str(tgl_beli), "nama_game": game, "email_akun": email,
                        "nama_penjual": penjual, "no_wa": wa_penjual, "akun_fb": fb_penjual,
                        "harga_beli": float(harga_beli),
                        "tanggal_jual": str(tgl_jual) if tgl_jual else "-",
                        "nama_pembeli": pembeli, "harga_jual": float(harga_jual), 
                        "screenshot": url_gambar
                    }
                    supabase.table("pendataan_akun").insert(data_baru).execute()
                    st.success("✅ Data tersimpan aman!")
                    st.rerun()

    # --- TAB 2: DATABASE ---
    with tab2:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        
        # FITUR EDIT
        st.subheader("📝 Edit Data Transaksi")
        if not df.empty:
            edit_id = st.selectbox("Pilih ID Akun:", df['id'].tolist(), key="edit_select")
            row = df[df['id'] == edit_id].iloc[0]
            
            with st.expander(f"Edit Rincian ID: {edit_id}"):
                with st.form(f"form_edit_{edit_id}"):
                    ce1, ce2 = st.columns(2)
                    with ce1:
                        e_game = st.text_input("Nama Game", value=row['nama_game'])
                        e_email = st.text_input("Email Akun", value=row['email_akun'])
                        e_penjual = st.text_input("Nama Penjual", value=row['nama_penjual'])
                        e_wa = st.text_input("No WA Penjual", value=row['no_wa'])
                        e_fb = st.text_input("FB Penjual", value=row['akun_fb'])
                        e_hbeli = st.number_input("Harga Beli", value=float(row['harga_beli']))
                    with ce2:
                        e_pembeli = st.text_input("Nama Pembeli", value=row['nama_pembeli'])
                        e_tjual = st.text_input("Tgl Jual (YYYY-MM-DD)", value=row['tanggal_jual'])
                        e_hjual = st.number_input("Harga Jual", value=float(row['harga_jual']))
                    
                    if st.form_submit_button("💾 Update"):
                        upd = {
                            "nama_game": e_game, "email_akun": e_email, "nama_penjual": e_penjual,
                            "no_wa": e_wa, "akun_fb": e_fb, "harga_beli": e_hbeli,
                            "nama_pembeli": e_pembeli, "tanggal_jual": e_tjual, "harga_jual": e_hjual
                        }
                        supabase.table("pendataan_akun").update(upd).eq("id", edit_id).execute()
                        st.success("Berhasil diperbarui!")
                        st.rerun()

        st.markdown("---")
        v1, v2 = st.columns(2)
        with v1:
            st.subheader("🖼️ Viewer Screenshot")
            df_ss = df[df['screenshot'].str.contains("http", na=False)]
            if not df_ss.empty:
                v_id = st.selectbox("Pilih ID:", df_ss['id'].tolist(), key="v_sel")
                st.image(df_ss[df_ss['id'] == v_id]['screenshot'].values[0], use_container_width=True)
        with v2:
            st.subheader("🗑️ Hapus Data")
            d_id = st.number_input("ID Hapus:", min_value=0, step=1)
            if st.button("Hapus Permanen", type="primary"):
                supabase.table("pendataan_akun").delete().eq("id", d_id).execute()
                st.success("Terhapus!")
                st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Log Out"):
        del st.session_state["password_correct"]
        st.rerun()