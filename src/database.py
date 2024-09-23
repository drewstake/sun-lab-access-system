# Database management for SUN Lab Access System

import sqlite3

class Database:

    def __init__(self, db_path="sun_lab_access.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create students table
        cursor.execute(
            \"\"\"
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT
            )
            \"\"\"
        )
        # Create access_logs table
        cursor.execute(
            \"\"\"
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                timestamp DATETIME,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            \"\"\"
        )
        self.conn.commit()

    # Add more database methods as needed
