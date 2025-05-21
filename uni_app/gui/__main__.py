"""
GUI entry point for the university app.
"""
from uni_app.gui.university_app import run_university_app

if __name__ == "__main__":
    try:
        run_university_app()
    except KeyboardInterrupt:
        print("\nExiting...") 