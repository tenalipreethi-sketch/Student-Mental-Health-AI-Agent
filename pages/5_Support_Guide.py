import streamlit as st


st.set_page_config(
    page_title="Support Guide",
    page_icon="🆘",
    layout="wide",
)


st.title(
    "🆘 Student Support Guide"
)

st.caption(
    "Practical educational guidance for supporting student mental wellbeing."
)


# ============================================================
# DAILY WELLNESS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🌱 Daily Wellness Basics"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        st.markdown(
            """
            ### 😴 Sleep

            - Aim for approximately 7–9 hours of sleep.
            - Try to sleep and wake at similar times.
            - Reduce late-night screen use.
            - Avoid heavy study sessions immediately before sleep.
            """
        )

    with col2:

        st.markdown(
            """
            ### 🏃 Physical Activity

            - Take short daily walks.
            - Stretch during study breaks.
            - Avoid sitting continuously for many hours.
            - Choose activities you actually enjoy.
            """
        )


# ============================================================
# STUDY STRESS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "📚 Managing Academic Stress"
    )

    st.write(
        """
        1. Divide large assignments into smaller tasks.

        2. Choose only a few important priorities each day.

        3. Use focused study periods followed by short breaks.

        4. Avoid comparing your academic progress continuously with others.

        5. Ask teachers, classmates or mentors for clarification when needed.

        6. Schedule rest before you become completely exhausted.
        """
    )


# ============================================================
# STRESS RESET
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🧘 5-Minute Stress Reset"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.info(
            """
            **Minute 1**

            Stop what you are doing.

            Take slow breaths.
            """
        )

    with col2:

        st.info(
            """
            **Minutes 2–3**

            Relax your shoulders.

            Notice your surroundings.
            """
        )

    with col3:

        st.info(
            """
            **Minutes 4–5**

            Choose one small next task.

            Ignore everything else temporarily.
            """
        )


# ============================================================
# SOCIAL SUPPORT
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🤝 Build a Support Network"
    )

    st.write(
        """
        Consider staying connected with:

        - Trusted friends
        - Family members
        - Classmates
        - Faculty mentors
        - College counsellors
        - Qualified mental-health professionals

        Reaching out for help is not weakness.
        """        
    )


# ============================================================
# WARNING SIGNS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "⚠️ When Extra Support May Be Helpful"
    )

    st.warning(
        """
        Consider speaking with a qualified professional when difficulties
        continue for a long time or interfere significantly with daily life.

        Examples include:

        - Persistent sadness or hopelessness
        - Severe or continuing anxiety
        - Major sleep problems
        - Withdrawal from friends and activities
        - Difficulty concentrating for long periods
        - Major changes in appetite or energy
        - Feeling unable to cope with normal responsibilities
        """
    )


# ============================================================
# CRISIS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "🚨 Immediate Safety"
    )

    st.error(
        """
        If you or someone else may be in immediate danger:

        - Do not remain alone.
        - Contact a trusted adult or responsible person immediately.
        - Contact local emergency services.
        - Seek urgent professional medical support.

        This application cannot provide emergency or crisis care.
        """
    )


# ============================================================
# HEALTHY DIGITAL HABITS
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "📱 Healthy Digital Habits"
    )

    st.write(
        """
        - Take regular breaks from continuous screen use.
        - Avoid unnecessary scrolling before sleep.
        - Disable distracting notifications during study.
        - Make time for offline activities.
        - Avoid comparing your life continuously with social-media content.
        """
    )


# ============================================================
# REMINDER
# ============================================================

with st.container(
    border=True
):

    st.subheader(
        "✨ Remember"
    )

    st.success(
        """
        You do not need to solve everything at once.

        Small improvements in sleep, stress management, social connection,
        activity and study balance can make daily life easier.
        """
    )


st.caption(
    "This guide provides general educational information and does not replace professional advice."
)