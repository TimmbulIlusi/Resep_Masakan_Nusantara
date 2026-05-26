import streamlit as st
from utils.style import load_css

# Load styling halaman
load_css()

st.title("Tentang Project")

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp{
        background-color:#f5efe6;
    }
    .about-box{
        background-color:#fffaf3;
        padding:26px;
        border-radius:18px;
        border:1px solid #dbc4aa;
        margin-bottom:25px;
        line-height:1.6;
        color:#4b3a2f;
    }
    .member-card {
        background-color:#fffaf3;
        padding:16px;
        border-radius:12px;
        border:1px solid #dbc4aa;
        text-align:center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DESKRIPSI PROJECT
# =========================
st.markdown(
    """
    <div class="about-box">
        <h2 style="color:#6b4226; margin-top:0; margin-bottom:12px; font-size:24px;">
            Sistem Rekomendasi Resep Nusantara
        </h2>
        <p style="font-size:15px; margin-bottom:12px;">
            Project ini dibuat untuk membantu pengguna menemukan resep masakan Nusantara berdasarkan ketersediaan bahan makanan yang dimiliki di rumah. Pengembangan aplikasi ini ditujukan 
            sebagai pemenuhan tugas <b>Ujian Tengah Semester (UTS) Mata Kuliah Sistem Cerdas</b>.
        </p>
        <p style="font-size:15px; margin-bottom:0;">
            Sistem rekomendasi ini diimplementasikan menggunakan metode <b>Certainty Factor (CF)</b> untuk 
            mengakomodasi ketidakpastian dan menghitung tingkat kepastian kecocokan resep.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# DAFTAR ANGGOTA KELOMPOK
# =========================
st.markdown("<h3 style='color:#6b4226; margin-bottom:15px;'>Anggota Kelompok</h3>", unsafe_allow_html=True)

# Membuat tata letak 3 kolom sejajar untuk profil anggota
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="member-card">
            <span style="font-size:30px; display:block; margin-bottom:8px;"></span>
            <b style="color:#6b4226; font-size:15px; display:block; min-height:45px;">Hasto Timbul Wawandono</b>
            <span style="color:#7c6a5e; font-size:13px;">NIM. 2313010639</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="member-card">
            <span style="font-size:30px; display:block; margin-bottom:8px;"></span>
            <b style="color:#6b4226; font-size:15px; display:block; min-height:45px;">Mohammad Zacky Baihaqie</b>
            <span style="color:#7c6a5e; font-size:13px;">NIM. 2313010651</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="member-card">
            <span style="font-size:30px; display:block; margin-bottom:8px;"></span>
            <b style="color:#6b4226; font-size:15px; display:block; min-height:45px;">Ridwan Hidayatullah</b>
            <span style="color:#7c6a5e; font-size:13px;">NIM. 2313010628</span>
        </div>
        """, 
        unsafe_allow_html=True
    )