import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>

        /* Main content area */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Main page headings */
        h1 {
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(128, 128, 128, 0.35);
            margin-bottom: 25px;
        }

        /* Section headings */
        h2, h3 {
            margin-top: 18px;
            margin-bottom: 14px;
        }

        /* Form border */
        div[data-testid="stForm"] {
            border: 1px solid rgba(128, 128, 128, 0.40);
            border-radius: 14px;
            padding: 25px;
            margin-top: 15px;
            margin-bottom: 25px;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 12px;
            padding: 15px;
            min-height: 110px;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 12px;
            overflow: hidden;
        }

        /* Charts */
        div[data-testid="stVegaLiteChart"],
        div[data-testid="stArrowVegaLiteChart"] {
            border: 1px solid rgba(128, 128, 128, 0.30);
            border-radius: 12px;
            padding: 12px;
        }

        /* Expanders */
        details {
            border: 1px solid rgba(128, 128, 128, 0.35) !important;
            border-radius: 10px !important;
            margin-bottom: 10px;
        }

        /* Input fields */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-radius: 8px;
        }

        /* Horizontal separator */
        hr {
            border: none;
            border-top: 1px solid rgba(128, 128, 128, 0.35);
            margin-top: 28px;
            margin-bottom: 28px;
        }

        /* Buttons */
        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 9px;
            border: 1px solid rgba(128, 128, 128, 0.45);
        }

        /* Sidebar separator */
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.25);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def section_start():
    st.markdown(
        """
        <div style="
            border: 1px solid rgba(128,128,128,0.35);
            border-radius: 14px;
            padding: 8px 20px 18px 20px;
            margin: 18px 0;
        ">
        """,
        unsafe_allow_html=True,
    )


def section_end():
    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )