from uni_app.model.database import Database
from uni_app.model.student import Student
from uni_app.model.subject import Subject

db = Database()

def enrolment_menu(student):

    while True:
        print("Student Course Manu (c/e/r/s/x): ")
        choice = input(">>> ").lower()
        match choice:
            case "c":
                _handle_change_password(student)
            case "e":
                _handle_enrol_subject(student)
            case "r":
                _handle_remove_subject(student)
            case "s":
                _handle_show_subjects(student)
            case "x":
                return
            case _:
                print("Invalid option")

def _handle_change_password(student: Student):

    print("\n------------------ Change Password ------------------")
    while True:
        new_password = input("Enter new password: ")
        confirm_password = input("Confirm password: ")
        
        if new_password != confirm_password:
            print("Password does not match - try again")
            if input("Try again? (y/n): ").lower() != 'y':
                return
            continue
        
        try:
            student.change_password(new_password)
            db.update(student)
            print("Password changed successfully!")
            return
        except ValueError as e:
            print(f"\nError: {e}")     
            if input("Try again? (y/n): ").lower() != 'y':
                return

def _handle_enrol_subject(student: Student):

    print("\n------------------ Enrol in New Subject ------------------")
    
    if len(student.subjects) >= 4:
        print("Students are allowed to enrol in 4 subjects only")
        return
    

    try:
        new_subject = Subject()
        student.enrol(new_subject)
        db.update(student)
        print(f"\nEnrolling in {new_subject.id}")
        print(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")
    except ValueError as e:
        print(f"Error: {e}")


def _handle_remove_subject(student: Student):

    print("\n------------------ Remove Subject ------------------")
    
    if not student.subjects:
        print("You are not enrolled in any subjects.")
        return
    
    
    subject_id = input("\nRemove Subject by ID: ")
    
        
    # Check if the subject exists
    subject_exists = any(subject.id == subject_id for subject in student.subjects)
    if not subject_exists:
        print(f"No subject found with ID: {subject_id}")
        return
    

    student.drop(subject_id)
    db.update(student)
    print(f"Dropping {subject_id}")
    print(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")

    print("\n---------------------------------------------------")

def _handle_show_subjects(student: Student):

    print("\n------------------ Enrolled Subjects ------------------")
    
    if not student.subjects:
        print("Showing 0 subjects")
        return
    
    print(f"Showing {len(student.subjects)} subjects:")
    for subject in student.subjects:
        print(f"[ Subject::{subject.id} -- mark = {subject.mark} -- grade = {subject.grade} ]")
    
    average = student.average()
    passed = student.has_passed()
    
    print(f"\nAverage Mark: {average}")
    print(f"Overall Status: {'PASS' if passed else 'FAIL'}")

    print("\n---------------------------------------------------")
