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

def detect_categories(title, ingredients):

    title = str(title).lower()

    categories = []


    # =========================
    # DAGING SAPI
    # =========================

    sapi_keywords = [

        "daging sapi",
        "sapi",
        "bakso sapi",
        "rendang sapi",
        "iga sapi",
        "semur sapi"

    ]

    if any(x in title for x in sapi_keywords):

        categories.append(
            "Daging Sapi"
        )


    # =========================
    # DAGING KAMBING
    # =========================

    kambing_keywords = [

        "daging kambing",
        "kambing",
        "sate kambing",
        "gulai kambing",
        "tongseng kambing"

    ]

    if any(x in title for x in kambing_keywords):

        categories.append(
            "Daging Kambing"
        )


    # =========================
    # DAGING AYAM
    # =========================

    ayam_keywords = [

        "ayam",
        "chicken",
        "bakso ayam",
        "rendang ayam"

    ]

    if any(x in title for x in ayam_keywords):

        categories.append(
            "Daging Ayam"
        )


    # =========================
    # IKAN
    # =========================

    ikan_keywords = [

        "ikan ",
        "ikan-",
        "lele",
        "tongkol",
        "gurame",
        "bandeng",
        "patin",
        "tuna",
        "salmon"

    ]

    if any(x in title for x in ikan_keywords):

        categories.append(
            "Ikan"
        )


    # =========================
    # SEAFOOD
    # =========================

    seafood_keywords = [

        "udang",
        "cumi",
        "kepiting",
        "kerang",
        "lobster"

    ]

    if any(x in title for x in seafood_keywords):

        categories.append(
            "Seafood"
        )


    # =========================
    # SAYUR
    # =========================

    sayur_keywords = [

        "sayur",
        "capcay",
        "bayam",
        "kangkung",
        "sop sayur"

    ]

    if any(x in title for x in sayur_keywords):

        categories.append(
            "Sayur"
        )


    # =========================
    # SAMBAL
    # =========================

    if "sambal" in title:

        categories.append(
            "Sambal"
        )


    # =========================
    # SUP & SOTO
    # =========================

    sup_keywords = [

        "sup",
        "sop",
        "soto"

    ]

    if any(x in title for x in sup_keywords):

        categories.append(
            "Sup & Soto"
        )


    # =========================
    # MIE & NASI
    # =========================

    mie_keywords = [

        "mie",
        "mi ",
        "kwetiau",
        "bihun",
        "nasi"

    ]

    if any(x in title for x in mie_keywords):

        categories.append(
            "Mie & Nasi"
        )


    # =========================
    # KUE & DESSERT
    # =========================

    dessert_keywords = [

        "kue",
        "cake",
        "bolu",
        "brownies",
        "puding"

    ]

    if any(x in title for x in dessert_keywords):

        categories.append(
            "Kue & Dessert"
        )


    # =========================
    # MINUMAN
    # =========================

    minuman_keywords = [

        "es ",
        "jus",
        "kopi",
        "teh"

    ]

    if any(x in title for x in minuman_keywords):

        categories.append(
            "Minuman"
        )


    # =========================
    # DEFAULT
    # =========================

    if len(categories) == 0:

        categories.append(
            "Lauk"
        )


    # =========================
    # HAPUS DUPLIKAT
    # =========================

    categories = list(
        dict.fromkeys(categories)
    )


    # =========================
    # BATASI 3 KATEGORI
    # =========================

    categories = categories[:3]


    return categories


# =========================
# TAMBAH KOLOM
# =========================

df["KategoriBaru"] = df.apply(

    lambda row: detect_categories(
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
    "Daging Kambing",
    "Ikan",
    "Seafood",
    "Sambal",
    "Sup & Soto",
    "Mie & Nasi",
    "Kue & Dessert",
    "Minuman"

]


# =========================
# SELECTBOX
# =========================

selected_category = st.selectbox(
    "Pilih Jenis Masakan",
    categories
)


# =========================
# FILTER
# =========================

filtered_df = df[
    df["KategoriBaru"].apply(
        lambda x: selected_category in x
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

    .category-card{
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
        margin-bottom:14px;
    }

    .preview-box{
        background-color:#ede0d4;
        padding:12px;
        border-radius:12px;
        color:#4b3a2f;
        line-height:1.8;
        margin-top:10px;
    }

    .badge{
        background-color:#a47148;
        color:white;
        padding:6px 14px;
        border-radius:999px;
        font-size:13px;
        display:inline-block;
        margin-bottom:12px;
        margin-right:8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# INFO
# =========================

st.info(
    f"Menampilkan {len(filtered_df)} resep kategori {selected_category}"
)


# =========================
# PAGINATION
# =========================

items_per_page = 20

total_data = len(filtered_df)

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


page_data = filtered_df.iloc[
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


    badges = ""

    for cat in row["KategoriBaru"]:

        badges += f"""
        <span class="badge">
            {cat}
        </span>
        """


    st.markdown(
        f"""
        <div class="category-card">

        {badges}

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
        "Lihat Detail Masakan"
    ):

        st.subheader("Kategori")

        st.write(
            ", ".join(
                row["KategoriBaru"]
            )
        )


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