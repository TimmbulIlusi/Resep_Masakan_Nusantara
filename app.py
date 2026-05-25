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
# STYLE
# =========================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#f5efe6;
    }

    section[data-testid="stSidebar"]{
        background-color:#dbc1ac;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# HEADER
# =========================

st.title("🍲 Sistem Rekomendasi Resep Masakan Nusantara")

st.markdown("""

Aplikasi ini membantu pengguna menemukan
berbagai resep khas Indonesia
berdasarkan bahan yang tersedia.

Sistem rekomendasi menggunakan metode
**TF-IDF** dan **Cosine Similarity**
untuk menampilkan resep
yang paling relevan.

""")


st.divider()


# =========================
# FITUR
# =========================

st.subheader("Fitur Utama")


col1, col2, col3 = st.columns(3)


with col1:

    st.info("""

### 🔍 Rekomendasi Resep

Cari resep berdasarkan
bahan yang dimiliki pengguna.

""")


with col2:

    st.success("""

### 🥘 Detail Bahan

Menampilkan bahan cocok,
bahan kurang,
dan langkah memasak.

""")


with col3:

    st.warning("""

### 📚 Kategori Masakan

Resep dikelompokkan
berdasarkan jenis masakan.

""")


st.divider()


# =========================
# INFORMASI
# =========================

st.subheader("Tentang Aplikasi")

st.write(
    """
    Dataset yang digunakan berisi
    ribuan resep makanan Indonesia.

    Aplikasi ini dirancang untuk membantu
    pengguna menemukan ide masakan
    dengan tampilan sederhana,
    nyaman dibaca,
    dan mudah digunakan.
    """
)


st.divider()


# =========================
# FOOTER
# =========================

st.caption(
    "Sistem Cerdas • Sistem Rekomendasi Resep Nusantara"
)