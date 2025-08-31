import streamlit as st
import db
from ai import generate_questions
import re
import yagmail  # pip install yagmail

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

def send_thank_you_email(to_email, candidate_name):
    """Send email to candidate after submission"""
    sender_email = st.secrets["EMAIL_USER"]
    sender_password = st.secrets["EMAIL_PASS"]

    subject = "Thank you for your response - Talentscout"
    body = f"""
    Hi {candidate_name},

    Thank you for submitting your responses. We are currently reviewing your application 
    and will reach out to you soon.

    Best regards,
    PGAGI Talent Team
    """
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(to=to_email, subject=subject, contents=body)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

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
        if location == "Other":
             other_location = st.text_input("Please specify your location *")
        else:
            other_location = ""
        tech_stack = st.text_area("Tech Stack (comma separated) *")

        submitted = st.form_submit_button("Save & Continue")

        if submitted:
            errors = []

            if not name.strip(): errors.append("Full Name")
            if not position.strip(): errors.append("Position")
            if not tech_stack.strip(): errors.append("Tech Stack")
            if not is_valid_email(email): errors.append("Valid Email")
            if not phone.isdigit() or len(phone) != 10: errors.append("Valid 10-digit Phone")
            if location == "Other" and not other_location.strip():
                errors.append("Please specify your location")

            if errors:
                st.error(f"⚠️ Please correct the following fields: {', '.join(errors)}")
            else:
                final_location = other_location.strip() if location == "Other" else location

                candidate_id = db.insert_candidate(
                    name.strip(), email.strip(), phone.strip(),
                    experience, position.strip(), final_location, tech_stack.strip()
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

# ---------------- Step 2: Technical Q&A ----------------
elif st.session_state.step == 2:
    candidate = db.get_candidate_by_id(st.session_state.candidate_id)
    
    tech_stack = candidate[7]      # tech_stack column
    position = candidate[2]        # position column
    experience = candidate[3]      # experience column

    # Generate questions only once
    if not st.session_state.questions:
        st.session_state.questions = generate_questions(tech_stack, position, experience)

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
    else:
        st.success("🎉 Thank you! Your responses have been recorded. We will reach out to you soon.")
        st.subheader("Your Answers Summary:")
        for i, (q, a) in enumerate(st.session_state.answers.items()):
            st.write(f"**Q{i+1}: {q}**")
            st.write(f"**A:** {a}")

        # ---------------- Send Thank You Email ----------------
        candidate_name = candidate[1]  # name column
        candidate_email = candidate[2]  # email column
        send_thank_you_email(candidate_email, candidate_name)


