import os
import json
import pandas as pd
from student import Student

_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.json')

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, name, age, marks, enrollment_no):
        if any(s.enrollment_no == enrollment_no for s in self.students):
            print(f"Enrollment No '{enrollment_no}' already exists.")
            return
        student = Student(name, age, marks, enrollment_no)
        self.students.append(student)
        print(f"Student '{name}' added with Enrollment No: {enrollment_no}")

    def delete_student(self, enrollment_no):
        original_count = len(self.students)
        self.students = [s for s in self.students if s.enrollment_no != enrollment_no]
        if len(self.students) < original_count:
            print(f"Student with Enrollment No '{enrollment_no}' deleted.")
        else:
            print(f"No student found with Enrollment No '{enrollment_no}'.")

    def get_average_marks(self, enrollment_no):
        for student in self.students:
            if student.enrollment_no == enrollment_no:
                return student.get_average_marks()
        print(f"No student found with Enrollment No '{enrollment_no}'.")
        return None

    def search_student(self, search_term):
        results = []
        for student in self.students:
            if search_term.lower() in student.name.lower() or search_term == student.enrollment_no:
                results.append(student)
        return results

    def to_dataframe(self):
        """Return current students as a pandas DataFrame with averages."""
        records = []
        for s in self.students:
            records.append({
                'enrollment_no': s.enrollment_no,
                'name': s.name,
                'age': s.age,
                'marks': s.marks,
                'average': s.get_average_marks()
            })
        return pd.DataFrame(records)

    def save_students_to_json(self, file_path=_DATA_FILE):
        with open(file_path, 'w') as f:
            json.dump([student.__dict__ for student in self.students], f, indent=4)

    def load_students_from_json(self, file_path=_DATA_FILE):
        if not os.path.exists(file_path):
            return
        try:
            with open(file_path, 'r') as f:
                student_data = json.load(f)
                self.students = [Student(**data) for data in student_data]
        except (json.JSONDecodeError, TypeError):
            self.students = []