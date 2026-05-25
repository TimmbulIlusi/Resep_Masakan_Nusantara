import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Daftar Resep Nusantara")


# =========================
# STYLE
# =========================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#f5efe6;
    }

    .recipe-card{
        background-color:#fffaf3;
        padding:20px;
        border-radius:16px;
        border:1px solid #dbc4aa;
        margin-bottom:20px;
    }

    .recipe-title{
        color:#6b4226;
        font-size:24px;
        font-weight:bold;
        margin-bottom:12px;
    }

    .recipe-preview{
        background-color:#ede0d4;
        padding:12px;
        border-radius:12px;
        color:#4b3a2f;
        line-height:1.7;
        margin-top:10px;
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
# SEARCH
# =========================

search = st.text_input(
    "Cari Nama Resep"
)


if search:

    filtered_df = df[
        df["Title"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )
    ]

else:

    filtered_df = df


# =========================
# INFO
# =========================

st.info(
    f"Total resep ditemukan: {len(filtered_df)}"
)


# =========================
# TAMPILKAN RESEP
# =========================

for index, row in filtered_df.head(50).iterrows():

    title = str(
        row["Title"]
    )

    ingredients = str(
        row["Ingredients"]
    ).split("--")


    preview = []

    for item in ingredients[:5]:

        item = item.strip()

        if item:

            preview.append(item)


    preview_text = " • ".join(preview)


    st.markdown(
        f"""
        <div class="recipe-card">

        <div class="recipe-title">
            {title}
        </div>

        <div class="recipe-preview">

        <b>Preview Bahan:</b>

        <br><br>

        {preview_text}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    with st.expander(
        "Lihat Detail Resep"
    ):

        st.subheader("Bahan Lengkap")

        for ing in ingredients:

            ing = ing.strip()

            if ing:

                st.write(
                    f"• {ing}"
                )


        st.subheader("Langkah Memasak")

        steps = str(
            row["Steps"]
        )

        if "--" in steps:

            step_list = steps.split("--")

        else:

            step_list = steps.split("\n")


        nomor = 1

        for step in step_list:

            step = step.strip()

            if step:

                st.write(
                    f"{nomor}. {step}"
                )

                nomor += 1