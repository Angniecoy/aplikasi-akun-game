import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="Sistem Akun Game Pro", page_icon="🎮", layout="wide")

# --- 2. DESAIN UI KUSTOM ---
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
    .stApp > header {{ background-color: transparent; }}
    .block-container {{
        background-color: rgba(14, 17, 23, 0.85); 
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
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

# --- 4. SISTEM KEAMANAN ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "131313":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Copyright Fani")
        st.info("Silakan masukkan password untuk mengakses sistem manajemen.")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Copyright Fani")
        st.text_input("Password:", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Password salah. Silakan coba lagi.")
        return False
    return True

# --- 5. APLIKASI UTAMA ---
if check_password():
    st.title("☁️ Sistem Manajemen Bisnis Akun Game (Pro Cloud)")
    st.caption("Akses Aman • Data Pembelian & Penjualan Lengkap")

    try:
        response = supabase.table("pendataan_akun").select("*").order('id', desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            
            # --- URUTAN KOLOM TABEL SESUAI PERMINTAAN BARU ---
            urutan_kolom = [
                "id", 
                "tanggal_beli", 
                "tanggal_jual", 
                "nama_game", 
                "nama_penjual", 
                "email_akun", 
                "password_akun", 
                "wa_penjual", 
                "fb_penjual", 
                "harga_beli", 
                "nama_pembeli", 
                "no_wa", 
                "akun_fb", 
                "harga_jual", 
                "screenshot"
            ]
            kolom_tersedia = [kol for kol in urutan_kolom if kol in df.columns]
            df = df[kolom_tersedia]
            
        else:
            df = pd.DataFrame(columns=["id", "tanggal_beli", "tanggal_jual", "nama_game", "nama_penjual", "email_akun", "password_akun", "wa_penjual", "fb_penjual", "harga_beli", "nama_pembeli", "no_wa", "akun_fb", "harga_jual", "screenshot"])
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    if not df.empty:
        df['harga_beli'] = pd.to_numeric(df['harga_beli'], errors='coerce').fillna(0)
        df['harga_jual'] = pd.to_numeric(df['harga_jual'], errors='coerce').fillna(0)
        stok = len(df[df['harga_jual'] == 0])
        terjual = len(df[df['harga_jual'] > 0])
        modal = df['harga_beli'].sum()
        nilai_stok = df[df['harga_jual'] == 0]['harga_beli'].sum()
        profit = (df[df['harga_jual'] > 0]['harga_jual'] - df[df['harga_jual'] > 0]['harga_beli']).sum()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("📦 In Stock", f"{stok} Akun")
        c2.metric("✅ Terjual", f"{terjual} Akun")
        c3.metric("💳 Total Modal", f"Rp {modal:,.0f}")
        c4.metric("💎 Nilai Stok", f"Rp {nilai_stok:,.0f}")
        c5.metric("💰 Total Profit", f"Rp {profit:,.0f}")

    st.markdown("---")
    t1, t2 = st.tabs(["📝 Input Transaksi", "📊 Database & Media"])

    with t1:
        with st.form("main_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("🛒 Data Pembelian (Dari Seller)")
                t_beli = st.date_input("Tanggal Beli")
                game = st.text_input("Nama Game*")
                
                col_em, col_pw = st.columns(2)
                with col_em:
                    email = st.text_input("Email Akun*")
                with col_pw:
                    pass_akun = st.text_input("Password Akun*")
                    
                seller = st.text_input("Nama Penjual")
                wa_seller = st.text_input("WhatsApp Penjual")
                fb_seller = st.text_input("FB Penjual")
                h_beli = st.number_input("Harga Beli (Rp)*", min_value=0)
                ss = st.file_uploader("Upload Bukti Screenshot", type=['png', 'jpg', 'jpeg'])
                
            with col_b:
                st.subheader("💰 Data Penjualan (Ke Customer)")
                t_jual = st.date_input("Tanggal Jual", value=None)
                buyer = st.text_input("Nama Pembeli")
                wa_buyer = st.text_input("WhatsApp Pembeli")
                fb_buyer = st.text_input("FB Pembeli")
                h_jual = st.number_input("Harga Jual (Rp)", min_value=0)

            if st.form_submit_button("💾 Simpan Data ke Cloud"):
                url = "-"
                if ss:
                    try:
                        fname = f"{game}_{ss.name}".replace(" ","_")
                        supabase.storage.from_("screenshots").upload(fname, ss.getvalue())
                        url = supabase.storage.from_("screenshots").get_public_url(fname)
                    except: pass
                
                payload = {
                    "tanggal_beli": str(t_beli), "nama_game": game, "email_akun": email,
                    "password_akun": pass_akun, 
                    "nama_penjual": seller, "wa_penjual": wa_seller, "fb_penjual": fb_seller,
                    "harga_beli": float(h_beli), "tanggal_jual": str(t_jual) if t_jual else "-",
                    "nama_pembeli": buyer, "no_wa": wa_buyer, "akun_fb": fb_buyer,
                    "harga_jual": float(h_jual), "screenshot": url
                }
                supabase.table("pendataan_akun").insert(payload).execute()
                st.success("Berhasil Disimpan!")
                st.rerun()

    with t2:
        st.subheader("📊 Tabel Seluruh Transaksi")
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        
        col_view, col_manage = st.columns([1, 1])
        
        with col_view:
            st.subheader("🖼️ Viewer Screenshot")
            if not df.empty:
                df_with_ss = df[df['screenshot'].str.contains("http", na=False)]
                if not df_with_ss.empty:
                    pilih_id_ss = st.selectbox("Pilih ID Akun untuk lihat gambar:", df_with_ss['id'].tolist())
                    img_url = df_with_ss[df_with_ss['id'] == pilih_id_ss]['screenshot'].values[0]
                    st.image(img_url, caption=f"Bukti Transaksi ID: {pilih_id_ss}", use_container_width=True)
                else:
                    st.info("Belum ada bukti screenshot yang diupload.")
        
        with col_manage:
            st.subheader("⚙️ Kelola Data")
            if not df.empty:
                tab_edit, tab_hapus = st.tabs(["📝 Edit Data Lanjutan", "🗑️ Hapus"])
                
                with tab_edit:
                    eid = st.selectbox("Pilih ID untuk diedit:", df['id'].tolist())
                    row = df[df['id'] == eid].iloc[0]
                    
                    with st.form(f"edit_form_{eid}"):
                        st.info("Silakan perbarui rincian data di bawah ini:")
                        e_col1, e_col2 = st.columns(2)
                        
                        with e_col1:
                            st.caption("🛍️ PEMBELIAN (MODAL)")
                            try:
                                val_tb = datetime.strptime(str(row['tanggal_beli']), "%Y-%m-%d").date()
                            except:
                                val_tb = datetime.today().date()
                            etb = st.date_input("Tanggal Beli", value=val_tb)
                            
                            eg = st.text_input("Game", value=row['nama_game'])
                            
                            e_col_em, e_col_pw = st.columns(2)
                            with e_col_em:
                                ee = st.text_input("Email", value=row['email_akun'])
                            with e_col_pw:
                                epa = st.text_input("Password Akun", value=row.get('password_akun','-')) 
                            
                            es = st.text_input("Seller", value=row.get('nama_penjual',''))
                            ews = st.text_input("WA Seller", value=row.get('wa_penjual',''))
                            efs = st.text_input("FB Seller", value=row.get('fb_penjual',''))
                            ehb = st.number_input("Harga Beli", value=float(row['harga_beli']))
                            
                        with e_col2:
                            st.caption("💰 PENJUALAN (PROFIT)")
                            try:
                                val_tj = datetime.strptime(str(row['tanggal_jual']), "%Y-%m-%d").date()
                            except:
                                val_tj = None
                            etj = st.date_input("Tanggal Jual", value=val_tj)
                            
                            eb = st.text_input("Buyer", value=row['nama_pembeli'])
                            ewb = st.text_input("WA Buyer", value=row['no_wa'])
                            efb = st.text_input("FB Buyer", value=row.get('akun_fb',''))
                            ehj = st.number_input("Harga Jual", value=float(row['harga_jual']))
                            
                        if st.form_submit_button("💾 Update Seluruh Data"):
                            upd = {
                                "tanggal_beli": str(etb) if etb else "-", 
                                "nama_game": eg, "email_akun": ee, 
                                "password_akun": epa,
                                "nama_penjual": es, "wa_penjual": ews, "fb_penjual": efs, "harga_beli": ehb,
                                "tanggal_jual": str(etj) if etj else "-", 
                                "nama_pembeli": eb, "no_wa": ewb, "akun_fb": efb, "harga_jual": ehj
                            }
                            supabase.table("pendataan_akun").update(upd).eq("id", eid).execute()
                            st.success("Rincian data berhasil diupdate!")
                            st.rerun()
                
                with tab_hapus:
                    did = st.number_input("Masukkan ID yang akan dihapus:", min_value=0, step=1)
                    if st.button("Hapus Permanen", type="primary"):
                        supabase.table("pendataan_akun").delete().eq("id", did).execute()
                        st.success(f"ID {did} Terhapus!")
                        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()