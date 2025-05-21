from uni_app.model.database import Database
from itertools import groupby
from operator import attrgetter

db = Database()

GRADE_RANK = {'HD': 5, 'D': 4, 'C': 3, 'P': 2, 'F': 1, 'N/A': 0}

def admin_menu():
    
    while True:
        print("Admin System (c/g/p/r/s/x): ")
        choice = input(">>> ").lower()
        match choice:
            case "c":
                _handle_clear_database()
            case "g":
                _handle_group_students()
            case "p":
                _handle_partition_students()
            case "r":
                _handle_remove_student()
            case "s":
                _handle_show_all_students()
            case "x":
                return
            case _:
                print("Invalid option")

def _handle_show_all_students():
    print("\n------------------ Student List ------------------\n")
    students = db.load()
    
    if not students:
        print("< No students to Display >")
        return
    
    for student in students:
        print(f"{student.name} :: {student.id} --> Email: {student.email}")

    print("\n---------------------------------------------------")

def _handle_group_students():
 

    print("\n------------------ Grade Grouping ------------------")
    students = db.load()
    
    if not students:
        print("< Nothing to Display >")
        return
    

    for student in students:
        student.avg_mark    = student.average()                  
        student.group_grade = student.average_label() if student.subjects else 'N/A'

    students.sort(key=lambda s: GRADE_RANK[s.group_grade], reverse=True)


    for grade, group in groupby(students, key=attrgetter('group_grade')):
        print(f"\nGrade: {grade}")
        for student in group:
            print(f"  {student.name} :: {student.id}  —  MARK: {student.avg_mark:>6.2f}")

    print("\n---------------------------------------------------")


def _handle_partition_students():

    print("\n------------------ PASS/FAIL Partition ------------------")
    students = db.load()
    
    if not students:
        print("FAIL -> []")
        print("PASS -> []")
        return
    
    pass_students = []
    fail_students = []
    
    for student in students:
        if student.has_passed():
            pass_students.append(student)
        else:
            fail_students.append(student)
    

    print("FAIL -> [", end="")
    if fail_students:
        print(", ".join(f"{s.name} ({s.id})" for s in fail_students), end="")
    print("]")
    
    print("PASS -> [", end="")
    if pass_students:
        print(", ".join(f"{s.name} :: {s.id}" for s in pass_students), end="")
    print("]")

    print("\n---------------------------------------------------")

def _handle_remove_student():

    print("\n------------------ Remove Student ------------------")
    student_id = input("Remove by ID: ")
    
    students = db.load()
    student_exists = any(s.id == student_id for s in students)
    
    if not student_exists:
        print(f"No student found with ID: {student_id}")
        return
    

    db.remove_by_id(student_id)
    print(f"Removing student {student_id} Account")
    print("\n---------------------------------------------------")

def _handle_clear_database():

    print("\n------------------ Clear Database ------------------")
    confirmation = input("Are you sure you want to clear the database (Y)es/(N)o: ").lower()
    
    if confirmation == 'y':
        db.clear()
        print("Students data cleared")
    else:
        print("Operation cancelled")

    print("\n---------------------------------------------------")
