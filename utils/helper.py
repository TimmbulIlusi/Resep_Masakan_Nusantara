import pandas as pd
import re


# =========================
# LOAD DATA
# =========================

def load_data():

    df = pd.read_csv(
        "data/Indonesian_Food_Recipes.csv"
    )


    # CLEAN TITLE
    df["cleaned_title"] = df[
        "Title"
    ].astype(str).str.lower()


    return df


# =========================
# CLEAN INGREDIENTS
# =========================

def clean_ingredients(text):

    text = str(text).lower()


    # GANTI PEMISAH
    text = text.replace("--", ",")


    # HAPUS ANGKA
    text = re.sub(
        r"\d+",
        " ",
        text
    )


    # HAPUS SATUAN
    stopwords = [

        "gr",
        "gram",
        "kg",
        "ml",
        "liter",
        "sdm",
        "sdt",
        "butir",
        "siung",
        "buah",
        "lembar",
        "batang",
        "ruas",
        "cm"

    ]


    for word in stopwords:

        text = text.replace(
            word,
            " "
        )


    # HAPUS KARAKTER ANEH
    text = re.sub(
        r"[^a-zA-Z,\s]",
        " ",
        text
    )


    # RAPIIKAN SPASI
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    return text