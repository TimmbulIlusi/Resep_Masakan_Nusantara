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
# HEADER
# =========================

st.markdown(
    f"""
    <div style="
        background-color:#dfe3e8;
        padding:20px;
        border-radius:12px;
        margin-bottom:20px;
        border:1px solid #cbd5e1;
    ">

    <h2 style="
        color:#1f2937;
        margin-bottom:10px;
    ">
        {recipe_title}
    </h2>

    <div style="
        color:#4b5563;
        font-size:15px;
    ">
        <b>Kategori:</b>
        {recipe_category}
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
    <div style="
        background-color:#dfe3e8;
        padding:15px;
        border-radius:12px;
        margin-bottom:15px;
        border:1px solid #cbd5e1;
    ">

    <h3 style="
        color:#1e40af;
        margin:0;
    ">
        Bahan-Bahan
    </h3>

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
            <div style="
                background-color:#f3f4f6;
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
                border-left:4px solid #94a3b8;
                color:#111827;
            ">
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
    <div style="
        background-color:#dfe3e8;
        padding:15px;
        border-radius:12px;
        margin-top:25px;
        margin-bottom:15px;
        border:1px solid #cbd5e1;
    ">

    <h3 style="
        color:#1e40af;
        margin:0;
    ">
        Langkah Memasak
    </h3>

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

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="
                    background-color:#f8fafc;
                    padding:15px;
                    border-radius:10px;
                    color:#111827;
                ">

                <b>Langkah {step_number}</b>

                <br><br>

                {step}

                </div>
                """,
                unsafe_allow_html=True
            )

        step_number += 1