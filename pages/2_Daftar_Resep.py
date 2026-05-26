import streamlit as st
from utils.helper import load_data
from utils.style import load_css

# Load styling halaman
load_css()

st.title("Daftar Resep Nusantara")

# =========================
# STYLE INJECTION (CSS BARU: VINTAGE CATALOG)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5efe6;
    }
    /* Kotak utama bergaya kartu katalog resep klasik */
    .recipe-catalog-card {
        background-color: #fffcf7;
        padding: 6px;
        border-radius: 4px;
        color: #4b3a2f;
    }
    /* Judul menggunakan warna merah bata terakota khas bumbu tradisional */
    .catalog-title {
        color: #b05a3e;
        font-size: 21px;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 10px;
        line-height: 1.3;
        font-family: 'Georgia', serif;
    }
    /* Kotak preview bahan dengan border putus-putus seperti buku resep jadul */
    .catalog-preview {
        background-color: #fbf5ed;
        padding: 12px;
        border-radius: 8px;
        border: 1px dashed #dbc4aa;
        color: #5c4d41;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    /* Label penanda di bagian bawah kartu */
    .catalog-footer {
        font-size: 11px;
        color: #a47148;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD & PREPARE DATA
# =========================
df = load_data()

if "cleaned_title" not in df.columns:
    df["cleaned_title"] = df["Title"].astype(str).str.lower()

# =========================
# INTERFACE PENCARIAN
# =========================
search = st.text_input("Cari Resep", placeholder="Ketik nama masakan, misal: Soto, Rendang...")

if search:
    df = df[df["cleaned_title"].str.contains(search.lower(), na=False)]

st.info(f"Total koleksi ditemukan: **{len(df)}** resep makanan")

# =========================
# LOGIKA PAGINATION
# =========================
items_per_page = 20
total_data = len(df)
total_pages = max(1, (total_data + items_per_page - 1) // items_per_page)

page = st.number_input(
    "Halaman Katalog", min_value=1, max_value=total_pages, value=1, step=1
)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_data = df.iloc[start_idx:end_idx]

# =========================
# TAMPILKAN DATA (GRID 2 KOLOM)
# =========================
col1, col2 = st.columns(2)
grid_columns = [col1, col2]

for idx, (_, row) in enumerate(page_data.iterrows()):
    title = str(row["Title"])
    ingredients = [x.strip() for x in str(row["Ingredients"]).split("--") if x.strip()]
    preview_text = " • ".join(ingredients[:4]) + (" ..." if len(ingredients) > 4 else "")

    with grid_columns[idx % 2]:
        # Menggunakan struktur border tipis Streamlit untuk memperkuat kesan kartu katalog
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="recipe-catalog-card">
                    <div class="catalog-title">📖 {title}</div>
                    <div class="catalog-preview">
                        <span style="color: #b05a3e; font-weight: bold;">Komposisi Utama:</span><br>
                        {preview_text}
                    </div>
                    <div class="catalog-footer">📍 Arsip Kuliner Nusantara</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Tombol detail masuk ke dalam frame kartu
            with st.expander("Buka Catatan Resep"):
                st.write("**Bahan Lengkap:**")
                for ing in ingredients:
                    st.write(f"• {ing}")
                
                st.write("---")
                st.write("**Langkah Pembuatan:**")
                steps = str(row["Steps"])
                step_list = steps.split("--") if "--" in steps else steps.split("\n")
                
                nomor = 1
                for step in step_list:
                    step = step.strip()
                    if step:
                        st.write(f"{nomor}. {step}")
                        nomor += 1

# =========================
# FOOTER PAGE
# =========================
st.markdown(
    f"""
    <div style="text-align:center; padding:20px 0 10px 0; color:#b05a3e; font-weight:bold; font-size:14px; letter-spacing: 1px;">
        — Lembar {page} dari {total_pages} —
    </div>
    """,
    unsafe_allow_html=True
)