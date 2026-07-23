from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Assessment Result",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

HISTORY_PATH = (
    PROJECT_DIR
    / "records"
    / "prediction_history.csv"
)


# ============================================================
# 3. BASIC HELPERS
# ============================================================

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_bool(value):
    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def load_history():
    if not HISTORY_PATH.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(HISTORY_PATH)

    except Exception:
        return pd.DataFrame()


def save_history(history_df):
    history_df.to_csv(
        HISTORY_PATH,
        index=False,
    )


def load_latest_assessment():

    if "latest_assessment" in st.session_state:

        latest = st.session_state[
            "latest_assessment"
        ]

        if isinstance(
            latest,
            pd.Series,
        ):
            return latest.to_dict()

        if isinstance(
            latest,
            dict,
        ):
            return latest

    history = load_history()

    if not history.empty:
        return history.iloc[-1].to_dict()

    return None


# ============================================================
# 4. RECOMMENDATIONS
# ============================================================

def generate_recommendations(data):

    recommendations = []

    risk_level = str(
        data.get(
            "risk_level",
            "",
        )
    ).strip()

    sleep_hours = safe_float(
        data.get(
            "sleep_hours",
            0,
        )
    )

    stress_level = safe_int(
        data.get(
            "stress_level",
            0,
        )
    )

    social_support = safe_int(
        data.get(
            "social_support",
            0,
        )
    )

    physical_activity = safe_int(
        data.get(
            "physical_activity",
            0,
        )
    )

    screen_time = safe_float(
        data.get(
            "screen_time",
            0,
        )
    )

    anxiety = to_bool(
        data.get(
            "anxiety_concern",
            False,
        )
    )

    depression = to_bool(
        data.get(
            "depression_concern",
            False,
        )
    )

    sleep_difficulty = to_bool(
        data.get(
            "sleep_difficulty",
            False,
        )
    )

    mood = str(
        data.get(
            "mood",
            "",
        )
    ).strip()


    if risk_level == "Low Risk":

        recommendations.append(
            "Continue maintaining your current healthy routine."
        )

    elif risk_level == "Moderate Risk":

        recommendations.append(
            "Monitor your emotional wellbeing and talk with someone you trust."
        )

    elif risk_level == "High Risk":

        recommendations.append(
            "Consider speaking with a counsellor or qualified mental-health professional."
        )


    if stress_level >= 7:

        recommendations.append(
            "Use daily stress-management activities such as breathing exercises, walking, meditation or journaling."
        )


    if sleep_hours < 7:

        recommendations.append(
            "Aim for approximately 7–9 hours of sleep and maintain a consistent sleep schedule."
        )


    if social_support <= 4:

        recommendations.append(
            "Spend more time with supportive friends, family members, mentors or classmates."
        )


    if physical_activity <= 3:

        recommendations.append(
            "Add gentle physical activity such as walking or stretching to your routine."
        )


    if screen_time > 8:

        recommendations.append(
            "Reduce unnecessary screen time, especially before sleeping."
        )


    if anxiety:

        recommendations.append(
            "Discuss continuing anxiety with a trusted person, mentor or counsellor."
        )


    if depression:

        recommendations.append(
            "Persistent sadness or loss of interest should be discussed with a qualified professional."
        )


    if sleep_difficulty:

        recommendations.append(
            "Follow a consistent sleeping schedule and reduce late-night screen use."
        )


    if mood.lower() in {
        "sad",
        "overwhelmed",
        "exhausted",
    }:

        recommendations.append(
            "Slow down where possible and focus on one manageable task at a time."
        )


    if not recommendations:

        recommendations.append(
            "Continue maintaining balanced sleep, study, activity and social-support routines."
        )

    return recommendations


# ============================================================
# 5. 7-DAY WELLNESS PLAN
# ============================================================

