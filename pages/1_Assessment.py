from __future__ import annotations

from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from utils.styles import apply_global_styles


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Assessment",
    page_icon="📝",
    layout="wide",
)

apply_global_styles()


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_DIR
    / "models"
    / "student_mental_health_model.pkl"
)

RECORDS_DIR = PROJECT_DIR / "records"

HISTORY_PATH = (
    RECORDS_DIR
    / "prediction_history.csv"
)

RECORDS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# 3. OPTIONS
# ============================================================

GENDER_OPTIONS = [
    "Female",
    "Male",
]

COURSE_OPTIONS = [
    "Accounting",
    "Ala",
    "Banking Studies",
    "Biomedical Science",
    "Biotechnology",
    "Business Administration",
    "Communication",
    "Computer Science",
    "Cts",
    "Diploma Nursing",
    "Diploma Tesl",
    "Economics And Management",
    "Econs",
    "Engin",
    "Engineering",
    "English",
    "Enm",
    "Fiqh",
    "Fiqh Fatwa",
    "Human Resources",
    "Human Sciences",
    "Information Technology",
    "Islamic Education",
    "Kop",
    "Law",
    "Malcom",
    "Marine Science",
    "Mathematics",
    "Mhsc",
    "Nursing",
    "Psychology",
    "Radiography",
    "Taasl",
    "Usuluddin",
]

STUDY_YEAR_OPTIONS = [
    "Year 1",
    "Year 2",
    "Year 3",
    "Year 4",
]

MARITAL_STATUS_OPTIONS = [
    "Not Married",
    "Married",
]

MOOD_OPTIONS = [
    "Happy",
    "Fine",
    "Neutral",
    "Anxious",
    "Sad",
    "Overwhelmed",
    "Exhausted",
]


# ============================================================
# 4. LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    return joblib.load(
        MODEL_PATH
    )


try:

    model = load_model()

