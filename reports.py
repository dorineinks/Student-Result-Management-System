from results import calculate_total, calculate_average, assign_grade


def generate_report_card(student):
    if not student.scores:
        print("No results available for this student.")
        return

    total = calculate_total(student)
    average = calculate_average(student)
    grade = assign_grade(average)

    print("\n===================================")
    print("       STUDENT REPORT CARD")
    print("===================================")

    print("Student ID:", student.student_id)
    print("Full Name:", student.full_name)
    print("Class:", student.class_form)

    print("-----------------------------------")
    print("SUBJECT SCORES")
    print("-----------------------------------")

    for subject, score in student.scores.items():
        print(f"{subject}: {score}")

    print("-----------------------------------")
    print("Total Score:", total)
    print("Average:", round(average, 2))
    print("Grade:", grade)
    print("===================================")

    
def list_student_results(students):
    print("\n--- ALL STUDENT RESULTS ---")

    if not students:
        print("No students registered.")
        return

    for student in students:
        print("\n------------------------------")
        print("Student ID:", student.student_id)
        print("Full Name:", student.full_name)
        print("Class:", student.class_form)

        if student.scores:
            total = calculate_total(student)
            average = calculate_average(student)
            grade = assign_grade(average)

            print("Total Score:", total)
            print("Average:", round(average, 2))
            print("Grade:", grade)
        else:
            print("Results: No scores recorded.")

        print("------------------------------")


def sort_students(students):
    print("\n--- SORT STUDENTS ---")
    print("1. Sort by Average (Highest to Lowest)")
    print("2. Sort by Name (A-Z)")

    choice = input("Choose sorting option: ")

    if choice == "1":
        sorted_students = sorted(
            students,
            key=lambda student: calculate_average(student)
            if student.scores else -1,
            reverse=True
        )

    elif choice == "2":
        sorted_students = sorted(
            students,
            key=lambda student: student.full_name.lower()
        )

    else:
        print("Invalid sorting option.")
        return

    list_student_results(sorted_students)


def class_statistics(students):
    print("\n--- CLASS STATISTICS ---")

    students_with_scores = [
        student for student in students if student.scores
    ]

    if not students_with_scores:
        print("No student results available.")
        return

    averages = [
        calculate_average(student)
        for student in students_with_scores
    ]

    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("Number of Students:", len(students_with_scores))
    print("Highest Average:", round(highest, 2))
    print("Lowest Average:", round(lowest, 2))
    print("Class Average:", round(class_average, 2))


def save_class_report(students):
    print("\n--- SAVE CLASS REPORT ---")

    report = "STUDENT RESULT MANAGEMENT SYSTEM\n"
    report += "CLASS PERFORMANCE REPORT\n"
    report += "=" * 40 + "\n"

    for student in students:
        report += f"\nStudent ID: {student.student_id}\n"
        report += f"Name: {student.full_name}\n"
        report += f"Class: {student.class_form}\n"

        if student.scores:
            total = calculate_total(student)
            average = calculate_average(student)
            grade = assign_grade(average)

            report += f"Total: {total}\n"
            report += f"Average: {average:.2f}\n"
            report += f"Grade: {grade}\n"
        else:
            report += "Results: No scores recorded.\n"

        report += "-" * 40 + "\n"

    with open("class_report.txt", "w") as file:
        file.write(report)

    print("Class report saved successfully!")
    print("File name: class_report.txt")

