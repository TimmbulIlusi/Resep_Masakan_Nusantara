import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Daftar Resep Nusantara")


# =========================
# LOAD DATA
# =========================

df = load_data()


# =========================
# SEARCH
# =========================

search = st.text_input(
    "Cari Resep"
)


if search:

    df = df[
        df["cleaned_title"].str.contains(
            search.lower(),
            na=False
        )
    ]


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
        padding:22px;
        border-radius:18px;
        border:1px solid #dbc4aa;
        margin-bottom:20px;
    }

    .recipe-title{
        color:#6b4226;
        font-size:24px;
        font-weight:bold;
        margin-bottom:12px;
    }

    .preview-box{
        background-color:#ede0d4;
        padding:12px;
        border-radius:12px;
        color:#4b3a2f;
        line-height:1.8;
        margin-top:10px;
    }

    .info-badge{
        background-color:#a47148;
        color:white;
        padding:6px 14px;
        border-radius:999px;
        font-size:13px;
        display:inline-block;
        margin-bottom:14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# INFO
# =========================

st.info(
    f"Total resep ditemukan: {len(df)}"
)


# =========================
# PAGINATION
# =========================

items_per_page = 20

total_data = len(df)

total_pages = total_data // items_per_page

if total_data % items_per_page != 0:

    total_pages += 1


page = st.number_input(

    "Halaman",

    min_value=1,

    max_value=max(total_pages, 1),

    value=1,

    step=1

)


start_idx = (
    (page - 1)
    * items_per_page
)

end_idx = (
    start_idx
    + items_per_page
)


page_data = df.iloc[
    start_idx:end_idx
]


# =========================
# TAMPILKAN DATA
# =========================

for index, row in page_data.iterrows():

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

        <div class="info-badge">
            Resep Nusantara
        </div>

        <div class="recipe-title">
            {title}
        </div>

        <div class="preview-box">

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

        st.subheader(
            "Bahan Lengkap"
        )

        for ing in ingredients:

            ing = ing.strip()

            if ing:

                st.write(
                    f"• {ing}"
                )


        st.subheader(
            "Langkah Memasak"
        )

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


# =========================
# FOOTER PAGE
# =========================

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:12px;
        color:#6b4226;
        font-weight:bold;
    ">
        Halaman {page} dari {total_pages}
    </div>
    """,
    unsafe_allow_html=True
)