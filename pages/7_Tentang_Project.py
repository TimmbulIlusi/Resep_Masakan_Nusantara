import streamlit as st

from utils.style import load_css


load_css()

st.title("Tentang Project")


# =========================
# STYLE
# =========================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#f5efe6;
    }

    .about-box{
        background-color:#fffaf3;
        padding:24px;
        border-radius:18px;
        border:1px solid #dbc4aa;
        margin-bottom:20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# PROJECT
# =========================

st.markdown(
    """
    <div class="about-box">

    <h2 style="color:#6b4226;">
        Sistem Rekomendasi Resep Nusantara
    </h2>

    <p>
    Project ini dibuat untuk membantu
    pengguna menemukan resep makanan
    berdasarkan bahan yang tersedia. Sekaligus sebagai tugas Ujian Tengah Semester Mata Kuliah Sistem Cerdas.
    </p>

    <p>
    Sistem rekomendasi menggunakan
    metode TF-IDF dan
    Cosine Similarity.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# ANGGOTA
# =========================

st.subheader("Anggota Kelompok")

st.write(
    "1. Hasto Timbul Wawandono (2313010639)"
)

st.write(
    "2. Mohammad Zacky Baihaqie (2313010651)"
)

st.write(
    "3. Ridwan Hidayatullah (2313010628)"
)


# =========================
# TEKNOLOGI
# =========================

st.subheader("Teknologi Yang Digunakan")

st.write("• Python")
st.write("• Streamlit")
st.write("• Pandas")
st.write("• Scikit-Learn")
st.write("• TF-IDF")
st.write("• Cosine Similarity")