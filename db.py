from supabase import create_client, Client
import os

# ---------------- Supabase Config ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- Database Init ----------------
def init_db():
    """Initialize Supabase tables if they don't exist."""
    # In Supabase, you generally create tables via the web dashboard.
    # For first-time setup, create these tables manually:
    #
    # Table: candidates
    # Columns: id (bigint, primary key, auto-increment)
    #          name (text), email (text), phone (text)
    #          experience (int), position (text), location (text)
    #          tech_stack (text)
    #
    # Table: responses
    # Columns: id (bigint, primary key, auto-increment)
    #          candidate_id (bigint, foreign key -> candidates.id)
    #          question (text), answer (text)
    #
    # This function can remain empty; table creation happens in dashboard.
    pass

# ---------------- Candidate Functions ----------------
def insert_candidate(name, email, phone, experience, position, location, tech_stack):
    """Insert candidate info into Supabase candidates table."""
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "position": position,
        "location": location,
        "tech_stack": tech_stack
    }
    response = supabase.table("candidates").insert(data).execute()
    candidate_id = response.data[0]["id"]
    return candidate_id

def insert_response(candidate_id, question, answer):
    """Insert a candidate's answer into Supabase responses table."""
    data = {
        "candidate_id": candidate_id,
        "question": question,
        "answer": answer
    }
    supabase.table("responses").insert(data).execute()

def get_candidate_by_id(candidate_id):
    """Fetch candidate details by ID."""
    response = supabase.table("candidates").select("*").eq("id", candidate_id).execute()
    if response.data:
        # Return as tuple like SQLite for compatibility
        c = response.data[0]
        return (c["id"], c["name"], c["email"], c["phone"], c["experience"], c["position"], c["location"], c["tech_stack"])
    return None

def get_all_responses(candidate_id):
    """Fetch all responses for a candidate."""
    response = supabase.table("responses").select("question, answer").eq("candidate_id", candidate_id).execute()
    # Return as list of tuples
    return [(r["question"], r["answer"]) for r in response.data]

def get_all_candidates():
    """Fetch all candidates with basic info."""
    response = supabase.table("candidates").select("id, name, email, phone, position, tech_stack").execute()
    return [(c["id"], c["name"], c["email"], c["phone"], c["position"], c["tech_stack"]) for c in response.data]

