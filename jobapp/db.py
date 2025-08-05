import sqlite3
import json 
from typing import List, Dict, Optional

#path
DB_PATH = 'data/sessions.db' 

#function to initialize database

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()


    # creating table to store session
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Unique ID for each session
            session_name TEXT UNIQUE,                 -- Name of the session (must be unique)
            job_description TEXT,                     -- Job description for the session
            resumes TEXT,                             -- List of resumes (stored as JSON string)
            results TEXT                              -- Results (top matches + summaries, stored as JSON string)
        )
    ''')

    conn.commit()  # Save changes
    conn.close()   # Close the database connection


#Function to save session to the databser

def save_session(session_name: str, job_description: str, resumes: List[str], results: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # insert and update a session
    c.execute('''
        INSERT OR REPLACE INTO sessions (session_name, job_description, resumes, results)
        VALUES (?, ?, ?, ?)
    ''', (
        session_name,
        job_description,
        json.dumps(resumes),  # Convert resume list to JSON string
        json.dumps(results)   # Convert results list to JSON string
    ))

    conn.commit()  # Save to DB
    conn.close()   # Close connection

#Functions to get a list fo all saved sessions
def load_all_sessions() -> List[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT session_name FROM sessions')
    rows = c.fetchall()

    conn.close()
    return [row[0] for row in rows]

# function to load all data for agiven session

def load_session(session_name: str)-> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if row:
        return {
            "job_description": row[0],
            "resumes": json.loads(row[1]),
            "results": json.loads(row[2])
        }
    return None

#funstion to delete a session by name

def delete_session(session_name: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    #delete
    c.execute('DELETE FROM sessions WHERE session_name = ?', (session_name,))

    conn.commit()
    conn.close
