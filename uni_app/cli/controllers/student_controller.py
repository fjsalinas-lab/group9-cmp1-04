from uni_app.model.database import Database
from uni_app.model.student import Student, EMAIL_RE, PASS_RE
from uni_app.cli.controllers.enrolment_controller import enrolment_menu

db = Database()

def student_menu():
    """
    Student menu loop for registration and login.

    Options:
        (l)ogin: Log in as an existing student.
        (r)egister: Register a new student account.
        (x)it: Return to the main menu.
    """
    while True:
        print("Student System (l/r/x): ")
        match input(">>> ").lower():
            case "l":
                _login_flow()
            case "r":
                _register_flow()
            case "x":
                return
            case _:
                print("Invalid option")

def _login_flow():

    print("------------------ Student Sign in ------------------")
    email = input("Email: ")
    

    if not EMAIL_RE.fullmatch(email):
        print("\nIncorrect email format.")
        print("Email format acceptable: must end with @university.com")
        print("Example: firstname.lastname@university.com\n")
        return
    
    password = input("Password: ")
    
    # Validate password format
    if not PASS_RE.fullmatch(password):
        print("\nIncorrect password format.")
        print("Password format acceptable: starts with an uppercase letter, at least 5 letters, followed by 3+ digits")
        print("Example: Password123\n")
        return

    existing_students = db.load()
    logged_in_student = None

    for student in existing_students:
        if student.email == email and student.password == password:
            logged_in_student = student
            break

    if logged_in_student:
        print(f"\nLogin successful! Welcome, {logged_in_student.name}.")
        enrolment_menu(logged_in_student)
    else:
        print("\nStudent does not exist or credentials don't match.\n")

    print("\n---------------------------------------------------")

def _register_flow():

    print("------------------ New Student Registration ------------------")
    email = input("Email: ")
    

    if not EMAIL_RE.fullmatch(email):
        print("\nInvalid email format.")
        print("Your email must meet the following conditions:")
        print("  * End with '@university.com'")
        print("  * The part before '@university.com' should consist of lowercase letters (a-z), optionally separated by dots (e.g., 'firstname.lastname').")
        print("  * Example: 'your.name@university.com'\n")
        return
    
    password = input("Password: ")

    if not PASS_RE.fullmatch(password):
        print("\nInvalid password format.")
        print("Your password must meet the following conditions:")
        print("  * Start with an uppercase letter.")
        print("  * Have at least 5 letters in total at the beginning.")
        print("  * End with at least 3 digits.")
        print("  * Contain only letters and digits.")
        print("  * Example: Password123\n")
        return


    existing_students = db.load()
    for s in existing_students:
        if s.email == email:
            print(f"Student {s.name} with email {email} already exists.")
            return


    name = input("Name: ")

    try:
        new_student = Student(name=name, email=email, password=password)
        db.add(new_student)
        print(f"Enrolling Student {new_student.name}")
    except ValueError as e:
 
        print(f"Registration failed: {e}")
       