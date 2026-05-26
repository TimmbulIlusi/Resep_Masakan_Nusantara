import streamlit as st
from utils.helper import load_data
from utils.style import load_css

# Load styling halaman
load_css()

st.title("Eksplorasi Kategori Masakan")

# =========================
# STYLE INJECTION (CSS)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5efe6;
    }
    .category-card {
        background-color: #fffaf3;
        padding: 5px;
        border-radius: 8px;
        color: #4b3a2f;
    }
    .recipe-title {
        color: #6b4226;
        font-size: 20px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 12px;
        line-height: 1.3;
    }
    .preview-box {
        background-color: #ede0d4;
        padding: 10px;
        border-radius: 10px;
        color: #4b3a2f;
        line-height: 1.5;
        font-size: 13px;
        margin-bottom: 12px;
    }
    .badge {
        background-color: #a47148;
        color: white;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 11px;
        display: inline-block;
        margin-bottom: 4px;
        margin-right: 5px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# CACHED CATEGORY DETECTION (ANTI-LAG)
# =========================
def detect_categories(title, ingredients):
    title = str(title).lower()
    categories = []

    keywords = {
        "Daging Sapi": ["daging sapi", "sapi", "bakso sapi", "rendang sapi", "iga sapi", "semur sapi"],
        "Daging Kambing": ["daging kambing", "kambing", "sate kambing", "gulai kambing", "tongseng kambing"],
        "Daging Ayam": ["ayam", "chicken", "bakso ayam", "rendang ayam"],
        "Ikan": ["ikan ", "ikan-", "lele", "tongkol", "gurame", "bandeng", "patin", "tuna", "salmon"],
        "Seafood": ["udang", "cumi", "kepiting", "kerang", "lobster"],
        "Sayur": ["sayur", "capcay", "bayam", "kangkung", "sop sayur"],
        "Sambal": ["sambal"],
        "Sup & Soto": ["sup", "sop", "soto"],
        "Mie & Nasi": ["mie", "mi ", "kwetiau", "bihun", "nasi"],
        "Kue & Dessert": ["kue", "cake", "bolu", "brownies", "puding"],
        "Minuman": ["es ", "jus", "kopi", "teh"]
    }

    for cat_name, key_list in keywords.items():
        if any(x in title for x in key_list):
            categories.append(cat_name)

    if not categories:
        categories.append("Lauk")

    # Hapus duplikat & batasi 3 kategori tertinggi
    categories = list(dict.fromkeys(categories))
    return categories[:3]

@st.cache_data
def get_processed_data():
    data = load_data()
    data["KategoriBaru"] = data.apply(
        lambda row: detect_categories(row["Title"], row["Ingredients"]), axis=1
    )
    return data

# Ambil data yang sudah ter-cache aman
df = get_processed_data()

# =========================
# INTERFACE FILTER KATEGORI
# =========================
categories_list = [
    "Sayur", "Lauk", "Daging Ayam", "Daging Sapi", "Daging Kambing", 
    "Ikan", "Seafood", "Sambal", "Sup & Soto", "Mie & Nasi", "Kue & Dessert", "Minuman"
]

selected_category = st.selectbox("Pilih Jenis Masakan", categories_list)

# Filter Berdasarkan Kategori Terpilih
filtered_df = df[df["KategoriBaru"].apply(lambda x: selected_category in x)]

st.info(f"Menampilkan {len(filtered_df)} resep kategori **{selected_category}**")

# =========================
# LOGIKA PAGINATION
# =========================
items_per_page = 20
total_data = len(filtered_df)
total_pages = max(1, (total_data + items_per_page - 1) // items_per_page)

# Navigasi halaman diletakkan di atas agar user tidak perlu scroll jauh ke bawah
page = st.number_input(
    "Halaman", min_value=1, max_value=total_pages, value=1, step=1
)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_data = filtered_df.iloc[start_idx:end_idx]

# =========================
# DISPLAY DAFTAR RESEP (GRID 2 KOLOM)
# =========================
col1, col2 = st.columns(2)
grid_columns = [col1, col2]

for idx, (_, row) in enumerate(page_data.iterrows()):
    title = str(row["Title"])
    ingredients = [x.strip() for x in str(row["Ingredients"]).split("--") if x.strip()]
    preview_text = " • ".join(ingredients[:4]) + (" ..." if len(ingredients) > 4 else "")

    # Render badge HTML kategori
    badges_html = "".join([f'<span class="badge">{cat}</span>' for cat in row["KategoriBaru"]])

    with grid_columns[idx % 2]:
        # Kotak container pembungkus utama resep
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="category-card">
                    <div>{badges_html}</div>
                    <div class="recipe-title">{title}</div>
                    <div class="preview-box">
                        <b>Preview Bahan:</b><br>{preview_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expander masuk ke dalam container agar menyatu secara visual
            with st.expander("Lihat Detail Masakan"):
                st.write("**Bahan Lengkap:**")
                for ing in ingredients:
                    st.write(f"• {ing}")
                
                st.write("---")
                st.write("**Langkah Memasak:**")
                steps_data = str(row["Steps"])
                step_list = steps_data.split("--") if "--" in steps_data else steps_data.split("\n")
                
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
    <div style="text-align:center; padding:20px 0 10px 0; color:#6b4226; font-weight:bold; font-size:14px;">
        Halaman {page} dari {total_pages}
    </div>
    """,
    unsafe_allow_html=True
)