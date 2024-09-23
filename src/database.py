# database.py
# Database management for SUN Lab Access System

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="sun_lab_access.db"):
        """
        Initialize the Database class with the path to the SQLite database.
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """
        Connect to the SQLite database and create tables if they don't exist.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """
        Create the necessary tables: students and access_logs.
        """
        cursor = self.conn.cursor()
        
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Active', 'Suspended'))
            )
        """)
        
        # Create access_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)
        
        self.conn.commit()

    def add_access_log(self, student_id):
        """
        Add an access log entry with the current timestamp.
        """
        cursor = self.conn.cursor()
        timestamp = datetime.now()
        cursor.execute("""
            INSERT INTO access_logs (student_id, timestamp)
            VALUES (?, ?)
        """, (student_id, timestamp))
        self.conn.commit()

    def get_access_logs(self, student_id=None, start_date=None, end_date=None):
        """
        Retrieve access logs with optional filters:
        - student_id: Filter by specific student ID.
        - start_date and end_date: Filter by date range.
        """
        cursor = self.conn.cursor()
        query = "SELECT student_id, timestamp FROM access_logs WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()

    def add_student(self, student_id, name, status='Active'):
        """
        Add a new student to the database.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (student_id, name, status)
                VALUES (?, ?, ?)
            """, (student_id, name, status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Student ID already exists

    def update_student_status(self, student_id, new_status):
        """
        Update the status of a student (e.g., Activate, Suspend, Reactivate).
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE students
            SET status = ?
            WHERE student_id = ?
        """, (new_status, student_id))
        self.conn.commit()
        return cursor.rowcount > 0  # Returns True if a row was updated

    def get_students(self, status=None):
        """
        Retrieve a list of students with an optional status filter.
        """
        cursor = self.conn.cursor()
        query = "SELECT student_id, name, status FROM students WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)
        
        cursor.execute(query, params)
        return cursor.fetchall()

    def search_access_logs(self, student_id=None, date=None, time_range=None):
        """
        Search access logs based on various criteria.
        """
        cursor = self.conn.cursor()
        query = "SELECT student_id, timestamp FROM access_logs WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if date:
            query += " AND DATE(timestamp) = DATE(?)"
            params.append(date)
        
        if time_range:
            start_time, end_time = time_range
            query += " AND TIME(timestamp) BETWEEN TIME(?) AND TIME(?)"
            params.extend([start_time, end_time])
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
