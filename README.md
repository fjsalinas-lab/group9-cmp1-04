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
  # Activate the virtual environment with Tkinter support
  source venv_with_tkinter/bin/activate
  
  # Run the GUI application
  python -m uni_app.gui.main
  ```

## Virtual Environment
The GUI requires Tkinter. If you're experiencing issues with Tkinter not being available, you may need to use the provided virtual environment:

```sh
# Create the virtual environment (if not already created)
/usr/bin/python3 -m venv venv_with_tkinter

# Activate the virtual environment
source venv_with_tkinter/bin/activate
```


