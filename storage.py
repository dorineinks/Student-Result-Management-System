
import json
import os
from student import Student

FILE_PATH = "data/students.json"


def save_students(students):
    try:
        os.makedirs("data", exist_ok=True)

        student_data = [student.to_dict() for student in students]

        with open(FILE_PATH, "w") as file:
            json.dump(student_data, file, indent=4)

        print("Student records saved successfully!")

    except (OSError, TypeError) as error:
        print("Error saving student records:", error)


def load_students():
    if not os.path.exists(FILE_PATH):
        print("No saved records found. Starting with an empty student list.")
        return []

    try:
        with open(FILE_PATH, "r") as file:
            student_data = json.load(file)

        if not isinstance(student_data, list):
            raise ValueError("The JSON file must contain a list of students.")

        students = [Student.from_dict(data) for data in student_data]

        print("Student records loaded successfully!")
        return students

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("Error loading student records:", error)
        return []

    except OSError as error:
        print("File access error:", error)
        return [] 
