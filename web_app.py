import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- 1. PENGATURAN HALAMAN ---
st.set_page_config(page_title="Sistem Akun Game Pro", page_icon="🎮", layout="wide")

# --- 2. KONEKSI SUPABASE ---
SUPABASE_URL = "https://elnedvfsuxfdizrpciwb.supabase.co"
SUPABASE_KEY = "sb_publishable_Z3h1zSRnCH5N2LStz_i_aQ__FsnB0Rh"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 3. SISTEM KEAMANAN (LOGIN) ---
def check_password():
    """Mengembalikan True jika password benar."""
    def password_entered():
        # Ganti 'admin123' di bawah ini dengan password rahasia Anda
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Hapus dari memori demi keamanan
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

# --- 4. APLIKASI UTAMA (Berjalan jika Login Sukses) ---
if check_password():
    st.title("☁️ Sistem Manajemen Bisnis Akun Game (Pro Cloud)")
    st.caption("Akses Aman • Sinkronisasi Sydney Server • Cloud Storage Aktif")

    # Ambil Data dari Database
    try:
        response = supabase.table("pendataan_akun").select("*").order('id').execute()
        df = pd.DataFrame(response.data) if response.data else pd.DataFrame(columns=["id", "tanggal_beli", "nama_game", "email_akun", "nama_penjual", "harga_beli", "tanggal_jual", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    # --- Kalkulasi Dashboard Otomatis ---
    df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
    df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)

    stok = len(df[df['harga_jual'] == 0])
    terjual = len(df[df['harga_jual'] > 0])
    total_modal = df['harga_beli'].sum()
    stok_rp = df[df['harga_jual'] == 0]['harga_beli'].sum()
    profit = (df[df['harga_jual'] > 0]['harga_jual'] - df[df['harga_jual'] > 0]['harga_beli']).sum()

    # --- Tampilan Dashboard 5 Kolom ---
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📦 In Stock", f"{stok} Akun")
    col2.metric("✅ Terjual", f"{terjual} Akun")
    col3.metric("💳 Total Modal", f"Rp {total_modal:,.0f}")
    col4.metric("💎 Nilai Stok", f"Rp {stok_rp:,.0f}")
    col5.metric("💰 Total Profit", f"Rp {profit:,.0f}")
    st.markdown("---")

    # --- Pengaturan Tab Layar ---
    tab1, tab2 = st.tabs(["📝 Input Transaksi Baru", "📊 Database & Laporan"])

    # --- TAB 1: FORM INPUT DATA ---
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
                ss_file = st.file_uploader("Upload Bukti Pembelian", type=['png', 'jpg', 'jpeg'])
            with c2:
                st.subheader("Data Penjualan")
                tgl_jual = st.date_input("Tanggal Jual", value=None)
                pembeli = st.text_input("Nama Pembeli")
                no_wa = st.text_input("No. WhatsApp")
                akun_fb = st.text_input("Akun FB")
                harga_jual = st.number_input("Harga Jual (Rp)", min_value=0)
            
            if st.form_submit_button("💾 Simpan ke Cloud"):
                if not game or not email or harga_beli == 0:
                    st.error("⚠️ Nama Game, Email, dan Harga Beli wajib diisi!")
                else:
                    url_gambar = "-"
                    # Proses Upload Gambar ke Supabase Storage
                    if ss_file:
                        try:
                            file_nama = f"{game}_{email}_{ss_file.name}".replace(" ", "_")
                            supabase.storage.from_("screenshots").upload(file_nama, ss_file.getvalue())
                            url_gambar = supabase.storage.from_("screenshots").get_public_url(file_nama)
                        except: pass
                    
                    # Siapkan Data
                    data_baru = {
                        "tanggal_beli": str(tgl_beli), "nama_game": game, "email_akun": email,
                        "nama_penjual": penjual, "harga_beli": float(harga_beli),
                        "tanggal_jual": str(tgl_jual) if tgl_jual else "-",
                        "nama_pembeli": pembeli, "no_wa": no_wa, "akun_fb": akun_fb,
                        "harga_jual": float(harga_jual), "screenshot": url_gambar
                    }
                    # Kirim ke Database
                    supabase.table("pendataan_akun").insert(data_baru).execute()
                    st.success("✅ Data tersimpan aman!")
                    st.rerun()

    # --- TAB 2: MANAJEMEN DATABASE ---
    with tab2:
        # Tabel Utama
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        
        # --- FITUR EDIT DATA ---
        st.subheader("📝 Edit Data Transaksi")
        if not df.empty:
            edit_id = st.selectbox("Pilih ID yang ingin diubah:", df['id'].tolist(), key="edit_select")
            row_data = df[df['id'] == edit_id].iloc[0]
            
            with st.expander(f"Klik untuk Mengubah Data ID: {edit_id}"):
                with st.form(f"form_edit_{edit_id}"):
                    ce1, ce2 = st.columns(2)
                    with ce1:
                        new_game = st.text_input("Nama Game", value=row_data['nama_game'])
                        new_email = st.text_input("Email Akun", value=row_data['email_akun'])
                        new_harga_beli = st.number_input("Harga Beli (Rp)", value=float(row_data['harga_beli']))
                    with ce2:
                        new_pembeli = st.text_input("Nama Pembeli", value=row_data['nama_pembeli'])
                        new_tgl_jual = st.text_input("Tanggal Jual (YYYY-MM-DD)", value=row_data['tanggal_jual'])
                        new_harga_jual = st.number_input("Harga Jual (Rp)", value=float(row_data['harga_jual']))
                    
                    if st.form_submit_button("💾 Update Data"):
                        update_payload = {
                            "nama_game": new_game,
                            "email_akun": new_email,
                            "harga_beli": new_harga_beli,
                            "nama_pembeli": new_pembeli,
                            "tanggal_jual": new_tgl_jual,
                            "harga_jual": new_harga_jual
                        }
                        supabase.table("pendataan_akun").update(update_payload).eq("id", edit_id).execute()
                        st.success(f"✅ Data ID {edit_id} berhasil diperbarui!")
                        st.rerun()

        st.markdown("---")
        c_view, c_del = st.columns(2)
        
        # --- FITUR VIEWER GAMBAR ---
        with c_view:
            st.subheader("🖼️ Viewer Bukti Transaksi")
            df_ss = df[df['screenshot'].str.contains("http", na=False)]
            if not df_ss.empty:
                pilih_id = st.selectbox("Pilih ID Akun:", df_ss['id'].tolist(), key="view_select")
                link = df_ss[df_ss['id'] == pilih_id]['screenshot'].values[0]
                st.image(link, use_container_width=True)
            else:
                st.caption("Belum ada gambar yang tersimpan.")
                
        # --- FITUR HAPUS DATA ---
        with c_del:
            st.subheader("🗑️ Hapus Data")
            del_id = st.number_input("Masukkan ID Akun:", min_value=0, step=1)
            if st.button("Hapus Permanen", type="primary"):
                supabase.table("pendataan_akun").delete().eq("id", del_id).execute()
                st.success("Data Terhapus Secara Permanen!")
                st.rerun()

    # --- TOMBOL LOGOUT ---
    st.sidebar.markdown("---")
    st.sidebar.caption("Sistem Keamanan Aktif")
    if st.sidebar.button("🚪 Log Out dari Aplikasi"):
        del st.session_state["password_correct"]
        st.rerun()