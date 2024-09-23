# Entry point for SUN Lab Access System

import gui
import database

def main():
    # Initialize database
    db = database.Database()
    db.connect()

    # Initialize GUI
    app = gui.AdminGUI(db)
    app.run()

if __name__ == "__main__":
    main()
