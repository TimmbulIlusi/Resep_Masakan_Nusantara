import re
import streamlit as st

from utils.helper import load_data
from utils.style import load_css
from model.recommender_cf import RecipeRecommender


load_css()

st.title("Rekomendasi Resep Nusantara")

df = load_data()

recommender = RecipeRecommender(df)


# =========================
# SESSION
# =========================

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "recommendation_results" not in st.session_state:
    st.session_state["recommendation_results"] = []


# =========================
# INPUT
# =========================

user_input = st.text_input(
    "Masukkan bahan yang tersedia",
    placeholder="contoh: ayam, bawang putih, telur"
)


# =========================
# NORMALISASI
# =========================

def normalize(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z0-9 ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================
# CLEAN BAHAN
# =========================

noise_words = {

    "gram",
    "kg",
    "sdm",
    "sdt",
    "ml",
    "buah",
    "siung",
    "ruas",
    "butir",
    "secukupnya",
    "sesuai",
    "selera",
    "haluskan",
    "cincang",
    "iris",
    "rebus",
    "goreng",
    "kukus",
    "dan",
    "atau"

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


# =========================
# SEARCH
# =========================

if st.button("Cari Rekomendasi"):

    results = recommender.recommend(
        user_input
    )

    user_ingredients = [

        clean_ingredient(x)

        for x in user_input.split(",")

        if x.strip()
    ]

    final_results = []


    for index, row in results.iterrows():

        raw_ingredients = str(
            row["Ingredients"]
        )


        # parsing berdasarkan --
        ingredient_list = [

            clean_ingredient(x)

            for x in raw_ingredients.split("--")

            if x.strip()
        ]


        ingredient_list = [

            x for x in ingredient_list

            if x
        ]


        # =========================
        # CARI YANG COCOK
        # =========================

        matched = []

        for user_item in user_ingredients:

            for recipe_item in ingredient_list:

                if user_item in recipe_item:

                    matched.append(user_item)


        matched = list(set(matched))


        # =========================
        # PERSENTASE BENAR
        # =========================

        percentage = int(

            (len(matched) / len(ingredient_list)) * 100

        ) if len(ingredient_list) > 0 else 0


        # =========================
        # BAHAN KURANG
        # =========================

        missing = []

        for recipe_item in ingredient_list:

            found = False

            for user_item in user_ingredients:

                if user_item in recipe_item:

                    found = True
                    break

            if not found:

                missing.append(recipe_item)


        final_results.append({

            "title": row["Title"],

            "category": row["Category"],

            "ingredients": ingredient_list,

            "steps": row["Steps"],

            "percentage": percentage,

            "matched": matched,

            "missing": missing[:8],

            "index": index

        })


    # SORT
    final_results = sorted(

        final_results,

        key=lambda x: x["percentage"],

        reverse=True
    )

    st.session_state[
        "recommendation_results"
    ] = final_results[:20]


# =========================
# TAMPILKAN
# =========================

results = st.session_state[
    "recommendation_results"
]


if results:

    for item in results:

        with st.container(border=True):

            st.subheader(
                item["title"]
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"Kategori: {item['category']}"
                )

            with col2:

                st.write(
                    f"Kecocokan: {item['percentage']}%"
                )


            # =========================
            # BAHAN COCOK
            # =========================

            st.markdown(
                """
                <div style="
                    background-color:#dbeafe;
                    color:#1e3a5f;
                    padding:12px;
                    border-radius:10px;
                    margin-top:10px;
                    margin-bottom:10px;
                ">
                <b>Bahan Yang Cocok</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                ", ".join(item["matched"])
            )


            # =========================
            # BAHAN KURANG
            # =========================

            st.markdown(
                """
                <div style="
                    background-color:#fde7e7;
                    color:#8b1e1e;
                    padding:12px;
                    border-radius:10px;
                    margin-top:10px;
                    margin-bottom:10px;
                ">
                <b>Bahan Yang Kurang</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                ", ".join(item["missing"])
            )


            # =========================
            # DETAIL
            # =========================

            with st.expander(
                "Lihat Semua Bahan"
            ):

                for ing in item["ingredients"]:

                    st.write(
                        f"• {ing}"
                    )


            with st.expander(
                "Lihat Langkah Memasak"
            ):

                st.write(
                    item["steps"]
                )


            # =========================
            # FAVORIT
            # =========================

            if st.button(
                "Tambah ke Favorit",
                key=f"fav_{item['index']}"
            ):

                if (
                    item["title"]
                    not in st.session_state[
                        "favorites"
                    ]
                ):

                    st.session_state[
                        "favorites"
                    ].append(
                        item["title"]
                    )

                    st.toast(
                        "Berhasil ditambahkan ke favorit"
                    )

                else:

                    st.info(
                        "Resep sudah ada di favorit"
                    )