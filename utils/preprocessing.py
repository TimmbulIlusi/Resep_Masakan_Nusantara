import re


def clean_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    # =========================
    # NORMALISASI PHRASE
    # =========================

    phrase_mapping = {

        "bawang putih": "bawang_putih",
        "bawang merah": "bawang_merah",
        "gula merah": "gula_merah",
        "daging sapi": "daging_sapi",
        "daging ayam": "daging_ayam",
        "tepung roti": "tepung_roti",
        "tepung panir": "tepung_panir",
        "merica bubuk": "merica_bubuk",
        "cabai merah": "cabai_merah",
        "cabai rawit": "cabai_rawit",
        "susu cair": "susu_cair",
        "kecap manis": "kecap_manis"

    }

    for phrase, replacement in phrase_mapping.items():

        text = text.replace(
            phrase,
            replacement
        )

    # =========================
    # HAPUS ANGKA
    # =========================

    text = re.sub(r"\d+", " ", text)

    # =========================
    # HAPUS SIMBOL
    # =========================

    text = re.sub(
        r"[^a-zA-Z_\s]",
        " ",
        text
    )

    # =========================
    # HAPUS KATA TIDAK PENTING
    # =========================

    useless_words = {

        "gram",
        "kg",
        "ml",
        "liter",
        "sdm",
        "sdt",

        "buah",
        "lembar",
        "siung",
        "butir",
        "batang",
        "bungkus",

        "secukupnya",
        "sesuai",
        "selera",

        "iris",
        "halus",
        "ulek",
        "potong",
        "cincang",
        "giling",

        "dan",
        "atau"

    }

    words = text.split()

    filtered_words = []

    for word in words:

        word = word.strip()

        if (
            word
            and word not in useless_words
            and len(word) > 2
        ):

            filtered_words.append(word)

    # =========================
    # HAPUS DUPLIKAT
    # =========================

    filtered_words = list(
        dict.fromkeys(filtered_words)
    )

    # =========================
    # KEMBALIKAN PHRASE
    # =========================

    final_words = []

    for word in filtered_words:

        final_words.append(
            word.replace("_", " ")
        )

    return ", ".join(final_words)