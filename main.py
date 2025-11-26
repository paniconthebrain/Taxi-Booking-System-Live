
import sys
import traceback
from Db.DatabaseCRUD import DatabaseCRUD
from config import DEFAULT_ADMIN, WINDOW_TITLE

def initialize_database():    
    try:
        db = DatabaseCRUD()
        
        success = db.setup_database()
        
        if success:
            db.get_database_info()
            return db
        else:
            
            return db
        
    except Exception as e:
        traceback.print_exc()
        return None


def launch_application():
    # Step 1: Initialize Database
    db = initialize_database()
    try:
        import tkinter as tk
        from UI.LoginPage import LoginPage
        
        # Create main window
        root = tk.Tk()
        
        # Create and run login page
        login_app = LoginPage(root)
        login_app.run()
        
    except ImportError as e:
        print(f"Error importing UI components: {e}")
        print("Make sure all UI files are created properly.")
    except Exception as e:
        print(f"Error launching UI: {e}")
        traceback.print_exc()
    
def main():
    try:
        launch_application()
        
    except Exception as e:
        print(f"\nError: {e}\n")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()