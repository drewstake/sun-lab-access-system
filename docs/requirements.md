# High-Level Requirements

## Functional Requirements

1. **Access Logging**
   - **MUST** record the student ID and timestamp every time a card is swiped.
   - **MUST** store each access record in the database.
   - **MUST** retain access records for 5 years.

2. **Admin Interface**
   - **MUST** provide a graphical user interface (GUI) for authorized administrators.
   - **MUST** allow admins to view the history of SUN Lab access.
   - **MUST** enable admins to filter access records by date, student ID, and time range.

3. **Future Extensions**
   - **SHOULD** support multiple user types (students, faculty members, staff members, janitors).
   - **SHOULD** allow admins to activate, suspend, and reactivate user IDs.

## Non-Functional Requirements

1. **Usability**
   - The GUI **SHALL** be intuitive and user-friendly for administrators.

2. **Performance**
   - The system **SHALL** handle concurrent access logging without significant delays.

3. **Security**
   - Access to the admin interface **SHALL** be restricted to authorized personnel only.
