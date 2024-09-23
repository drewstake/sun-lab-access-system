# Database Documentation

## Overview

The SUN Lab Access System uses SQLite as its relational database to store access logs and manage user information.

## Tables

### access_logs
- **id** (INTEGER, Primary Key, Auto-increment)
- **student_id** (TEXT, Foreign Key referencing students.student_id)
- **timestamp** (DATETIME)

### students
- **student_id** (TEXT, Primary Key)
- **name** (TEXT)
- **status** (TEXT) — e.g., Active, Suspended

## Relationships

- **One-to-Many:** Each student can have multiple access log entries in the access_logs table.
