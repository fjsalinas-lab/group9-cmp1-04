def main_menu():

    while True:
        print("University System: (A)dmin, (S)tudent, or X")
        choice = input(">>> ").lower()
        match choice:
            case "a":
                from . import admin_controller
                admin_controller.admin_menu()
            case "s":
                from . import student_controller
                student_controller.student_menu()
            case "x":
                print("Thank You.")
                break
            case _:
                print("Invalid option")
