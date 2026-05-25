import streamlit as st

from utils.helper import load_data
from utils.style import load_css


load_css()

st.title("Resep Favorit")


# =========================
# LOAD DATA
# =========================

df = load_data()


# =========================
# SESSION FAVORIT
# =========================

if "favorites" not in st.session_state:

    st.session_state["favorites"] = []


favorites = st.session_state[
    "favorites"
]


# =========================
# CEK KOSONG
# =========================

if len(favorites) == 0:

    st.markdown(
        """
        <div style="
            background-color:#e5e7eb;
            padding:30px;
            border-radius:18px;
            text-align:center;
            margin-top:30px;
            border:1px solid #cbd5e1;
        ">

        <h2 style="
            color:#374151;
            margin-bottom:10px;
        ">
            Belum Ada Resep Favorit
        </h2>

        <p style="
            color:#6b7280;
            font-size:15px;
        ">
            Tambahkan resep favorit dari halaman
            rekomendasi atau daftar resep.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div style="
            background-color:#dbe4ea;
            padding:18px;
            border-radius:14px;
            margin-top:10px;
            margin-bottom:25px;
            border:1px solid #c5d0d8;
        ">

        <h3 style="
            color:#1f2937;
            margin-bottom:8px;
        ">
            Koleksi Resep Favorit
        </h3>

        <div style="
            color:#4b5563;
            font-size:15px;
        ">
            Total resep tersimpan:
            <b>{len(favorites)}</b>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # GRID FAVORIT
    # =========================

    col1, col2 = st.columns(2)

    columns = [col1, col2]


    for i, recipe_name in enumerate(favorites):

        recipe_data = df[
            df["Title"] == recipe_name
        ]


        if not recipe_data.empty:

            recipe = recipe_data.iloc[0]

            title = str(
                recipe["Title"]
            )

            ingredients = str(
                recipe["Ingredients"]
            ).split("--")


            preview = []

            for item in ingredients[:4]:

                item = item.strip()

                if item:

                    preview.append(item)


            preview_text = " • ".join(preview)


            with columns[i % 2]:

                with st.container(border=True):

                    st.markdown(
                        f"""
                        <div style="
                            background:linear-gradient(
                                135deg,
                                #dbeafe,
                                #eef2ff
                            );
                            padding:20px;
                            border-radius:16px;
                            min-height:240px;
                        ">

                        <div style="
                            background-color:#bfdbfe;
                            color:#1e3a8a;
                            display:inline-block;
                            padding:6px 14px;
                            border-radius:999px;
                            font-size:13px;
                            font-weight:bold;
                            margin-bottom:14px;
                        ">
                            FAVORIT
                        </div>

                        <h3 style="
                            color:#111827;
                            margin-bottom:15px;
                        ">
                            {title}
                        </h3>

                        <div style="
                            background-color:rgba(
                                255,
                                255,
                                255,
                                0.6
                            );
                            padding:12px;
                            border-radius:12px;
                            color:#334155;
                            line-height:1.7;
                            font-size:14px;
                        ">

                        <b>Preview Bahan:</b>

                        <br><br>

                        {preview_text}

                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # =========================
                    # DETAIL
                    # =========================

                    with st.expander(
                        "Lihat Detail Resep"
                    ):

                        st.markdown(
                            "### Bahan Lengkap"
                        )

                        for ing in ingredients:

                            ing = ing.strip()

                            if ing:

                                st.write(
                                    f"• {ing}"
                                )


                        st.markdown(
                            "### Langkah Memasak"
                        )

                        steps = str(
                            recipe["Steps"]
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
                    # HAPUS FAVORIT
                    # =========================

                    if st.button(
                        "Hapus dari Favorit",
                        key=f"hapus_{i}"
                    ):

                        st.session_state[
                            "favorites"
                        ].remove(
                            recipe_name
                        )

                        st.toast(
                            "Resep dihapus dari favorit"
                        )

                        st.rerun()