import sqlite3

DB_NAME = "talentscout.db"

def init_db():
    """Initialize database with candidates and responses tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Candidates table
    c.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        experience INTEGER,
        position TEXT,
        location TEXT,
        tech_stack TEXT
    )
    """)

    # Responses table
    c.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        question TEXT,
        answer TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)

    conn.commit()
    conn.close()

def insert_candidate(name, email, phone, experience, position, location, tech_stack):
    """Insert candidate info into candidates table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidates (name, email, phone, experience, position, location, tech_stack)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, experience, position, location, tech_stack))
    conn.commit()
    candidate_id = c.lastrowid
    conn.close()
    return candidate_id

def insert_response(candidate_id, question, answer):
    """Insert a candidate's answer to a question."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO responses (candidate_id, question, answer)
        VALUES (?, ?, ?)
    """, (candidate_id, question, answer))
    conn.commit()
    conn.close()

def get_candidate_by_id(candidate_id):
    """Fetch candidate details by ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    candidate = c.fetchone()
    conn.close()
    return candidate

def get_all_responses(candidate_id):
    """Fetch all responses for a candidate."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM responses WHERE candidate_id = ?", (candidate_id,))
    responses = c.fetchall()
    conn.close()
    return responses

def get_all_candidates():
    """Fetch all candidates with basic info."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, position, tech_stack FROM candidates")
    candidates = c.fetchall()
    conn.close()
    return candidates
