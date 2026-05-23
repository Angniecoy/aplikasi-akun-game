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

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > header {{ background-color: transparent; }}
    
    .block-container {{
        background-color: rgba(14, 17, 23, 0.85); 
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0b0f19 0%, #161b22 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        position: relative;
        overflow: hidden;
    }}
    
    [data-testid="stSidebar"]::before {{
        content: ""; position: absolute; top: -100px; left: -100px; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0, 201, 255, 0.15) 0%, transparent 70%); border-radius: 50%; z-index: 0; pointer-events: none;
    }}

    [data-testid="stSidebar"]::after {{
        content: ""; position: absolute; bottom: -100px; right: -100px; width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(146, 254, 157, 0.1) 0%, transparent 70%); border-radius: 50%; z-index: 0; pointer-events: none;
    }}

    .stRadio > div {{ gap: 12px; position: relative; z-index: 1; }}
    .stRadio > div > label {{
        background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important; padding: 12px 15px !important; transition: all 0.3s ease !important; cursor: pointer;
    }}
    .stRadio > div > label:hover {{
        background: linear-gradient(90deg, rgba(0, 201, 255, 0.1) 0%, transparent 100%) !important;
        border-color: rgba(0, 201, 255, 0.4) !important; transform: translateX(8px);
    }}

    .glowing-title {{
        font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; text-shadow: 0px 0px 20px rgba(0, 201, 255, 0.3);
    }}

    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 16px;
        box-shadow: 0 4px