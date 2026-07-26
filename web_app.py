# ==========================================
    # HALAMAN 4: DETAIL ANTRIAN BUYER
    # ==========================================
    elif menu_pilihan == "👥 Detail Antrian Buyer":
        st.markdown("### 👥 Detail Antrian Buyer")
        st.info("Kelola, pantau, edit, dan hapus daftar antrian calon pembeli akun game di sini.")
        
        # 1. Form Input Antrian Baru
        with st.form("form_antrian_buyer", clear_on_submit=True):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                nama_calon_buyer = st.text_input("Nama Calon Buyer*")
                kontak_buyer = st.text_input("No WA / Kontak*")
            with col_b2:
                game_diincar = st.text_input("Game / Akun yang Diincar*")
                catatan_buyer = st.text_area("Catatan / Request Khusus")
            
            if st.form_submit_button("➕ Tambah ke Antrian", use_container_width=True):
                if nama_calon_buyer and game_diincar:
                    try:
                        payload_buyer = {
                            "tanggal_input": datetime.today().strftime('%Y-%m-%d'),
                            "nama_buyer": nama_calon_buyer,
                            "kontak": kontak_buyer,
                            "game_diincar": game_diincar,
                            "catatan": catatan_buyer if catatan_buyer else "-"
                        }
                        supabase.table("antrian_buyer").insert(payload_buyer).execute()
                        st.success(f"Berhasil menambahkan {nama_calon_buyer} ke dalam antrian buyer!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menyimpan antrian: {e}")
                else:
                    st.warning("Mohon lengkapi Nama Calon Buyer dan Game yang diincar.")

        st.markdown("---")
        st.markdown("### 📋 Daftar Tabel Antrian Buyer Aktif")
        
        # Ambil dan Tampilkan Data Antrian dari Supabase
        try:
            res_buyer = supabase.table("antrian_buyer").select("*").order('id', desc=True).execute()
            if res_buyer.data:
                df_buyer = pd.DataFrame(res_buyer.data)
                
                # Urutan kolom yang rapi jika tersedia
                kolom_buyer_order = ["id", "tanggal_input", "nama_buyer", "kontak", "game_diincar", "catatan", "akun_fb"]
                kolom_b_tersedia = [col for col in kolom_buyer_order if col in df_buyer.columns]
                df_buyer = df_buyer[kolom_b_tersedia]
                
                st.dataframe(df_buyer, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("### ⚙️ Kelola Antrian (Edit / Hapus)")
                tab_edit_b, tab_hapus_b = st.tabs(["📝 Edit Antrian", "🗑️ Hapus Antrian"])
                
                # --- TAB EDIT ANTRIAN ---
                with tab_edit_b:
                    eid_b = st.selectbox("Pilih ID Antrian yang ingin diedit:", df_buyer['id'].tolist(), key="select_edit_buyer")
                    row_edit_b = df_buyer[df_buyer['id'] == eid_b].iloc[0]
                    
                    with st.form(f"edit_form_buyer_{eid_b}"):
                        st.info(f"Perbarui data antrian untuk ID: {eid_b}")
                        eb_col1, eb_col2 = st.columns(2)
                        
                        with eb_col1:
                            try: val_t_input = datetime.strptime(str(row_edit_b['tanggal_input']), "%Y-%m-%d").date()
                            except: val_t_input = datetime.today().date()
                            e_tgl = st.date_input("Tanggal Input", value=val_t_input)
                            e_nama = st.text_input("Nama Calon Buyer", value=row_edit_b.get('nama_buyer', ''))
                            e_kontak = st.text_input("No WA / Kontak", value=row_edit_b.get('kontak', ''))
                        
                        with eb_col2:
                            e_game = st.text_input("Game yang Diincar", value=row_edit_b.get('game_diincar', ''))
                            e_catatan = st.text_area("Catatan", value=row_edit_b.get('catatan', ''))
                            e_akunfb = st.text_input("Akun FB", value=row_edit_b.get('akun_fb', '') if pd.notna(row_edit_b.get('akun_fb')) else '')
                        
                        if st.form_submit_button("💾 Update Data Antrian", use_container_width=True):
                            upd_buyer = {
                                "tanggal_input": str(e_tgl),
                                "nama_buyer": e_nama,
                                "kontak": e_kontak,
                                "game_diincar": e_game,
                                "catatan": e_catatan,
                                "akun_fb": e_akunfb
                            }
                            supabase.table("antrian_buyer").update(upd_buyer).eq("id", eid_b).execute()
                            st.success("Data antrian berhasil diperbarui!")
                            st.rerun()

                # --- TAB HAPUS ANTRIAN ---
                with tab_hapus_b:
                    did_b = st.number_input("Masukkan ID Antrian yang akan dihapus:", min_value=0, step=1, value=int(df_buyer['id'].iloc[0]))
                    if st.button("🚨 Hapus Permanen Antrian", type="primary", key="btn_hapus_buyer"):
                        supabase.table("antrian_buyer").delete().eq("id", did_b).execute()
                        st.success(f"ID Antrian {did_b} berhasil dihapus!")
                        st.rerun()
                        
            else:
                st.info("Belum ada data antrian buyer saat ini.")
        except Exception as e:
            st.warning(f"Gagal memuat data antrian: {e}")