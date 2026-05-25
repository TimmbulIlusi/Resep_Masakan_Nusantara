import pandas as pd


def load_data():

    df = pd.read_csv(
        "data/Indonesian_Food_Recipes.csv"
    )

    df["Title"] = df["Title"].fillna("")
    df["Ingredients"] = df["Ingredients"].fillna("")
    df["Steps"] = df["Steps"].fillna("")
    df["Category"] = df["Category"].fillna("Lainnya")

    df["cleaned_title"] = (
        df["Title"]
        .astype(str)
        .str.lower()
    )

    df["cleaned_ingredients"] = (
        df["Ingredients"]
        .astype(str)
        .str.lower()
    )

    return df