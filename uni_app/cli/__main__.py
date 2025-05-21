"""
CLI entry point for the university app. Runs the main menu loop.
"""
from .controllers import university_controller

if __name__ == "__main__":
    try:
        university_controller.main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
