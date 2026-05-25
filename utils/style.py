import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #f4f6f9;
        }

        h1 {
            color: #243b55;
            font-weight: 700;
        }

        h2, h3 {
            color: #2f4f6f;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {

            background-color: white;

            padding: 20px;

            border-radius: 14px;

            border: 1px solid #d6dce5;

            box-shadow:
                0 2px 6px rgba(0,0,0,0.04);

            margin-bottom: 18px;
        }

        .stButton > button {

            background-color: #2f4f6f;

            color: white;

            border-radius: 8px;

            border: none;

            padding: 10px 16px;

            font-weight: 600;
        }

        .stButton > button:hover {

            background-color: #243b55;

            color: white;
        }

        /* =========================
           SEARCH BAR
        ========================= */

        .stTextInput input {

            background-color: white !important;

            color: #1f2937 !important;

            border-radius: 10px;

            border: 2px solid #9fb3c8 !important;

            padding: 12px;

            font-size: 15px;
        }

        .stTextInput input:focus {

            border: 2px solid #2f4f6f !important;

            box-shadow: none !important;
        }

        /* =========================
           SELECTBOX
        ========================= */

        .stSelectbox div[data-baseweb="select"] {

            border-radius: 8px;

            border: 1px solid #c9d1d9;
        }

        /* =========================
           EXPANDER
        ========================= */

        .streamlit-expanderHeader {

            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )