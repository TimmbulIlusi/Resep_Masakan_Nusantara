import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Informasi Dataset")


# =========================
# STYLE
# =========================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#f5efe6;
    }

    .info-box{
        background-color:#fffaf3;
        padding:22px;
        border-radius:16px;
        border:1px solid #dbc4aa;
        margin-bottom:20px;
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
# INFO
# =========================

st.markdown(
    f"""
    <div class="info-box">

    <h3 style="color:#6b4226;">
        Ringkasan Dataset
    </h3>

    <p>
    Dataset berisi berbagai resep
    makanan khas Indonesia
    yang digunakan untuk
    sistem rekomendasi resep.
    </p>

    <ul>
        <li>Total Data: <b>{len(df)}</b></li>
        <li>Total Kolom: <b>{len(df.columns)}</b></li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)


st.subheader("Kolom Dataset")

for col in df.columns:

    st.write(f"• {col}")


st.subheader("Preview Dataset")

st.dataframe(
    df.head(20),
    use_container_width=True
)