import re
import streamlit as st

from utils.helper import load_data
from utils.style import load_css
from model.recommender_cf import RecipeRecommender
from utils.rating import save_rating

# Load styling halaman
load_css()

st.title("Rekomendasi Resep Nusantara")

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# NORMALISASI TEKS
# =========================
def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =========================
# CLEAN BAHAN (STOPWORDS)
# =========================
noise_words = {
    "gram", "kg", "sdm", "sdt", "ml", "buah", "siung", "ruas", "butir",
    "secukupnya", "sesuai", "selera", "haluskan", "cincang", "iris",
    "rebus", "goreng", "kukus", "dan", "atau"
}

def clean_ingredient(item):
    item = normalize(item)
    words = item.split()
    result = []
    
    for word in words:
        if (
            word not in noise_words
            and len(word) > 2
            and not word.isdigit()
        ):
            result.append(word)
            
    return " ".join(result)

# Tambahkan kolom bahan yang bersih ke DataFrame
df["cleaned_ingredients"] = df["Ingredients"].apply(clean_ingredient)

# =========================
# INITIALIZE RECOMMENDER & SESSION
# =========================
recommender = RecipeRecommender(df)

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "recommendation_results" not in st.session_state:
    st.session_state["recommendation_results"] = []

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp{
        background-color:#f5efe6;
    }
    .recipe-card{
        background-color:#fffaf3;
        padding:24px;
        border-radius:18px;
        border:1px solid #dbc4aa;
        margin-bottom:12px;
    }
    .recipe-title{
        color:#6b4226;
        font-size:26px;
        font-weight:bold;
        margin-bottom:12px;
    }
    .match-box{
        background-color:#ede0d4;
        padding:12px;
        border-radius:12px;
        margin-bottom:12px;
        color:#4b3a2f;
        font-size:15px;
    }
    .good-box{
        background-color:#d8f3dc;
        color:#1b4332;
        padding:12px;
        border-radius:12px;
        margin-bottom:12px;
        font-size:15px;
    }
    .missing-box{
        background-color:#ffe5d9;
        color:#9c6644;
        padding:12px;
        border-radius:12px;
        margin-bottom:4px;
        font-size:15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# INTERFACE INPUT USER
# =========================
user_input = st.text_input(
    "Masukkan bahan yang tersedia",
    placeholder="contoh: ayam, bawang putih, telur"
)

btn_cari = st.button("Cari Rekomendasi")

# =========================
# PROSES PENCARIAN & CERTAINTY FACTOR
# =========================
if btn_cari or (user_input.strip() != ""):
    results = recommender.recommend(user_input)
    
    # Bersihkan inputan bahan dari user
    user_ingredients = [
        clean_ingredient(x)
        for x in user_input.split(",")
        if x.strip()
    ]
    
    final_results = []

    for index, row in results.iterrows():
        raw_ingredients = str(row["Ingredients"])

        # Ekstrak daftar bahan asli dari resep
        ingredient_list = [
            clean_ingredient(x)
            for x in raw_ingredients.split("--")
            if x.strip()
        ]
        ingredient_list = [x for x in ingredient_list if x]
        
        n_bahan = len(ingredient_list)
        if n_bahan == 0:
            continue

        # Pembagian bobot pakar (CF Pakar) secara merata per gejala/bahan
        cf_pakar_per_bahan = 1.0 / n_bahan

        matched = []
        cf_total = 0.0
        first_match = True

        # Proses pencocokan string dan perhitungan akumulasi Certainty Factor
        for recipe_item in ingredient_list:
            is_matched = False
            for user_item in user_ingredients:
                if user_item in recipe_item:
                    is_matched = True
                    matched.append(user_item)
                    break
            
            if is_matched:
                # Nilai CF untuk gejala ini (User diasumsikan 100% yakin punya bahannya = 1.0)
                cf_gejala = cf_pakar_per_bahan * 1.0
                
                # Gunakan rumus kombinasi Certainty Factor
                if first_match:
                    cf_total = cf_gejala
                    first_match = False
                else:
                    cf_total = cf_total + cf_gejala * (1.0 - cf_total)

        matched = list(set(matched))

        # Cari tahu bahan apa saja yang kurang dari resep
        missing = []
        for recipe_item in ingredient_list:
            found = False
            for user_item in user_ingredients:
                if user_item in recipe_item:
                    found = True
                    break
            if not found:
                missing.append(recipe_item)

        # ========================================================
        # PENYESUAIAN LOGIS: Jika bahan lengkap, otomatis 100% cocok
        # ========================================================
        if len(missing) == 0:
            percentage = 100
        else:
            percentage = int(cf_total * 100)

        final_results.append({
            "title": row["Title"],
            "category": row["Category"],
            "ingredients": ingredient_list,
            "steps": row["Steps"],
            "percentage": percentage,  # Persentase berbasis Certainty Factor / Override 100%
            "matched": matched,
            "missing": missing[:8],
            "index": index
        })

    # Urutkan resep berdasarkan persentase Certainty Factor tertinggi
    final_results = sorted(
        final_results,
        key=lambda x: x["percentage"],
        reverse=True
    )

    st.session_state["recommendation_results"] = final_results[:5]


# =========================
# TAMPILKAN HASIL REKOMENDASI (VERSI RAPI)
# =========================
results = st.session_state["recommendation_results"]

if results and user_input.strip() != "":
    for item in results:
        with st.container():
            # Join teks bahan terlebih dahulu untuk dimasukkan ke dalam HTML
            str_matched = ", ".join(item["matched"]) if item["matched"] else "Tidak ada bahan yang cocok"
            str_missing = ", ".join(item["missing"]) if item["missing"] else "Semua bahan terpenuhi"
            
            # Tampilan Card Utama (Terbungkus utuh dalam .recipe-card)
            st.markdown(
                f"""
                <div class="recipe-card">
                    <div class="recipe-title">{item["title"]}</div>
                    <div class="match-box">
                        <b>Kategori:</b> {item["category"]} &nbsp;|&nbsp; 
                        <b>Tingkat Kecocokan:</b> <span style="font-weight:bold; color:#6b4226;">{item["percentage"]}%</span>
                    </div>
                    <div class="good-box">
                        <b>Bahan Yang Cocok:</b> {str_matched}
                    </div>
                    <div class="missing-box">
                        <b>Bahan Yang Kurang:</b> {str_missing}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expander Detail Bahan dan Langkah (Diletakkan tepat di bawah card agar rapi)
            with st.expander("Lihat Semua Bahan & Langkah Memasak"):
                st.write("**Semua Bahan Asli Resep:**")
                for ing in item["ingredients"]:
                    st.write(f"• {ing}")
                
                st.write("---")
                st.write("**Langkah-Langkah Memasak:**")
                steps = str(item["steps"])
                step_list = steps.split("--") if "--" in steps else steps.split("\n")

                nomor = 1
                for step in step_list:
                    step = step.strip()
                    if step:
                        st.write(f"{nomor}. {step}")
                        nomor += 1

            # Kolom Aksi Tombol (Favorit & Sistem Rating Bintang)
            col_fav, col_rate_ui, col_rate_btn = st.columns([3, 3, 2])
            
            with col_fav:
                if st.button("🤎 Favorit", key=f"fav_{item['index']}", use_container_width=True):
                    if item["title"] not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item["title"])
                        st.toast("Berhasil ditambahkan ke favorit")
                    else:
                        st.info("Resep sudah ada di favorit")

            with col_rate_ui:
                rating_value = st.radio(
                    "Rating",
                    [1, 2, 3, 4, 5],
                    horizontal=True,
                    key=f"rating_{item['index']}",
                    label_visibility="collapsed"
                )

            with col_rate_btn:
                if st.button("⭐ Simpan", key=f"save_rating_{item['index']}", use_container_width=True):
                    save_rating("anonymous_user", item["title"], rating_value)
                    st.success("Tersimpan")
            
            # Pemberi jarak antar kontainer resep
            st.markdown("<br>", unsafe_allow_html=True)