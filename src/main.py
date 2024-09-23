# main.py
# Entry point for SUN Lab Access System

import gui
import database

def main():
    # Initialize and connect to the database
    db = database.Database()
    db.connect()
    
    # Initialize and run the GUI
    app = gui.AdminGUI(db)
    app.run()
    
    # Close the database connection upon exiting the GUI
    db.close()

if __name__ == "__main__":
    main()
