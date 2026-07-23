from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "student_mental_health_model.pkl"
HISTORY_PATH = BASE_DIR / "records" / "prediction_history.csv"


GENDERS = [
    "female",
    "male",
]

COURSES = [
    "accounting",
    "ala",
    "banking studies",
    "biomedical science",
    "biotechnology",
    "business administration",
    "communication",
    "computer science",
    "cts",
    "diploma nursing",
    "diploma tesl",
    "economics and management",
    "econs",
    "engin",
    "engineering",
    "english",
    "enm",
    "fiqh",
    "fiqh fatwa",
    "human resources",
    "human sciences",
    "information technology",
    "islamic education",
    "kop",
    "law",
    "malcom",
    "marine science",
    "mathematics",
    "mhsc",
    "nursing",
    "psychology",
    "radiography",
    "taasl",
    "usuluddin",
]

STUDY_YEARS = [
    "year 1",
    "year 2",
    "year 3",
    "year 4",
]

CGPA_RANGES = [
    "0 - 1.99",
    "2.00 - 2.49",
    "2.50 - 2.99",
    "3.00 - 3.49",
    "3.50 - 4.00",
]

MARITAL_OPTIONS = [
    "no",
    "yes",
]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def get_numbered_choice(prompt, options):
    print(f"\n{prompt}")

    for number, option in enumerate(options, start=1):
        print(f"{number}. {option.title()}")

    while True:
        try:
            selected_number = int(
                input("Enter option number: ").strip()
            )

            if 1 <= selected_number <= len(options):
                return options[selected_number - 1]

            print(
                f"Please enter a number between "
                f"1 and {len(options)}."
            )

        except ValueError:
            print("Please enter a valid whole number.")


def get_age():
    while True:
        try:
            age = int(input("\nAge: ").strip())

            if 15 <= age <= 60:
                return age

            print("Please enter an age between 15 and 60.")

        except ValueError:
            print("Please enter a valid age.")


def save_prediction(
    student_data,
    prediction_label,
    no_risk_probability,
    risk_probability,
):
    record = {
        **student_data,
        "prediction": prediction_label,
        "no_risk_probability": round(
            no_risk_probability,
            2,
        ),
        "risk_probability": round(
            risk_probability,
            2,
        ),
    }

    record_dataframe = pd.DataFrame([record])

    HISTORY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if HISTORY_PATH.exists():
        record_dataframe.to_csv(
            HISTORY_PATH,
            mode="a",
            header=False,
            index=False,
        )
    else:
        record_dataframe.to_csv(
            HISTORY_PATH,
            index=False,
        )


def display_recommendations(risk_probability):
    print("\nRECOMMENDATIONS")
    print("-" * 60)

    if risk_probability < 40:
        print("1. Continue maintaining a balanced routine.")
        print("2. Take short breaks during study sessions.")
        print("3. Maintain proper sleep and meal timings.")

    elif risk_probability < 70:
        print("1. Monitor your stress and emotional wellbeing.")
        print("2. Speak with a trusted friend, mentor or family member.")
        print("3. Use a realistic study timetable.")
        print("4. Maintain regular sleep and physical activity.")

    else:
        print("1. Consider speaking with a qualified counsellor.")
        print("2. Avoid handling persistent distress alone.")
        print("3. Break difficult tasks into smaller activities.")
        print("4. Seek immediate help if you feel unsafe.")


def main():
    print("=" * 60)
    print("STUDENT MENTAL HEALTH ASSESSMENT AGENT")
    print("=" * 60)

    try:
        model = load_model()

    except Exception as error:
        print("\nModel could not be loaded.")
        print(f"Reason: {error}")
        return

    gender = get_numbered_choice(
        "Select Gender",
        GENDERS,
    )

    age = get_age()

    course = get_numbered_choice(
        "Select Course",
        COURSES,
    )

    study_year = get_numbered_choice(
        "Select Study Year",
        STUDY_YEARS,
    )

    cgpa = get_numbered_choice(
        "Select CGPA Range",
        CGPA_RANGES,
    )

    marital_status = get_numbered_choice(
        "Marital Status",
        MARITAL_OPTIONS,
    )

    student_data = {
        "age": age,
        "gender": gender,
        "course": course,
        "study_year": study_year,
        "cgpa": cgpa,
        "marital_status": marital_status,
    }

    input_dataframe = pd.DataFrame([student_data])

    try:
        prediction = int(
            model.predict(input_dataframe)[0]
        )

        probabilities = model.predict_proba(
            input_dataframe
        )[0]

        class_names = list(model.classes_)

        no_risk_index = class_names.index(0)
        risk_index = class_names.index(1)

        no_risk_probability = (
            probabilities[no_risk_index] * 100
        )

        risk_probability = (
            probabilities[risk_index] * 100
        )

    except Exception as error:
        print("\nPrediction could not be completed.")
        print(f"Reason: {error}")
        return

    if prediction == 1:
        prediction_label = (
            "HIGH RISK OF MENTAL HEALTH CONCERN"
        )
    else:
        prediction_label = (
            "LOW RISK OF MENTAL HEALTH CONCERN"
        )

    print("\nPrediction Completed!")

    print("\nSTUDENT DETAILS")
    print("-" * 60)
    print(f"Gender        : {gender.title()}")
    print(f"Age           : {age}")
    print(f"Course        : {course.title()}")
    print(f"Study Year    : {study_year.title()}")
    print(f"CGPA Range    : {cgpa}")
    print(
        "Marital Status: "
        + ("Married" if marital_status == "yes" else "Not Married")
    )

    print("\nPROBABILITY")
    print("-" * 60)
    print(
        f"No Risk : {no_risk_probability:.2f}%"
    )
    print(
        f"Risk    : {risk_probability:.2f}%"
    )

    print("\n" + "=" * 60)
    print(f"Prediction : {prediction_label}")
    print("=" * 60)

    display_recommendations(
        risk_probability
    )

    save_prediction(
        student_data,
        prediction_label,
        no_risk_probability,
        risk_probability,
    )

    print(
        "\nPrediction saved to "
        "records/prediction_history.csv"
    )

    print("\nDISCLAIMER")
    print("-" * 60)
    print(
        "This result is for educational screening only. "
        "It is not a medical diagnosis."
    )


if __name__ == "__main__":
    main()