def generate_week_plan(data):

    stress_level = safe_int(
        data.get(
            "stress_level",
            5,
        )
    )

    sleep_hours = safe_float(
        data.get(
            "sleep_hours",
            7,
        )
    )

    stress_goal = (
        "Practice 10 minutes of breathing or relaxation."
        if stress_level >= 6
        else
        "Take one mindful study break."
    )

    sleep_goal = (
        "Aim for at least 7 hours of sleep."
        if sleep_hours < 7
        else
        "Maintain your current healthy sleep routine."
    )

    return {

        "Monday":
            f"{stress_goal} Choose only three important priorities.",

        "Tuesday":
            "Take a 20-minute walk and reduce unnecessary screen time.",

        "Wednesday":
            "Talk with a supportive friend, mentor or family member.",

        "Thursday":
            f"{sleep_goal} Avoid screens for at least 30 minutes before bed.",

        "Friday":
            "Spend time doing one enjoyable activity without academic pressure.",

        "Saturday":
            "Review your stress level and simplify one stressful task.",

        "Sunday":
            "Prepare gently for the next week and schedule enough rest.",
    }


# ============================================================
# 6. LOAD DATA
# ============================================================

result = load_latest_assessment()

history = load_history()


# ============================================================
# 7. HEADER
# ============================================================

st.title(
    "📊 Mental Health Assessment Result"
)

st.caption(
    "Your latest machine-learning prediction, current wellness status, recommendations and saved assessment history."
)


# ============================================================
# 8. NO RESULT
# ============================================================

if result is None:

    with st.container(
        border=True
    ):

        st.warning(
            "No assessment result is available yet."
        )

        st.write(
            "Complete an assessment first."
        )

        st.page_link(
            "pages/1_Assessment.py",
            label="Start Assessment",
            icon="📝",
        )

    st.stop()


# ============================================================
# 9. VALUES
# ============================================================

risk_probability = safe_float(
    result.get(
        "risk_probability",
        0,
    )
)

no_risk_probability = safe_float(
    result.get(
        "no_risk_probability",
        100 - risk_probability,
    )
)

risk_level = str(
    result.get(
        "risk_level",
        "Unknown",
    )
)

wellness_score = safe_int(
    result.get(
        "wellness_score",
        0,
    )
)

wellness_grade = str(
    result.get(
        "wellness_grade",
        "-",
    )
)

mental_battery = safe_int(
    result.get(
        "mental_battery",
        wellness_score,
    )
)


# ============================================================
# 10. STUDENT SUMMARY
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "👤 Student Summary"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.write(
            f"**Gender:** {result.get('gender', '-')}"
        )

        st.write(
            f"**Age:** {result.get('age', '-')}"
        )

    with col2:

        st.write(
            f"**Course:** {result.get('course', '-')}"
        )

        st.write(
            f"**Study Year:** {result.get('study_year', '-')}"
        )

    with col3:

        st.write(
            f"**CGPA:** {result.get('cgpa', '-')}"
        )

        st.write(
            f"**Marital Status:** {result.get('marital_status', '-')}"
        )


# ============================================================
# 11. ML RISK
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🤖 ML-Predicted Mental Health Concern"
    )

    st.caption(
        "This prediction is generated only from the six features used during Phase 1 training: "
        "Gender, Age, Course, Study Year, CGPA and Marital Status."
    )

    if risk_level.lower().startswith(
        "low"
    ):

        st.success(
            f"🟢 LOW MODEL-PREDICTED CONCERN — {risk_probability:.2f}%"
        )

    elif risk_level.lower().startswith(
        "moderate"
    ):

        st.warning(
            f"🟡 MODERATE MODEL-PREDICTED CONCERN — {risk_probability:.2f}%"
        )

    elif risk_level.lower().startswith(
        "high"
    ):

        st.error(
            f"🔴 HIGH MODEL-PREDICTED CONCERN — {risk_probability:.2f}%"
        )

    else:

        st.info(
            f"Concern Probability — {risk_probability:.2f}%"
        )


    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Concern Probability",
            f"{risk_probability:.2f}%",
        )

    with col2:

        st.metric(
            "No-Concern Probability",
            f"{no_risk_probability:.2f}%",
        )

    with col3:

        st.metric(
            "Model Category",
            risk_level,
        )

    st.progress(
        max(
            0.0,
            min(
                1.0,
                risk_probability / 100,
            ),
        )
    )


# ============================================================
# 12. CURRENT WELLNESS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🌱 Current Wellness Assessment"
    )

    st.caption(
        "This score is calculated separately using your current lifestyle and self-reported wellness inputs such as sleep, stress, activity, support, screen time and mood."
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Wellness Score",
            f"{wellness_score}/100",
        )

    with col2:

        st.metric(
            "Wellness Grade",
            wellness_grade,
        )

    with col3:

        st.metric(
            "Mental Battery",
            f"{mental_battery}%",
        )

    st.progress(
        max(
            0.0,
            min(
                1.0,
                mental_battery / 100,
            ),
        )
    )