except Exception as error:

    st.error(
        "The trained model could not be loaded."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# 5. CGPA CONVERSION
# ============================================================

def convert_cgpa_to_model_band(
    cgpa_10_point: float,
) -> str:
    """
    Convert a user-friendly 10-point CGPA value into the
    categorical 4-point-style range expected by the trained model.

    This is an approximate normalization for model compatibility,
    not an official university CGPA conversion.
    """

    if cgpa_10_point < 5.0:
        return "0 - 1.99"

    if cgpa_10_point < 6.25:
        return "2.00 - 2.49"

    if cgpa_10_point < 7.50:
        return "2.50 - 2.99"

    if cgpa_10_point < 8.75:
        return "3.00 - 3.49"

    return "3.50 - 4.00"


# ============================================================
# 6. PREPARE MODEL INPUT
# ============================================================

def prepare_model_input(
    gender,
    age,
    course,
    study_year,
    model_cgpa,
    marital_status,
):

    model_marital_status = (
        "Yes"
        if marital_status == "Married"
        else "No"
    )

    return pd.DataFrame(
        [
            {
                "gender": gender,
                "age": int(age),
                "course": course,
                "study_year": study_year,
                "cgpa": model_cgpa,
                "marital_status": model_marital_status,
            }
        ],
        columns=[
            "gender",
            "age",
            "course",
            "study_year",
            "cgpa",
            "marital_status",
        ],
    )


# ============================================================
# 7. MODEL PREDICTION
# ============================================================

def predict_risk(
    input_df,
):

    prediction = int(
        model.predict(
            input_df
        )[0]
    )

    if hasattr(
        model,
        "predict_proba",
    ):

        probabilities = (
            model.predict_proba(
                input_df
            )[0]
        )

        no_risk_probability = (
            float(
                probabilities[0]
            )
            * 100
        )

        risk_probability = (
            float(
                probabilities[1]
            )
            * 100
        )

    else:

        risk_probability = (
            100.0
            if prediction == 1
            else 0.0
        )

        no_risk_probability = (
            100.0
            - risk_probability
        )

    return (
        prediction,
        risk_probability,
        no_risk_probability,
    )


# ============================================================
# 8. RISK CATEGORY
# ============================================================

def get_risk_category(
    risk_probability,
):

    if risk_probability < 40:
        return "Low Risk"

    if risk_probability < 70:
        return "Moderate Risk"

    return "High Risk"


# ============================================================
# 9. WELLNESS SCORE
# ============================================================

def calculate_wellness_score(
    sleep_hours,
    stress_level,
    physical_activity,
    study_hours,
    social_support,
    screen_time,
    anxiety,
    depression,
    sleep_difficulty,
    mood,
):

    score = 100


    # Sleep
    if sleep_hours < 5:

        score -= 20

    elif sleep_hours < 7:

        score -= 10

    elif sleep_hours > 10:

        score -= 5


    # Stress
    score -= max(
        0,
        stress_level - 3,
    ) * 4


    # Physical activity
    if physical_activity <= 2:

        score -= 15

    elif physical_activity <= 4:

        score -= 8


    # Study load
    if study_hours > 10:

        score -= 12

    elif study_hours > 8:

        score -= 7


    # Social support
    if social_support <= 2:

        score -= 15

    elif social_support <= 4:

        score -= 8


    # Screen time
    if screen_time > 10:

        score -= 12

    elif screen_time > 7:

        score -= 6


    # Reported concerns
    if anxiety:

        score -= 8

    if depression:

        score -= 12

    if sleep_difficulty:

        score -= 8


    # Mood
    mood_penalties = {

        "Happy": 0,

        "Fine": 2,

        "Neutral": 4,

        "Anxious": 8,

        "Sad": 10,

        "Overwhelmed": 12,

        "Exhausted": 10,
    }

    score -= mood_penalties.get(
        mood,
        0,
    )


    return max(
        0,
        min(
            100,
            int(
                round(
                    score
                )
            ),
        ),
    )


# ============================================================
# 10. WELLNESS GRADE
# ============================================================

def get_wellness_grade(
    score,
):

    if score >= 80:
        return "Excellent"

    if score >= 65:
        return "Good"

    if score >= 50:
        return "Needs Attention"

    return "Needs Support"


# ============================================================
# 11. MENTAL BATTERY
# ============================================================

def get_mental_battery(
    wellness_score,
    stress_level,
):

    value = (
        wellness_score
        + (
            10
            - stress_level
        )
        * 2
    )

    return max(
        0,
        min(
            100,
            int(
                round(
                    value
                )
            ),
        ),
    )


# ============================================================
# 12. SAVE ASSESSMENT
# ============================================================

def save_assessment(
    record,
):

    columns = [
        "timestamp",
        "gender",
        "age",
        "course",
        "study_year",
        "cgpa",
        "marital_status",
        "sleep_hours",
        "study_hours",
        "stress_level",
        "social_support",
        "physical_activity",
        "screen_time",
        "anxiety_concern",
        "depression_concern",
        "sleep_difficulty",
        "mood",
        "prediction",
        "risk_probability",
        "no_risk_probability",
        "risk_level",
        "wellness_score",
        "wellness_grade",
        "mental_battery",
        "urgent_support_flag",
    ]

    new_row = pd.DataFrame(
        [record]
    ).reindex(
        columns=columns
    )

    if HISTORY_PATH.exists():

        try:

            existing = pd.read_csv(
                HISTORY_PATH
            ).reindex(
                columns=columns
            )

            combined = pd.concat(
                [
                    existing,
                    new_row,
                ],
                ignore_index=True,
            )

            combined.to_csv(
                HISTORY_PATH,
                index=False,
            )

        except Exception:

            backup_path = (
                RECORDS_DIR
                / (
                    "prediction_history_backup_"
                    + datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )
                    + ".csv"
                )
            )

            HISTORY_PATH.replace(
                backup_path
            )

            new_row.to_csv(
                HISTORY_PATH,
                index=False,
            )

    else:

        new_row.to_csv(
            HISTORY_PATH,
            index=False,
        )


# ============================================================
# 13. PAGE HEADER
# ============================================================

st.title(
    "📝 Student Mental Health Assessment"
)

st.caption(
    "Complete each section carefully to generate your mental-health "
    "risk prediction and current wellness assessment."
)


