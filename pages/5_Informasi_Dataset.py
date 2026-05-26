import streamlit as st
from utils.helper import load_data
from utils.style import load_css

# Load styling halaman
load_css()

st.title("Informasi Dataset")

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp{
        background-color:#f5efe6;
    }
    .info-box{
        background-color:#fffaf3;
        padding:24px;
        border-radius:16px;
        border:1px solid #dbc4aa;
        margin-bottom:25px;
        color:#4b3a2f;
        line-height:1.6;
    }
    .metric-container {
        display: flex;
        gap: 15px;
        margin-top: 15px;
    }
    .metric-card {
        background-color: #f5ebe0;
        padding: 12px 20px;
        border-radius: 10px;
        border: 1px solid #dbc4aa;
        flex: 1;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #6b4226;
        margin-top: 4px;
    }
    .column-badge {
        display: inline-block;
        background-color: #fffaf3;
        color: #6b4226;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #dbc4aa;
        margin-right: 8px;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# RINGKASAN DATASET
# =========================
st.markdown(
    f"""
    <div class="info-box">
        <h3 style="color:#6b4226; margin-top:0; margin-bottom:10px; font-size:22px;">Ringkasan Dataset</h3>
        <p style="margin-bottom:0; font-size:15px;">
            Dataset ini berisi kumpulan resep kuliner khas berbagai daerah di Nusantara. 
            Data di bawah diolah secara berkala untuk mendukung akurasi perhitungan penalaran pada sistem rekomendasi berbasis 
            <b>Certainty Factor (CF)</b>.
        </p>
        <div class="metric-container">
            <div class="metric-card">
                <div style="font-size:13px; color:#7c6a5e; font-weight:bold;">TOTAL BARIS DATA</div>
                <div class="metric-value">{len(df)}</div>
            </div>
            <div class="metric-card">
                <div style="font-size:13px; color:#7c6a5e; font-weight:bold;">TOTAL FITUR KOLOM</div>
                <div class="metric-value">{len(df.columns)}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# STRUKTUR KOLOM DATASET
# =========================
st.markdown("<h3 style='color:#6b4226; margin-bottom:12px; font-size:18px;'>Atribut/Kolom Tersedia</h3>", unsafe_allow_html=True)

# Membuat visualisasi badge horizontal untuk daftar kolom
badge_html = "".join([f'<span class="column-badge">📑 {col}</span>' for col in df.columns])
st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# PREVIEW DATASET
# =========================
st.markdown("<h3 style='color:#6b4226; margin-bottom:12px; font-size:18px;'>Preview 20 Data Pertama</h3>", unsafe_allow_html=True)

st.dataframe(
    df.head(20),
    use_container_width=True
)