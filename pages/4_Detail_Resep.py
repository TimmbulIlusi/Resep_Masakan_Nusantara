import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Detail Resep Nusantara")


# =========================
# LOAD DATA
# =========================

df = load_data()


# =========================
# SEARCH
# =========================

search = st.text_input(
    "Cari resep",
    placeholder="contoh: rendang, sate, ayam goreng"
)


# =========================
# FILTER DATA
# =========================

if "cleaned_title" not in df.columns:

    df["cleaned_title"] = (
        df["Title"]
        .astype(str)
        .str.lower()
    )


if search:

    filtered_df = df[
        df["cleaned_title"].str.contains(
            search.lower(),
            na=False
        )
    ]

else:

    filtered_df = df


# =========================
# PILIH RESEP
# =========================

recipe_names = filtered_df[
    "Title"
].tolist()


selected_recipe = st.selectbox(
    "Pilih Resep",
    recipe_names
)


# =========================
# AMBIL DATA
# =========================

recipe = filtered_df[
    filtered_df["Title"] == selected_recipe
].iloc[0]


recipe_title = str(
    recipe["Title"]
)

recipe_category = str(
    recipe["Category"]
)


# =========================
# STYLE
# =========================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#f5efe6;
    }

    .header-card{
        background:linear-gradient(
            135deg,
            #8b5e34,
            #a47148
        );
        padding:28px;
        border-radius:20px;
        margin-bottom:25px;
        box-shadow:0 4px 12px rgba(
            0,
            0,
            0,
            0.08
        );
    }

    .recipe-title{
        color:white;
        font-size:34px;
        font-weight:bold;
        margin-bottom:12px;
    }

    .recipe-category{
        background-color:rgba(
            255,
            255,
            255,
            0.18
        );
        color:#fff7ed;
        padding:8px 16px;
        border-radius:999px;
        display:inline-block;
        font-size:14px;
        font-weight:bold;
    }

    .section-title{
        background-color:#ede0d4;
        padding:16px;
        border-radius:14px;
        margin-top:20px;
        margin-bottom:15px;
        border:1px solid #dbc4aa;
    }

    .section-title h3{
        color:#6b4226;
        margin:0;
    }

    .ingredient-card{
        background-color:#fffaf3;
        padding:14px;
        border-radius:12px;
        margin-bottom:12px;
        border-left:6px solid #a47148;
        color:#4b3a2f;
        box-shadow:0 2px 6px rgba(
            0,
            0,
            0,
            0.04
        );
    }

    .step-card{
        background-color:#fffaf3;
        padding:18px;
        border-radius:14px;
        margin-bottom:16px;
        border:1px solid #dbc4aa;
        color:#4b3a2f;
        box-shadow:0 2px 8px rgba(
            0,
            0,
            0,
            0.05
        );
    }

    .step-number{
        background-color:#a47148;
        color:white;
        display:inline-block;
        padding:6px 14px;
        border-radius:999px;
        font-size:13px;
        font-weight:bold;
        margin-bottom:14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# HEADER
# =========================

st.markdown(
    f"""
    <div class="header-card">

    <div class="recipe-title">
        {recipe_title}
    </div>

    <div class="recipe-category">
        Kategori: {recipe_category}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# BAHAN
# =========================

st.markdown(
    """
    <div class="section-title">
        <h3>Bahan-Bahan</h3>
    </div>
    """,
    unsafe_allow_html=True
)


ingredients = str(
    recipe["Ingredients"]
).split("--")


for item in ingredients:

    item = item.strip()

    if item:

        st.markdown(
            f"""
            <div class="ingredient-card">
                • {item}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# LANGKAH
# =========================

st.markdown(
    """
    <div class="section-title">
        <h3>Langkah Memasak</h3>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# PARSING LANGKAH
# =========================

raw_steps = str(
    recipe["Steps"]
)


if "--" in raw_steps:

    steps = raw_steps.split("--")

else:

    steps = raw_steps.split("\n")


# =========================
# TAMPILKAN LANGKAH
# =========================

step_number = 1

for step in steps:

    step = step.strip()

    if step:

        st.markdown(
            f"""
            <div class="step-card">

            <div class="step-number">
                Langkah {step_number}
            </div>

            <div>
                {step}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        step_number += 1