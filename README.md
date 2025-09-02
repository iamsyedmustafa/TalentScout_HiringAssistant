TALENTSCOUT - AI Hiring Assistant

An AI-powered hiring assistant built with Streamlit, Groq (LLaMA model), Supabase, and Yagmail.
The app automates candidate screening by:

Collecting candidate details (Name, Email, Position, Tech Stack, Experience)

Generating 5 role-specific technical questions using Groq LLaMA model

Allowing candidates to answer questions step by step

Storing candidate details + responses securely in Supabase

Sending a confirmation email to candidates via Gmail (Yagmail)

FEATURES

Candidate registration form

Automatic 5-question Q&A round based on candidate’s tech stack & role

Responses saved in Supabase database

Email confirmation sent to the candidate after submission

Clean Streamlit UI with multi-step process

Deployable on Streamlit Cloud

TECH STACK

Frontend / App: Streamlit

AI Model: Groq LLaMA
 for generating technical questions

Database: Supabase

Emailing: Yagmail
 with Gmail App Password

Deployment: Streamlit Cloud

PROJECT STRUCTURE

talentscout-hiringassistant/
│── main.py          # Streamlit app entry point
│── db.py            # Supabase integration (insert, fetch, responses)
│── requirements.txt # Dependencies
│── README.md        # Project documentation

SETUP & INSTALLATION

1.Clone the Repository
git clone https://github.com/yourusername/talentscout-hiringassistant.git
cd talentscout-hiringassistant

2️.Install Dependencies
pip install -r requirements.txt

3️.Supabase Setup

Create a new project on Supabase
.

Get your Project URL and Anon API Key from Project Settings → API.

Create tables:

candidates Table
Column	Type
id (PK)	uuid
name	text
position	text
experience	text
email	text
phone	text
tech_stack	text
timestamp	timestamptz (default now)
responses Table
Column	Type
id (PK)	uuid
candidate_id	uuid (FK → candidates.id)
question	text
answer	text
timestamp	timestamptz (default now)

4️.Gmail Setup (Yagmail)

Enable 2FA in your Gmail account.

Generate a Gmail App Password from Google Security
.

Store this in secrets.toml (see below).

5️.Create .streamlit/secrets.toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

GMAIL_USER = "your-email@gmail.com"
GMAIL_PASS = "your-gmail-app-password"

GROQ_API_KEY = "your-groq-api-key"

Run Locally
streamlit run main.py

Deployment (Streamlit Cloud)

Push code to GitHub

Deploy on Streamlit Cloud

Add the above secrets.toml entries in Streamlit → Settings → Secrets

Email Example

Candidates will receive an email after submission:

Subject: Thank You for Applying to TalentScout!

Dear [Candidate Name],

Thank you for completing the technical assessment. 
We’ve recorded your responses and will get back to you soon.

Best regards,  
TalentScout Hiring Team

REQUIREMENTS

requirements.txt should include:

streamlit
supabase
yagmail
groq

DEMO FLOW

Candidate enters details

Groq LLaMA generates 5 technical questions

Candidate answers step by step

Responses stored in Supabase

Candidate gets confirmation email

Author

Syed Mustafa Ahmed
Email: syedmustafaahmed3733@gmail.com