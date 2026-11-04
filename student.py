class Student:
    def __init__(self, student_id, full_name, class_form, gender, date_of_birth):
        self.student_id = student_id
        self.full_name = full_name
        self.class_form = class_form
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.scores = {}

    def display_details(self):
        print("\n--- STUDENT DETAILS ---")
        print("Student ID:", self.student_id)
        print("Full Name:", self.full_name)
        print("Class/Form:", self.class_form)
        print("Gender:", self.gender)
        print("Date of Birth:", self.date_of_birth)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_form": self.class_form,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": self.scores
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(
            data["student_id"],
            data["full_name"],
            data["class_form"],
            data["gender"],
            data["date_of_birth"]
        )

        student.scores = data.get("scores", {})
        return student