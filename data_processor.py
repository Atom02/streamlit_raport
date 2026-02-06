import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
from utils import generate_token
import os

DB_PATH = 'report_card.db'

def init_db():
    """Initializes the SQLite database with students and scores tables."""
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_id TEXT,
                name TEXT,
                access_token TEXT UNIQUE
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                score_type TEXT,
                score REAL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """))
        conn.commit()
    return engine

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def regenerate_token(student_id):
    """Regenerates the access token for a student."""
    new_token = generate_token()
    engine = create_engine(f'sqlite:///{DB_PATH}')
    with engine.connect() as conn:
        conn.execute(text("UPDATE students SET access_token = :token WHERE id = :id"), 
                     {'token': new_token, 'id': student_id})
        conn.commit()
    return new_token

def parse_data(file):
    """
    Parses the input file (CSV or Excel).
    Assumes header is 2 rows.
    """
    filename = file.name
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file, header=[0, 1])
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file, header=[0, 1])
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")
    
    # 1. Clean Columns
    # Forward fill the top level header (Attributes like MATEMATIKA, IPAS)
    new_columns = []
    last_top = None
    
    for top, bottom in df.columns:
        if str(top).startswith('Unnamed'):
            top = last_top
        else:
            last_top = top
            
        if str(bottom).startswith('Unnamed'):
            bottom = ''
            
        new_columns.append((top, bottom))
        
    df.columns = pd.MultiIndex.from_tuples(new_columns)
    
    # 2. Rename basic columns for clarity
    # We look for "Nama Siswa" or "Nama" in the first few columns
    # Heuristic: Column 1 is usually Name. Column 0 is No.
    
    # Let's verify where 'No' and 'Nama Siswa' are.
    # We can try to rename specifically if they exist.
    
    # Rename level 0 columns if they match known patterns
    rename_map = {}
    for col in df.columns.levels[0]:
        if "Nama" in str(col):
            rename_map[col] = 'Name'
        if "No" == str(col):
            rename_map[col] = 'No'
            
    df.rename(columns=rename_map, level=0, inplace=True)
    
    return df

def save_to_db(df):
    """
    Saves the parsed dataframe to DB.
    1. Upsert Student (Name based)
    2. Replace scores
    """
    engine = init_db()
    
    # Get just the name column (level 0)
    # The dataframe has MultiIndex columns.
    # We need to iterate rows.
    
    # Filter out columns that are not subjects.
    # Subjects are columns where level 1 is not empty OR level 0 is not No/Name
    # But simpler: Just iterate all and skip No/Name
    
    with engine.connect() as conn:
        for idx, row in df.iterrows():
            # Handle Name (it's a tuple key in series if we are not careful)
            # Accessing MultiIndex column 'Name', '' 
            name = row.get(('Name', ''))
            original_id = row.get(('No', '')) # Using the CSV 'No' as original_id
            
            if pd.isna(name):
                continue
                
            # Check if student exists
            existing = conn.execute(text("SELECT id FROM students WHERE name = :name"), {'name': name}).fetchone()
            
            if existing:
                student_db_id = existing[0]
                # Delete old scores
                conn.execute(text("DELETE FROM scores WHERE student_id = :id"), {'id': student_db_id})
            else:
                token = generate_token()
                result = conn.execute(text("INSERT INTO students (original_id, name, access_token) VALUES (:oid, :name, :token)"), 
                                      {'oid': original_id, 'name': name, 'token': token})
                student_db_id = result.lastrowid
            
            # Insert new scores
            for col_tuple, value in row.items():
                subject = col_tuple[0]
                score_type = col_tuple[1]
                
                # Skip meta columns
                if subject in ['No', 'Name', 'Nama Siswa']:
                    continue
                    
                # Clean Score (handle commas as decimals if string)
                if isinstance(value, str):
                    value = value.replace(',', '.')
                
                try:
                    score_val = float(value)
                except (ValueError, TypeError):
                    score_val = None 
                
                # Insert even if score is None, to preserve the subject in the DB
                # This ensures "all_subjects" query finds it.
                conn.execute(text("""
                    INSERT INTO scores (student_id, subject, score_type, score) 
                    VALUES (:sid, :sub, :type, :val)
                """), {'sid': student_db_id, 'sub': subject, 'type': score_type, 'val': score_val})
        
        conn.commit()

def get_all_students():
    """Returns list of all students with tokens."""
    conn = get_db_connection()
    students = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return students

def get_student_report(token):
    """
    Returns (student_info, scores_df, all_subjects_list) for a given token.
    """
    conn = get_db_connection()
    try:
        student = pd.read_sql("SELECT * FROM students WHERE access_token = ?", conn, params=(token,)).iloc[0]
    except IndexError:
        conn.close()
        return None, None, []
        
    scores = pd.read_sql("SELECT subject, score_type, score FROM scores WHERE student_id = ?", conn, params=(int(student['id']),))
    all_subjects = pd.read_sql("SELECT DISTINCT subject FROM scores", conn)['subject'].tolist()
    
    conn.close()
    
    return student, scores, all_subjects

def clear_all_scores():
    """Clears all scores from the database but keeps student records and tokens."""
    engine = create_engine(f'sqlite:///{DB_PATH}')
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM scores"))
        conn.commit()

