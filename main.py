from student import Student
from results import record_scores, update_scores
from reports import generate_report_card
from reports import (
    generate_report_card,
    list_student_results,
    sort_students,
    class_statistics,
    save_class_report
)
from storage import save_students, load_students
from datetime import datetime


students = []


def add_student():
    print("\n--- ADD NEW STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    for student in students:
        if student.student_id.lower() == student_id.lower():
            print("Student ID already exists!")
            return

    full_name = input("Enter Full Name: ").strip()
    class_form = input("Enter Class/Form: ").strip()
    gender = input("Enter Gender (Male/Female): ").strip().capitalize()
    date_of_birth = input("Enter Date of Birth (DD/MM/YYYY): ").strip()

    if not full_name or not class_form:
        print("Name and class are required.")
        return

    if gender not in ["Male", "Female"]:
        print("Invalid gender. Enter Male or Female.")
        return

    try:
        datetime.strptime(date_of_birth, "%d/%m/%Y")
    except ValueError:
        print("Invalid date. Use DD/MM/YYYY.")
        return

    student = Student(
        student_id,
        full_name,
        class_form,
        gender,
        date_of_birth
    )

    students.append(student)
    save_students(students)

    print("Student added successfully!")


def view_students():
    print("\n--- ALL REGISTERED STUDENTS ---")

    if not students:
        print("No students registered yet.")
        return

    for student in students:
        student.display_details()


def search_student():
    print("\n--- SEARCH STUDENT ---")
    print("1. Search by Student ID")
    print("2. Search by Name")

    choice = input("Choose search option: ")

    if choice == "1":
        search_value = input("Enter Student ID: ").strip().lower()

        for student in students:
            if student.student_id.lower() == search_value:
                student.display_details()
                return student

    elif choice == "2":
        search_value = input("Enter Student Name: ").strip().lower()

        for student in students:
            if search_value in student.full_name.lower():
                student.display_details()
                return student

    else:
        print("Invalid search option.")
        return None

    print("Student not found.")
    return None


def update_student():
    student = search_student()

    if not student:
        return

    print("\n--- UPDATE STUDENT DETAILS ---")

    new_name = input("Enter new name (press Enter to keep current): ").strip()
    new_class = input("Enter new class (press Enter to keep current): ").strip()
    new_gender = input("Enter new gender (Male/Female, press Enter to keep current): ").strip()
    new_dob = input("Enter new date of birth (DD/MM/YYYY, press Enter to keep current): ").strip()

    if new_gender:
        new_gender = new_gender.capitalize()

        if new_gender not in ["Male", "Female"]:
            print("Invalid gender. Enter Male or Female.")
            return

    if new_dob:
        try:
            datetime.strptime(new_dob, "%d/%m/%Y")
        except ValueError:
            print("Invalid date. Use DD/MM/YYYY.")
            return

    if new_name:
        student.full_name = new_name

    if new_class:
        student.class_form = new_class

    if new_gender:
        student.gender = new_gender

    if new_dob:
        student.date_of_birth = new_dob

    save_students(students)

    print("Student details updated successfully!")

def delete_student():
    student = search_student()

    if not student:
        return

    confirmation = input("Are you sure you want to delete this student? (yes/no): ")

    if confirmation.lower() == "yes":
        students.remove(student)
        save_students(students)
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


def main():
    global students

    students = load_students()

    while True:
        print("\n===== STUDENT RESULT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Record Student Scores")
        print("7. Update Student Scores")
        print("8. Generate Student Report Card")
        print("9. View All Student Results")
        print("10. Sort Students")
        print("11. View Class Statistics")
        print("12. Save Class Report")
        print("13. Exit")

        choice = input("Enter your choice (1-13): ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            student = search_student()
            if student:
                record_scores(student)
                save_students(students)

        elif choice == "7":
            student = search_student()
            if student:
                update_scores(student)
                save_students(students)

        elif choice == "8":
            student = search_student()
            if student:
                generate_report_card(student)

        elif choice == "9":
            list_student_results(students)

        elif choice == "10":
            sort_students(students)

        elif choice == "11":
            class_statistics(students)

        elif choice == "12":
            save_class_report(students)

        elif choice == "13":
            save_students(students)
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
