# group9-cmp1-04 University App

A CLI (and optional GUI) university student/admin management system for COMP1-04.

## Structure

- `uni_app/cli/` - Command-line interface and controllers
- `uni_app/model/` - Business logic (Student, Subject, Database)
- `uni_app/gui/` - GUI (tkinter)
- `students.data` - Pickle file (auto-created, excluded from repo)

## Setup

- Run CLI:
  ```sh
  python -m uni_app.cli
  ```

- For GUI (requires Tkinter):
  ```sh  
  # Run the GUI application
  python -m uni_app.gui.main
  ```