with st.container(
    border=True
):

    st.info(
        """
        **This assessment has two separate parts:**

        🤖 **ML Prediction** uses:
        Gender, Age, Course, Study Year, CGPA and Marital Status.

        🌱 **Wellness Assessment** uses:
        Sleep, Study Hours, Stress, Social Support, Physical Activity,
        Screen Time, Reported Concerns and Mood.

        CGPA can be entered normally on a **10-point scale**.
        The application automatically converts it internally into the
        category format required by the trained ML model.

        ML prediction and Wellness Score may be different because
        they measure different aspects.
        """
    )


# ============================================================
# 14. ASSESSMENT FORM
# ============================================================

with st.form(
    "assessment_form"
):


    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "👤 1. Student Profile"
        )

        st.caption(
            "These six profile details are used by the trained machine-learning model."
        )

        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            gender = st.selectbox(
                "Gender",
                GENDER_OPTIONS,
            )

            age = st.number_input(
                "Age",
                min_value=15,
                max_value=60,
                value=22,
                step=1,
            )


        with col2:

            course = st.selectbox(
                "Course",
                COURSE_OPTIONS,
                index=7,
            )

            study_year = st.selectbox(
                "Study Year",
                STUDY_YEAR_OPTIONS,
                index=2,
            )


        with col3:

            cgpa_10_point = st.number_input(
                "CGPA (out of 10)",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.1,
                format="%.2f",
                help=(
                    "Enter your current CGPA on a 10-point scale. "
                    "The app will automatically convert it internally "
                    "into the category format required by the trained model."
                ),
            )

            marital_status = st.selectbox(
                "Marital Status",
                MARITAL_STATUS_OPTIONS,
            )


        model_cgpa_preview = (
            convert_cgpa_to_model_band(
                cgpa_10_point
            )
        )

        st.caption(
            f"ℹ️ Your entered CGPA: **{cgpa_10_point:.2f}/10**. "
            "A compatible internal category will be used by the ML model."
        )


    # ========================================================
    # LIFESTYLE & WELLNESS
    # ========================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "🌱 2. Lifestyle & Wellness"
        )

        st.caption(
            "These values are used for the current Wellness Score, "
            "Mental Battery and personalized recommendations."
        )

        col4, col5, col6 = st.columns(
            3
        )


        with col4:

            sleep_hours = st.slider(
                "Average Sleep Hours per Day",
                min_value=2.0,
                max_value=12.0,
                value=7.0,
                step=0.5,
            )

            study_hours = st.slider(
                "Average Study Hours per Day",
                min_value=0.0,
                max_value=16.0,
                value=7.0,
                step=0.5,
            )


        with col5:

            stress_level = st.slider(
                "Stress Level",
                min_value=1,
                max_value=10,
                value=5,
            )

            social_support = st.slider(
                "Social Support Level",
                min_value=1,
                max_value=10,
                value=5,
            )


        with col6:

            physical_activity = st.slider(
                "Physical Activity Level",
                min_value=1,
                max_value=10,
                value=5,
            )

            screen_time = st.slider(
                "Daily Screen Time",
                min_value=0.0,
                max_value=16.0,
                value=6.0,
                step=0.5,
            )


    # ========================================================
    # EMOTIONAL WELLBEING
    # ========================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "🧠 3. Emotional Wellbeing"
        )

        st.caption(
            "Select only the concerns that currently apply to you."
        )

        concern1, concern2, concern3 = st.columns(
            3
        )


        with concern1:

            anxiety_concern = st.checkbox(
                "Anxiety-related concerns"
            )


        with concern2:

            depression_concern = st.checkbox(
                "Depression-related concerns"
            )


        with concern3:

            sleep_difficulty = st.checkbox(
                "Sleep difficulties"
            )


    # ========================================================
    # MOOD
    # ========================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "🙂 4. Current Mood"
        )

        st.caption(
            "Choose the option that best describes how you feel today."
        )

        mood = st.radio(
            "How are you feeling today?",
            MOOD_OPTIONS,
            horizontal=True,
        )


    # ========================================================
    # SUBMIT
    # ========================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "🔍 5. Generate Assessment"
        )

        st.caption(
            "Your result will be saved and displayed on the Result page."
        )

        submitted = st.form_submit_button(
            "Generate Assessment",
            width="stretch",
        )


