import streamlit as st
import db
from ai import generate_questions
import re

# Initialize database
db.init_db()

# ---------------- Session State ----------------
if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "step" not in st.session_state:
    st.session_state.step = 1  # Step 1: Candidate Info

st.title("💼 Talentscout - AI Hiring Assistant at PGAGI")

# ---------------- Helper Functions ----------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# ---------------- Step 1: Candidate Info ----------------
if st.session_state.step == 1:
    st.info("👋 Hello! I am Talentscout, your AI hiring assistant at PGAGI. Please enter your information to proceed.")

    with st.form("candidate_form"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone (10 digits) *")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.text_input("Position Applied For *")
        locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Other"]
        location = st.selectbox("Location *", locations)
        tech_stack = st.text_area("Tech Stack (comma separated) *")

        submitted = st.form_submit_button("Save & Continue")

        if submitted:
            errors = []

            if not name.strip(): errors.append("Full Name")
            if not position.strip(): errors.append("Position")
            if not tech_stack.strip(): errors.append("Tech Stack")
            if not is_valid_email(email): errors.append("Valid Email")
            if not phone.isdigit() or len(phone) != 10: errors.append("Valid 10-digit Phone")

            if errors:
                st.error(f"⚠️ Please correct the following fields: {', '.join(errors)}")
            else:
                # Save candidate in DB
                candidate_id = db.insert_candidate(
                    name.strip(), email.strip(), phone.strip(),
                    experience, position.strip(), location, tech_stack.strip()
                )
                st.session_state.candidate_id = candidate_id
                st.session_state.info_saved = True
                st.success("✅ Your information has been saved successfully!")

# ---------------- Step 1b: Proceed Button ----------------
if st.session_state.get("info_saved", False) and st.session_state.step == 1:
    st.info("Now, I would like to ask you a few technical questions based on your tech stack.")
    if st.button("Okay, let's proceed!"):
        st.session_state.step = 2
        st.session_state.info_saved = False

