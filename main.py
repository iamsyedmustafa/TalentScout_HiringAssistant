import streamlit as st
import db
from ai import generate_questions

# Initialize database
db.init_db()

# ---------------- Session State Initialization ----------------
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

# ---------------- Step 1: Candidate Info ----------------
if st.session_state.step == 1:
    st.info("👋 Hello! I am Talentscout, your AI hiring assistant at PGAGI. Please enter your information to proceed.")
    
    with st.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.text_input("Position Applied For")
        location = st.text_input("Location")
        tech_stack = st.text_area("Tech Stack (comma separated)")

        submitted = st.form_submit_button("Save & Continue")

        if submitted:
            if all([name, email, phone, position, location, tech_stack]):
                candidate_id = db.insert_candidate(
                    name, email, phone, experience, position, location, tech_stack
                )
                st.session_state.candidate_id = candidate_id
                st.session_state.info_saved = True
            else:
                st.error("⚠️ Please fill all required fields!")

# ---------------- Step 1b: Proceed Button ----------------
if st.session_state.get("info_saved", False) and st.session_state.step == 1:
    st.success("✅ Great! Your information has been saved.")
    st.info("Now, I would like to ask you a few technical questions based on your tech stack.")
    
    if st.button("Okay, let's proceed!"):
        st.session_state.step = 2
        st.session_state.info_saved = False

# ---------------- Step 2: Technical Q&A ----------------
elif st.session_state.step == 2:
    candidate = db.get_candidate_by_id(st.session_state.candidate_id)
    tech_stack = candidate[7]  # tech_stack column

    # Generate questions once
    if not st.session_state.questions:
        st.session_state.questions = generate_questions(tech_stack, num_questions=5)

    # Ask current question
    if st.session_state.current_q < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_q]
        st.subheader(f"Q{st.session_state.current_q + 1}: {q}")

        answer = st.text_area("Your answer:", key=f"answer_{st.session_state.current_q}")
        if st.button("Submit Answer"):
            if answer.strip():
                db.insert_response(st.session_state.candidate_id, q, answer.strip())
                st.session_state.answers[q] = answer.strip()
                st.session_state.current_q += 1
            else:
                st.warning("⚠️ Please enter an answer before submitting.")

    # All questions answered
    else:
        st.success("🎉 Thank you for submitting your answers! We will review your responses and reach out to you soon.")
        st.subheader("📑 Your Answers Summary:")
        for i, (q, a) in enumerate(st.session_state.answers.items()):
            st.markdown(f"**Q{i+1}: {q}**")
            st.markdown(f"**A:** {a}")
