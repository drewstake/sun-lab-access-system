# gui.py
# GUI for SUN Lab Access System

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from datetime import datetime
import database

class AdminGUI:
    def __init__(self, db):
        """
        Initialize the Admin GUI with the database connection.
        """
        self.db = db
        self.root = tk.Tk()
        self.root.title("SUN Lab Access System - Admin")
        self.root.geometry("800x600")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Create frames for different tabs
        self.create_access_logs_tab()
        self.create_manage_students_tab()
        
    def create_access_logs_tab(self):
        """
        Create the Access Logs tab in the GUI.
        """
        self.access_logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.access_logs_frame, text="Access Logs")
        
        # Filters Frame
        filters_frame = ttk.LabelFrame(self.access_logs_frame, text="Filters")
        filters_frame.pack(fill='x', padx=10, pady=10)
        
        # Student ID Filter
        ttk.Label(filters_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.student_id_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.student_id_var).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Date Filter
        ttk.Label(filters_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.date_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.date_var).grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # Time Range Filter
        ttk.Label(filters_frame, text="Start Time (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.start_time_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.start_time_var).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(filters_frame, text="End Time (HH:MM):").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.end_time_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.end_time_var).grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        # Search Button
        ttk.Button(filters_frame, text="Search", command=self.search_access_logs).grid(row=2, column=3, padx=5, pady=10, sticky='e')
        
        # Treeview for Access Logs
        self.access_logs_tree = ttk.Treeview(self.access_logs_frame, columns=("Student ID", "Timestamp"), show='headings')
        self.access_logs_tree.heading("Student ID", text="Student ID")
        self.access_logs_tree.heading("Timestamp", text="Timestamp")
        self.access_logs_tree.column("Student ID", width=100)
        self.access_logs_tree.column("Timestamp", width=200)
        self.access_logs_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Populate all access logs initially
        self.populate_access_logs()
        
    def create_manage_students_tab(self):
        """
        Create the Manage Students tab in the GUI.
        """
        self.manage_students_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_students_frame, text="Manage Students")
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self.manage_students_frame)
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Add Student", command=self.add_student).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Suspend Student", command=lambda: self.update_student_status("Suspended")).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Activate Student", command=lambda: self.update_student_status("Active")).pack(side='left', padx=5)
        
        # Treeview for Students
        self.students_tree = ttk.Treeview(self.manage_students_frame, columns=("Student ID", "Name", "Status"), show='headings')
        self.students_tree.heading("Student ID", text="Student ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Status", text="Status")
        self.students_tree.column("Student ID", width=100)
        self.students_tree.column("Name", width=200)
        self.students_tree.column("Status", width=100)
        self.students_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Populate all students initially
        self.populate_students()
        
    def populate_access_logs(self, logs=None):
        """
        Populate the Access Logs treeview with data.
        """
        # Clear existing data
        for item in self.access_logs_tree.get_children():
            self.access_logs_tree.delete(item)
        
        # Fetch logs from database if not provided
        if logs is None:
            logs = self.db.get_access_logs()
        
        # Insert logs into treeview
        for log in logs:
            student_id, timestamp = log
            self.access_logs_tree.insert("", "end", values=(student_id, timestamp))
    
    def search_access_logs(self):
        """
        Search access logs based on the provided filters.
        """
        student_id = self.student_id_var.get().strip()
        date = self.date_var.get().strip()
        start_time = self.start_time_var.get().strip()
        end_time = self.end_time_var.get().strip()
        
        time_range = None
        if start_time and end_time:
            # Validate time format
            try:
                datetime.strptime(start_time, "%H:%M")
                datetime.strptime(end_time, "%H:%M")
                time_range = (start_time, end_time)
            except ValueError:
                messagebox.showerror("Invalid Time Format", "Please enter time in HH:MM format.")
                return
        
        # Validate date format
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter date in YYYY-MM-DD format.")
                return
        
        # Fetch filtered logs
        logs = self.db.search_access_logs(student_id=student_id if student_id else None,
                                         date=date if date else None,
                                         time_range=time_range)
        
        self.populate_access_logs(logs)
    
    def populate_students(self):
        """
        Populate the Students treeview with data.
        """
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Fetch students from database
        students = self.db.get_students()
        
        # Insert students into treeview
        for student in students:
            student_id, name, status = student
            self.students_tree.insert("", "end", values=(student_id, name, status))
    
    def add_student(self):
        """
        Prompt the admin to add a new student.
        """
        # Prompt for Student ID
        student_id = simpledialog.askstring("Add Student", "Enter Student ID:")
        if not student_id:
            return  # Cancelled
        
        # Prompt for Name
        name = simpledialog.askstring("Add Student", "Enter Student Name:")
        if not name:
            return  # Cancelled
        
        # Add student to database
        success = self.db.add_student(student_id=student_id.strip(), name=name.strip())
        if success:
            messagebox.showinfo("Success", f"Student '{name}' added successfully.")
            self.populate_students()
        else:
            messagebox.showerror("Error", f"Student ID '{student_id}' already exists.")
    
    def update_student_status(self, new_status):
        """
        Update the status of the selected student.
        """
        selected_item = self.students_tree.selection()
        if not selected_item:
            messagebox.showerror("No Selection", "Please select a student to update.")
            return
        
        student = self.students_tree.item(selected_item)["values"]
        student_id, name, current_status = student
        
        if current_status == new_status:
            messagebox.showinfo("No Change", f"Student '{name}' is already '{new_status}'.")
            return
        
        # Update status in database
        success = self.db.update_student_status(student_id=student_id, new_status=new_status)
        if success:
            messagebox.showinfo("Success", f"Student '{name}' status updated to '{new_status}'.")
            self.populate_students()
        else:
            messagebox.showerror("Error", "Failed to update student status.")
    
    def run(self):
        """
        Run the main loop of the GUI.
        """
        self.root.mainloop()