# ============================================================
# 15. PROCESS ASSESSMENT
# ============================================================

if submitted:


    # --------------------------------------------------------
    # CONVERT USER CGPA FOR MODEL
    # --------------------------------------------------------

    model_cgpa = (
        convert_cgpa_to_model_band(
            cgpa_10_point
        )
    )


    # --------------------------------------------------------
    # PREPARE ML INPUT
    # --------------------------------------------------------

    input_df = prepare_model_input(
        gender,
        age,
        course,
        study_year,
        model_cgpa,
        marital_status,
    )


    # --------------------------------------------------------
    # PREDICT ML RISK
    # --------------------------------------------------------

    try:

        (
            prediction,
            risk_probability,
            no_risk_probability,
        ) = predict_risk(
            input_df
        )

    except Exception as error:

        st.error(
            "Prediction failed."
        )

        st.code(
            str(error)
        )

        st.stop()


    # --------------------------------------------------------
    # RISK CATEGORY
    # --------------------------------------------------------

    risk_level = get_risk_category(
        risk_probability
    )


    # --------------------------------------------------------
    # WELLNESS SCORE
    # --------------------------------------------------------

    wellness_score = calculate_wellness_score(
        sleep_hours,
        stress_level,
        physical_activity,
        study_hours,
        social_support,
        screen_time,
        anxiety_concern,
        depression_concern,
        sleep_difficulty,
        mood,
    )


    wellness_grade = get_wellness_grade(
        wellness_score
    )


    mental_battery = get_mental_battery(
        wellness_score,
        stress_level,
    )


    # --------------------------------------------------------
    # SAFETY FLAG
    # --------------------------------------------------------

    urgent_support_flag = bool(
        depression_concern
        and mood
        in {
            "Sad",
            "Overwhelmed",
            "Exhausted",
        }
    )


    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    record = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "gender":
            gender,

        "age":
            int(
                age
            ),

        "course":
            course,

        "study_year":
            study_year,

        # User-friendly value shown on Result page
        "cgpa":
            f"{cgpa_10_point:.2f} / 10",

        "marital_status":
            marital_status,

        "sleep_hours":
            float(
                sleep_hours
            ),

        "study_hours":
            float(
                study_hours
            ),

        "stress_level":
            int(
                stress_level
            ),

        "social_support":
            int(
                social_support
            ),

        "physical_activity":
            int(
                physical_activity
            ),

        "screen_time":
            float(
                screen_time
            ),

        "anxiety_concern":
            bool(
                anxiety_concern
            ),

        "depression_concern":
            bool(
                depression_concern
            ),

        "sleep_difficulty":
            bool(
                sleep_difficulty
            ),

        "mood":
            mood,

        "prediction":
            int(
                prediction
            ),

        "risk_probability":
            round(
                risk_probability,
                2,
            ),

        "no_risk_probability":
            round(
                no_risk_probability,
                2,
            ),

        "risk_level":
            risk_level,

        "wellness_score":
            wellness_score,

        "wellness_grade":
            wellness_grade,

        "mental_battery":
            mental_battery,

        "urgent_support_flag":
            urgent_support_flag,
    }


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    try:

        save_assessment(
            record
        )

    except Exception as error:

        st.error(
            "The assessment was generated but could not be saved."
        )

        st.code(
            str(error)
        )

        st.stop()


    # --------------------------------------------------------
    # SAVE LATEST RESULT
    # --------------------------------------------------------

    st.session_state[
        "latest_assessment"
    ] = record


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        st.success(
            "✅ Assessment generated and saved successfully."
        )

        st.write(
            f"Entered CGPA: **{cgpa_10_point:.2f}/10**"
        )

        st.write(
            "Open the **Result** page to view your complete "
            "ML prediction, wellness score, recommendations and history."
        )

        st.page_link(
            "pages/2_Result.py",
            label="Open Result Page",
            icon="📊",
        )


# ============================================================
# 16. FOOTER
# ============================================================

st.caption(
    "🧠 MindCare AI • Educational screening only • Not a medical diagnosis"
)