import streamlit as st

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# HOME PAGE
# ============================================================

st.title("🧠 MindCare AI")

st.subheader("Student Mental Wellness Companion")

st.write(
    """
    A simple AI-powered space to understand your mental wellness,
    receive personalized guidance, and build healthier daily habits.
    """
)

st.write("")

# ============================================================
# MAIN ACTION
# ============================================================

with st.container(border=True):

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("🌱 How are you feeling today?")

        st.write(
            """
            Take a short wellness assessment and receive insights
            based on your responses.
            """
        )

    with col2:

        st.page_link(
            "pages/1_Assessment.py",
            label="Start Assessment",
            icon="📝"
        )


# ============================================================
# THREE SIMPLE OPTIONS
# ============================================================

st.write("")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("📊 Results")

        st.write(
            "View your latest assessment and personalized guidance."
        )

        st.page_link(
            "pages/2_Result.py",
            label="View Result"
        )


with col2:

    with st.container(border=True):

        st.subheader("📈 Analytics")

        st.write(
            "Understand your wellness progress and patterns."
        )

        st.page_link(
            "pages/3_Analytics.py",
            label="View Analytics"
        )


with col3:

    with st.container(border=True):

        st.subheader("💚 Support")

        st.write(
            "Find helpful wellness resources and support guidance."
        )
        st.page_link(
            "pages/5_Support_Guide.py",
            label="Get Support"
        )
        


# ============================================================
# SMALL REMINDER
# ============================================================

st.write("")

with st.container(border=True):

    st.markdown(
        """
        ### 💡 Daily Reminder

        Small steps matter. Rest well, stay connected,
        move your body, and make time for yourself.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "MindCare AI • Educational wellness support • Not a medical diagnosis"
)