# ============================================================
# 13. EXPLANATION
# ============================================================

with st.container(
    border=True
):

    st.info(
        """
        **Why can ML Risk and Wellness Score be different?**

        These two results measure different things.

        - **ML Concern Risk** uses only the six features used to train the machine-learning model.
        - **Current Wellness Score** uses your present lifestyle and self-reported wellbeing.

        This means a student may currently have healthy sleep, low stress and strong support,
        but the trained model may still estimate a higher statistical concern from its original training patterns.

        Neither result is a medical diagnosis.
        """
    )


# ============================================================
# 14. LIFESTYLE SNAPSHOT
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🌿 Lifestyle Snapshot"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Sleep",
            f"{result.get('sleep_hours', '-')} hrs",
        )

        st.metric(
            "Study Hours",
            f"{result.get('study_hours', '-')} hrs",
        )

    with col2:

        st.metric(
            "Stress",
            f"{result.get('stress_level', '-')}/10",
        )

        st.metric(
            "Social Support",
            f"{result.get('social_support', '-')}/10",
        )

    with col3:

        st.metric(
            "Physical Activity",
            f"{result.get('physical_activity', '-')}/10",
        )

        st.metric(
            "Screen Time",
            f"{result.get('screen_time', '-')} hrs",
        )


# ============================================================
# 15. MOOD
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🙂 Current Mood"
    )

    st.info(
        f"Current reported mood: **{result.get('mood', '-')}**"
    )


# ============================================================
# 16. URGENT SUPPORT
# ============================================================

urgent_support = to_bool(
    result.get(
        "urgent_support_flag",
        False,
    )
)

if urgent_support:

    with st.container(
        border=True
    ):

        st.error(
            """
            🚨 **Immediate human support is recommended.**

            Please reach out to a trusted person, counsellor,
            qualified mental-health professional, or local emergency service
            if you feel unsafe or are in immediate danger.

            This application cannot provide emergency or crisis care.
            """
        )


# ============================================================
# 17. RECOMMENDATIONS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "💡 Personalized Recommendations"
    )

    recommendations = generate_recommendations(
        result
    )

    for number, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        st.write(
            f"**{number}.** {recommendation}"
        )


# ============================================================
# 18. 7-DAY PLAN
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "📅 7-Day Wellness Plan"
    )

    week_plan = generate_week_plan(
        result
    )

    for day, activity in week_plan.items():

        with st.expander(
            day
        ):

            st.write(
                activity
            )


# ============================================================
# 19. PREVIOUS VS CURRENT
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🔄 Previous vs Current"
    )

    if len(history) < 2:

        st.info(
            "Complete at least two assessments to compare progress."
        )

    else:

        latest = history.iloc[-1]
        previous = history.iloc[-2]

        latest_risk = safe_float(
            latest.get(
                "risk_probability",
                0,
            )
        )

        previous_risk = safe_float(
            previous.get(
                "risk_probability",
                0,
            )
        )

        latest_wellness = safe_float(
            latest.get(
                "wellness_score",
                0,
            )
        )

        previous_wellness = safe_float(
            previous.get(
                "wellness_score",
                0,
            )
        )

        risk_change = (
            latest_risk
            - previous_risk
        )

        wellness_change = (
            latest_wellness
            - previous_wellness
        )

        col1, col2 = st.columns(
            2
        )

        with col1:

            st.metric(
                "Current ML Concern Risk",
                f"{latest_risk:.1f}%",
                delta=f"{risk_change:+.1f}%",
                delta_color="inverse",
            )

        with col2:

            st.metric(
                "Current Wellness",
                f"{latest_wellness:.1f}/100",
                delta=f"{wellness_change:+.1f}",
            )


