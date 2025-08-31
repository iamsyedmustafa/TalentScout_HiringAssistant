import streamlit as st
from groq import Groq

# Load API key and model from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL = st.secrets.get("MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_questions(tech_stack: str, position: str, experience: str, num_questions: int = 5):
    """
    Generate a fixed number of clean technical questions 
    based on tech stack, position, and experience level.Give the 5 questions as Q1,Q2,Q3,Q4,Q5 , thats it.
    """
    prompt = (
        f"You are an AI interviewer. Generate exactly {num_questions} concise and relevant technical interview questions "
        f"for a candidate applying for the position of {position} with {experience} years of experience. "
        f"The candidate is skilled in {tech_stack}. "
        "The difficulty of the questions should match the experience: "
        "Beginner if <=1 year, Intermediate if 2-4 years, Advanced if >=5 years. "
        "Do NOT include any introductory text. "
        "Format strictly as:\n"
        " ...\n"
        " ...\n"
        " ...\n"
        " ...\n"
        " ..."
    )

    try:
        response_text = ask_llm(prompt)

        # Split lines and clean them
        questions = []
        for line in response_text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith("q") and line[1].isdigit():
                questions.append(line)
            else:
                questions.append(line)

        # Ensure max num_questions
        return questions[:num_questions]

    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback questions
        return [f"Sample question {i+1} on {tech_stack}, {position}, {experience} yrs" for i in range(num_questions)]

