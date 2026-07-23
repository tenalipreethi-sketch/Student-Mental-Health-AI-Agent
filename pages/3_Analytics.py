from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide",
)


PROJECT_DIR = Path(__file__).resolve().parent.parent

HISTORY_PATH = (
    PROJECT_DIR
    / "records"
    / "prediction_history.csv"
)


st.title(
    "📈 Wellness Analytics"
)

st.caption(
    "Explore patterns across saved student assessments."
)


if not HISTORY_PATH.exists():

    st.info(
        "No assessment records are available yet."
    )

    st.stop()


try:

    df = pd.read_csv(
        HISTORY_PATH
    )

except Exception as error:

    st.error(
        "Could not read assessment history."
    )

    st.code(
        str(error)
    )

    st.stop()


if df.empty:

    st.info(
        "No assessment records are available yet."
    )

    st.stop()


numeric_columns = [
    "risk_probability",
    "wellness_score",
    "stress_level",
    "sleep_hours",
    "study_hours",
    "social_support",
    "physical_activity",
    "screen_time",
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


# ============================================================
# SUMMARY
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "📊 Analytics Summary"
    )

    col1, col2, col3, col4 = st.columns(
        4
    )

    with col1:

        st.metric(
            "Total Assessments",
            len(df),
        )

    with col2:

        average_risk = (
            df[
                "risk_probability"
            ].mean()
            if "risk_probability"
            in df.columns
            else 0
        )

        st.metric(
            "Average Risk",
            f"{average_risk:.1f}%",
        )

    with col3:

        average_wellness = (
            df[
                "wellness_score"
            ].mean()
            if "wellness_score"
            in df.columns
            else 0
        )

        st.metric(
            "Average Wellness",
            f"{average_wellness:.1f}/100",
        )

    with col4:

        high_count = (
            df[
                "risk_level"
            ]
            .astype(str)
            .str.contains(
                "High",
                case=False,
                na=False,
            )
            .sum()
            if "risk_level"
            in df.columns
            else 0
        )

        st.metric(
            "High Risk Cases",
            int(
                high_count
            ),
        )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🎯 Risk Distribution"
    )

    if "risk_level" in df.columns:

        risk_distribution = (
            df[
                "risk_level"
            ]
            .value_counts()
            .rename_axis(
                "Risk Level"
            )
            .reset_index(
                name="Count"
            )
        )

        st.bar_chart(
            risk_distribution,
            x="Risk Level",
            y="Count",
            width="stretch",
        )

    else:

        st.info(
            "Risk data unavailable."
        )


# ============================================================
# WELLNESS TREND
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🌱 Wellness Trend"
    )

    if "wellness_score" in df.columns:

        trend = df[
            [
                "wellness_score"
            ]
        ].copy()

        trend.columns = [
            "Wellness Score"
        ]

        trend.index = range(
            1,
            len(
                trend
            )
            + 1,
        )

        st.line_chart(
            trend,
            width="stretch",
        )


# ============================================================
# RISK TREND
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "📉 Risk Probability Trend"
    )

    if "risk_probability" in df.columns:

        trend = df[
            [
                "risk_probability"
            ]
        ].copy()

        trend.columns = [
            "Risk Probability"
        ]

        trend.index = range(
            1,
            len(
                trend
            )
            + 1,
        )

        st.line_chart(
            trend,
            width="stretch",
        )


# ============================================================
# MOOD
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🙂 Mood Distribution"
    )

    if "mood" in df.columns:

        mood_distribution = (
            df[
                "mood"
            ]
            .value_counts()
            .rename_axis(
                "Mood"
            )
            .reset_index(
                name="Count"
            )
        )

        st.bar_chart(
            mood_distribution,
            x="Mood",
            y="Count",
            width="stretch",
        )


# ============================================================
# LIFESTYLE
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🌿 Lifestyle Overview"
    )

    lifestyle_columns = [
        "sleep_hours",
        "study_hours",
        "stress_level",
        "social_support",
        "physical_activity",
        "screen_time",
    ]

    available = [
        column
        for column
        in lifestyle_columns
        if column
        in df.columns
    ]

    if available:

        averages = (
            df[
                available
            ]
            .mean()
            .round(
                2
            )
            .rename_axis(
                "Factor"
            )
            .reset_index(
                name="Average"
            )
        )

        st.bar_chart(
            averages,
            x="Factor",
            y="Average",
            width="stretch",
        )


# ============================================================
# LATEST TABLE
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🕒 Latest Assessments"
    )

    columns = [
        column
        for column
        in [
            "timestamp",
            "course",
            "study_year",
            "risk_probability",
            "risk_level",
            "wellness_score",
            "mood",
        ]
        if column
        in df.columns
    ]

    st.dataframe(
        df[
            columns
        ]
        .tail(
            10
        )
        .iloc[
            ::-1
        ],
        width="stretch",
        hide_index=True,
    )


st.caption(
    "Analytics are based only on assessments saved in this application."
)