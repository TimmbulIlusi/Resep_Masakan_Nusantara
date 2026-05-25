import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Eksplorasi Kategori Masakan Nusantara")


# =========================
# LOAD DATA
# =========================

df = load_data()


# =========================
# DETEKSI KATEGORI
# =========================

def detect_category(title, ingredients):

    text = f"{title} {ingredients}".lower()


    # SAYUR
    if any(x in text for x in [

        "sayur",
        "bayam",
        "kangkung",
        "buncis",
        "wortel",
        "kol",
        "sawi",
        "terong",
        "daun singkong",
        "tumis"

    ]):

        return "Sayur"


    # DAGING SAPI
    elif any(x in text for x in [

        "sapi",
        "daging sapi",
        "rendang",
        "bakso",
        "iga"

    ]):

        return "Daging Sapi"


    # AYAM
    elif any(x in text for x in [

        "ayam",
        "chicken"

    ]):

        return "Daging Ayam"


    # IKAN
    elif any(x in text for x in [

        "ikan",
        "lele",
        "tongkol",
        "gurame",
        "bandeng",
        "nila",
        "patin",
        "tuna"

    ]):

        return "Ikan"


    # SEAFOOD
    elif any(x in text for x in [

        "udang",
        "cumi",
        "kepiting",
        "kerang",
        "lobster"

    ]):

        return "Seafood"


    # SAMBAL
    elif any(x in text for x in [

        "sambal",
        "balado"

    ]):

        return "Sambal"


    # SUP
    elif any(x in text for x in [

        "sup",
        "sop",
        "soto"

    ]):

        return "Sup & Soto"


    # GORENGAN
    elif any(x in text for x in [

        "goreng",
        "bakwan",
        "mendoan",
        "risol"

    ]):

        return "Gorengan"


    # MIE & NASI
    elif any(x in text for x in [

        "mie",
        "mi ",
        "bihun",
        "kwetiau",
        "nasi"

    ]):

        return "Mie & Nasi"


    # KUE
    elif any(x in text for x in [

        "kue",
        "cake",
        "bolu",
        "brownies",
        "puding"

    ]):

        return "Kue & Dessert"


    # MINUMAN
    elif any(x in text for x in [

        "es ",
        "jus",
        "kopi",
        "teh",
        "susu"

    ]):

        return "Minuman"


    else:

        return "Lauk"


# =========================
# TAMBAH KATEGORI
# =========================

df["KategoriBaru"] = df.apply(

    lambda row: detect_category(
        row["Title"],
        row["Ingredients"]
    ),

    axis=1
)


# =========================
# LIST KATEGORI
# =========================

categories = [

    "Sayur",
    "Lauk",
    "Daging Ayam",
    "Daging Sapi",
    "Ikan",
    "Seafood",
    "Sambal",
    "Sup & Soto",
    "Gorengan",
    "Mie & Nasi",
    "Kue & Dessert",
    "Minuman"

]


# =========================
# PILIH KATEGORI
# =========================

selected_category = st.selectbox(
    "Pilih Jenis Masakan",
    categories
)


# =========================
# FILTER DATA
# =========================

filtered_df = df[
    df["KategoriBaru"] == selected_category
]


# =========================
# HEADER INFO
# =========================

st.markdown(
    f"""
    <div style="
        background-color:#dbe4ea;
        padding:20px;
        border-radius:16px;
        margin-top:10px;
        margin-bottom:25px;
        border:1px solid #c5d0d8;
    ">

    <h3 style="
        color:#1f2937;
        margin-bottom:8px;
    ">
        {selected_category}
    </h3>

    <div style="
        color:#4b5563;
        font-size:15px;
    ">
        Total resep ditemukan:
        <b>{len(filtered_df)}</b>
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# CARD RESEP
# =========================

for index, row in filtered_df.head(30).iterrows():

    recipe_title = str(
        row["Title"]
    )

    ingredients = str(
        row["Ingredients"]
    ).split("--")


    # preview bahan
    preview = []

    for item in ingredients[:5]:

        item = item.strip()

        if item:

            preview.append(item)


    preview_text = " • ".join(preview)


    with st.container(border=True):

        col1, col2 = st.columns([4, 1])


        with col1:

            st.markdown(
                f"""
                <div style="
                    padding:5px 5px 5px 0px;
                ">

                <h3 style="
                    color:#111827;
                    margin-bottom:12px;
                ">
                    {recipe_title}
                </h3>

                <div style="
                    background-color:#eef2f7;
                    color:#334155;
                    padding:12px;
                    border-radius:10px;
                    line-height:1.7;
                    font-size:14px;
                ">

                <b>Bahan Utama:</b>

                <br><br>

                {preview_text}

                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
                <div style="
                    background-color:#cbd5e1;
                    color:#1e293b;
                    text-align:center;
                    padding:10px;
                    border-radius:12px;
                    margin-top:10px;
                    font-size:13px;
                    font-weight:bold;
                ">
                    {selected_category}
                </div>
                """,
                unsafe_allow_html=True
            )


        with st.expander("Lihat Detail Masakan"):

            st.markdown("### Bahan Lengkap")

            for ing in ingredients:

                ing = ing.strip()

                if ing:

                    st.write(f"• {ing}")


            st.markdown("### Langkah Memasak")

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