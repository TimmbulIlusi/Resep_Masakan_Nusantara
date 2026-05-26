import streamlit as st
from utils.style import load_css

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Resep Nusantara",
    page_icon="🍲",
    layout="wide"
)

load_css()

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5efe6;
    }
    section[data-testid="stSidebar"] {
        background-color: #dbc1ac;
    }
    .hero-text {
        font-size: 16px;
        color: #4b3a2f;
        line-height: 1.6;
    }
    /* Styling baru untuk menyeimbangkan kotak Fitur Utama */
    .feature-card {
        background-color: #fffaf3;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #dbc4aa;
        min-height: 180px; /* Memaksa semua kotak memiliki tinggi minimal yang sama */
        height: 100%;
        color: #4b3a2f;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .feature-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .feature-desc {
        font-size: 14px;
        line-height: 1.5;
        color: #6b5b4f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.title("🍲 Sistem Rekomendasi Resep Masakan Nusantara")

st.markdown(
    """
    <div class="hero-text">
    Aplikasi ini membantu pengguna menemukan berbagai resep khas Indonesia berdasarkan bahan yang tersedia.<br>
    Sistem rekomendasi menggunakan metode <b>Certainty Factor (CF)</b> untuk menghitung tingkat kecocokan 
    dan kepastian resep yang paling relevan dengan bahan dapur Anda.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================
# FITUR UTAMA (GRID SEIMBANG)
# =========================
st.subheader("Fitur Utama")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title" style="color: #2e6f40;">🔍 Rekomendasi Resep</div>
            <div class="feature-desc">
                Cari resep berdasarkan bahan yang dimiliki pengguna menggunakan perhitungan Certainty Factor secara presisi.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title" style="color: #b05a3e;">🥘 Detail Bahan</div>
            <div class="feature-desc">
                Menampilkan analisis bahan yang cocok, bahan yang kurang, serta panduan langkah memasak secara lengkap.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title" style="color: #a47148;">📚 Kategori Masakan</div>
            <div class="feature-desc">
                Eksplorasi ribuan arsip kuliner tradisional yang dikelompokkan berdasarkan jenis hidangan masakan Nusantara.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =========================
# TENTANG APLIKASI
# =========================
st.subheader("Tentang Aplikasi")

st.write(
    """
    Dataset yang digunakan berisi ribuan resep makanan Indonesia. 
    Aplikasi ini dirancang sebagai sistem cerdas untuk membantu pengguna menemukan ide masakan 
    dengan tampilan yang sederhana, nyaman dibaca, dan mudah digunakan.
    """
)

st.divider()

# =========================
# FOOTER
# =========================
st.caption("Sistem Cerdas • Sistem Rekomendasi Resep Nusantara")