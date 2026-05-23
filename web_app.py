# --- TAMBAHKAN INI DI BAGIAN AWAL HALAMAN DASHBOARD ---
    if menu == "📊 Dashboard":
        st.markdown("### 📊 Analitik Penjualan")
        
        # 1. Komponen Filter (Sidebar atau Main)
        col_f1, col_f2 = st.columns(2)
        pilih_game = col_f1.multiselect("Filter Game:", options=df['nama_game'].unique())
        
        # Logika Filter
        df_filter = df.copy()
        if pilih_game:
            df_filter = df_filter[df_filter['nama_game'].isin(pilih_game)]
        
        # 2. Ringkasan setelah Filter
        st.markdown(f"**Menampilkan data untuk: {', '.join(pilih_game) if pilih_game else 'Semua Game'}**")
        
        if not df_filter.empty:
            df_filter['hb'] = pd.to_numeric(df_filter['harga_beli'], errors='coerce').fillna(0)
            df_filter['hj'] = pd.to_numeric(df_filter['harga_jual'], errors='coerce').fillna(0)
            df_filter['profit'] = df_filter['hj'] - df_filter['hb']
            
            c1, c2, c3 = st.columns(3)
            c1.metric("📦 Stok Tersedia", f"{len(df_filter[df_filter['hj']==0])}")
            c2.metric("✅ Akun Terjual", f"{len(df_filter[df_filter['hj']>0])}")
            c3.metric("💰 Total Profit", f"Rp {df_filter[df_filter['hj']>0]['profit'].sum():,.0f}")
            
            # 3. Grafik Profit per Game (jika memilih lebih dari 1 game)
            st.markdown("### 📈 Performa Profit per Game")
            profit_game = df_filter[df_filter['hj']>0].groupby('nama_game')['profit'].sum()
            st.bar_chart(profit_game)