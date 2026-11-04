SUBJECTS = [
    "Mathematics",
    "English",
    "Biology",
    "Chemistry",
    "Physics"
]


def record_scores(student):
    print("\n--- RECORD STUDENT SCORES ---")

    scores = {}

    for subject in SUBJECTS:
        while True:
            try:
                score = float(input(f"Enter score for {subject}: "))

                if 0 <= score <= 100:
                    scores[subject] = score
                    break
                else:
                    print("Score must be between 0 and 100.")

            except ValueError:
                print("Invalid input. Please enter a number.")

    student.scores = scores

    print("Scores recorded successfully!")


def calculate_total(student):
    total = sum(student.scores.values())
    return total


def calculate_average(student):
    total = calculate_total(student)
    average = total / len(SUBJECTS)
    return average


def assign_grade(average):

    if average >= 70:
        return "A"

    elif average >= 60:
        return "B"

    elif average >= 50:
        return "C"

    elif average >= 45:
        return "D"

    else:
        return "F"


def update_scores(student):
    if not student.scores:
        print("No scores found. Please record scores first.")
        return

    print("\n--- UPDATE STUDENT SCORES ---")

    for subject in SUBJECTS:
        current_score = student.scores[subject]

        while True:
            new_score = input(
                f"{subject} (Current: {current_score}) - New score "
                "(press Enter to keep current): "
            ).strip()

            if new_score == "":
                break

            try:
                score = float(new_score)

                if 0 <= score <= 100:
                    student.scores[subject] = score
                    break
                else:
                    print("Score must be between 0 and 100.")

            except ValueError:
                print("Invalid input. Please enter a number.")

    print("Scores updated successfully!")

