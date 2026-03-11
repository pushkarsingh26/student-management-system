class Student:
    def __init__(self, name, age, marks, enrollment_no):
        self.enrollment_no = enrollment_no
        self.name = name
        self.age = age
        self.marks = marks  # dict: {subject_name: mark}

    def get_average_marks(self):
        if not self.marks:
            return 0
        values = list(self.marks.values())
        return sum(values) / len(values)

    def __str__(self):
        subjects = ', '.join(f"{sub}: {mark}" for sub, mark in self.marks.items())
        return (f"Enrollment No: {self.enrollment_no}, Name: {self.name}, "
                f"Age: {self.age}, Marks: [{subjects}]")