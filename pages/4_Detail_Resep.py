import streamlit as st
from utils.helper import load_data
from utils.style import load_css

# Load styling halaman
load_css()

st.title("Detail Resep Nusantara")

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color:#f5efe6;
    }
    .header-card {
        background: linear-gradient(135deg, #8b5e34, #a47148);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .recipe-title {
        color: white;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .recipe-category {
        background-color: rgba(255, 255, 255, 0.18);
        color: #fff7ed;
        padding: 6px 16px;
        border-radius: 999px;
        display: inline-block;
        font-size: 13px;
        font-weight: bold;
    }
    .section-title {
        background-color: #ede0d4;
        padding: 12px 16px;
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 15px;
        border: 1px solid #dbc4aa;
    }
    .section-title h3 {
        color: #6b4226;
        margin: 0;
        font-size: 18px;
    }
    .ingredient-container {
        background-color: #fffaf3;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #dbc4aa;
        color: #4b3a2f;
    }
    .ingredient-line {
        padding: 6px 0;
        border-bottom: 1px dashed #ede0d4;
        font-size: 14px;
    }
    .ingredient-line:last-child {
        border-bottom: none;
    }
    .step-card {
        background-color: #fffaf3;
        padding: 16px;
        border-radius: 14px;
        margin-bottom: 14px;
        border: 1px solid #dbc4aa;
        color: #4b3a2f;
    }
    .step-number {
        background-color: #a47148;
        color: white;
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
df = load_data()

# Normalisasi kolom pencarian judul jika belum ada
if "cleaned_title" not in df.columns:
    df["cleaned_title"] = df["Title"].astype(str).str.lower()

# =========================
# INTERFACE PENCARIAN
# =========================
search = st.text_input(
    "Cari resep",
    placeholder="contoh: rendang, sate, ayam goreng"
)

# Filter dataframe berdasarkan input user
if search:
    filtered_df = df[df["cleaned_title"].str.contains(search.lower(), na=False)]
else:
    filtered_df = df

# =========================
# DROP-DOWN PILIH RESEP & VALIDASI
# =========================
recipe_names = filtered_df["Title"].tolist()

if not recipe_names:
    st.warning("Resep tidak ditemukan. Coba masukkan kata kunci pencarian yang lain.")
else:
    selected_recipe = st.selectbox("Pilih hasil resep yang ditemukan:", recipe_names)

    # Ambil baris data resep yang dipilih pengguna
    recipe_data = filtered_df[filtered_df["Title"] == selected_recipe]
    
    if not recipe_data.empty:
        recipe = recipe_data.iloc[0]
        recipe_title = str(recipe["Title"])
        recipe_category = str(recipe["Category"])

        # =========================
        # RENDER BANNER HEADER RESEP
        # =========================
        st.markdown(
            f"""
            <div class="header-card">
                <div class="recipe-title">{recipe_title}</div>
                <div class="recipe-category">Kategori: {recipe_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Membuat struktur layout 2 kolom berdampingan
        col_left, col_right = st.columns([2, 3])

        # =========================
        # KOLOM KIRI: BAHAN-BAHAN
        # =========================
        with col_left:
            st.markdown('<div class="section-title"><h3>Bahan-Bahan</h3></div>', unsafe_allow_html=True)
            
            raw_ingredients = str(recipe["Ingredients"]).split("--")
            
            # Gabungkan seluruh item ke dalam satu blok HTML murni untuk performa render cepat
            ingredients_html = ""
            for item in raw_ingredients:
                item = item.strip()
                if item:
                    ingredients_html += f'<div class="ingredient-line">🔹 {item}</div>'
            
            st.markdown(f'<div class="ingredient-container">{ingredients_html}</div>', unsafe_allow_html=True)

        # =========================
        # KOLOM KANAN: LANGKAH MEMASAK
        # =========================
        with col_right:
            st.markdown('<div class="section-title"><h3>Langkah Memasak</h3></div>', unsafe_allow_html=True)
            
            raw_steps = str(recipe["Steps"])
            steps = raw_steps.split("--") if "--" in raw_steps else raw_steps.split("\n")
            
            step_number = 1
            for step in steps:
                step = step.strip()
                if step:
                    st.markdown(
                        f"""
                        <div class="step-card">
                            <div class="step-number">Langkah {step_number}</div>
                            <div style="font-size:14px; line-height:1.5;">{step}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    step_number += 1