import pandas as pd
import os


RATING_FILE = "ratings.csv"


# =========================
# BUAT FILE JIKA BELUM ADA
# =========================

def initialize_rating_file():

    if not os.path.exists(RATING_FILE):

        df = pd.DataFrame(
            columns=[
                "username",
                "recipe",
                "rating"
            ]
        )

        df.to_csv(
            RATING_FILE,
            index=False
        )


# =========================
# SIMPAN RATING
# =========================

def save_rating(
    username,
    recipe,
    rating
):

    initialize_rating_file()

    df = pd.read_csv(
        RATING_FILE
    )


    new_data = pd.DataFrame([{

        "username": username,

        "recipe": recipe,

        "rating": rating

    }])


    df = pd.concat(
        [df, new_data],
        ignore_index=True
    )


    df.to_csv(
        RATING_FILE,
        index=False
    )


# =========================
# LOAD RATING
# =========================

def load_ratings():

    initialize_rating_file()

    return pd.read_csv(
        RATING_FILE
    )


# =========================
# HITUNG RATING TERBAIK
# =========================

def get_top_rated_recipes():

    df = load_ratings()

    if df.empty:

        return pd.DataFrame()


    result = (

        df.groupby("recipe")["rating"]

        .mean()

        .reset_index()

        .sort_values(
            by="rating",
            ascending=False
        )

    )

    return result