# ============================================================
# 20. ASSESSMENT HISTORY
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🕒 Assessment History"
    )

    if history.empty:

        st.info(
            "No previous assessment history is available."
        )

    else:

        display_columns = [
            column
            for column in [
                "timestamp",
                "course",
                "study_year",
                "risk_probability",
                "risk_level",
                "wellness_score",
                "wellness_grade",
                "mood",
            ]
            if column in history.columns
        ]


        # ----------------------------------------------------
        # RECENT ASSESSMENTS
        # ----------------------------------------------------

        st.markdown(
            "#### Recent Assessments"
        )

        recent_history = (
            history[
                display_columns
            ]
            .tail(5)
            .iloc[::-1]
        )

        st.dataframe(
            recent_history,
            width="stretch",
            hide_index=True,
        )


        # ----------------------------------------------------
        # COMPLETE HISTORY
        # ----------------------------------------------------

        with st.expander(
            "📜 View Complete History",
            expanded=False,
        ):

            st.write(
                f"**Total Assessments:** {len(history)}"
            )

            st.dataframe(
                history[
                    display_columns
                ].iloc[::-1],
                width="stretch",
                hide_index=True,
            )


        # ----------------------------------------------------
        # DELETE ONE RECORD
        # ----------------------------------------------------

        st.markdown(
            "#### 🗑️ Delete an Assessment"
        )

        delete_options = []

        for index, row in history.iterrows():

            timestamp = row.get(
                "timestamp",
                f"Assessment {index + 1}",
            )

            risk = row.get(
                "risk_probability",
                "-",
            )

            wellness = row.get(
                "wellness_score",
                "-",
            )

            label = (
                f"{timestamp} | "
                f"Risk: {risk}% | "
                f"Wellness: {wellness}/100"
            )

            delete_options.append(
                (
                    index,
                    label,
                )
            )


        selected_label = st.selectbox(
            "Select the assessment you want to delete",
            options=[
                label
                for _, label
                in delete_options
            ],
        )


        selected_index = next(
            index
            for index, label
            in delete_options
            if label == selected_label
        )


        confirm_delete = st.checkbox(
            "I confirm that I want to delete this assessment."
        )


        if st.button(
            "🗑️ Delete Selected Assessment",
            width="stretch",
        ):

            if not confirm_delete:

                st.warning(
                    "Please confirm deletion first."
                )

            else:

                updated_history = history.drop(
                    index=selected_index
                ).reset_index(
                    drop=True
                )

                save_history(
                    updated_history
                )

                st.session_state.pop(
                    "latest_assessment",
                    None,
                )

                st.success(
                    "Selected assessment deleted successfully."
                )

                st.rerun()


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        st.markdown(
            "#### ⬇️ Download History"
        )

        csv_data = history.to_csv(
            index=False
        )

        st.download_button(
            label="Download Complete History",
            data=csv_data,
            file_name="mindcare_assessment_history.csv",
            mime="text/csv",
            width="stretch",
        )


        # ----------------------------------------------------
        # DELETE ALL
        # ----------------------------------------------------

        with st.expander(
            "⚠️ Delete All Assessment History"
        ):

            st.warning(
                "This will permanently remove all saved assessment records."
            )

            confirm_all = st.checkbox(
                "I understand that all assessment history will be deleted.",
                key="delete_all_confirmation",
            )

            if st.button(
                "🗑️ Clear Complete History",
                width="stretch",
            ):

                if not confirm_all:

                    st.warning(
                        "Please confirm before deleting all history."
                    )

                else:

                    empty_history = history.iloc[
                        0:0
                    ]

                    save_history(
                        empty_history
                    )

                    st.session_state.pop(
                        "latest_assessment",
                        None,
                    )

                    st.success(
                        "Complete assessment history deleted."
                    )

                    st.rerun()


# ============================================================
# 21. NAVIGATION
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🧭 What's Next?"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.page_link(
            "pages/1_Assessment.py",
            label="New Assessment",
            icon="📝",
        )

    with col2:

        st.page_link(
            "pages/3_Analytics.py",
            label="View Analytics",
            icon="📈",
        )

    with col3:
        st.page_link(
            "pages/5_Support_Guide.py",
            label="Support Guide",
            icon="🆘",
        )


# ============================================================
# 22. DISCLAIMER
# ============================================================

with st.container(
    border=True
):

    st.warning(
        """
        This assessment is intended only for educational screening
        and wellness awareness.

        It is not a diagnosis of depression, anxiety or any other
        medical or psychological condition.

        Seek guidance from a qualified mental-health professional
        when symptoms are serious, persistent or interfere with daily life.
        """
    )


# ============================================================
# 23. FOOTER
# ============================================================

st.caption(
    "🧠 MindCare AI • Assess • Understand • Improve"
)