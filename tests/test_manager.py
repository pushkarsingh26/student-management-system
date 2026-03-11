import unittest
from src.student import Student
from src.manager import StudentManager

class TestStudentManager(unittest.TestCase):

    def setUp(self):
        self.manager = StudentManager()
        self.student1 = Student(name="Alice", age=20, marks=[85, 90, 78])
        self.student2 = Student(name="Bob", age=22, marks=[70, 75, 80])
        self.manager.add_student(self.student1)
        self.manager.add_student(self.student2)

    def test_add_student(self):
        self.assertEqual(len(self.manager.students), 2)
        self.manager.add_student(Student(name="Charlie", age=21, marks=[88, 92, 95]))
        self.assertEqual(len(self.manager.students), 3)

    def test_delete_student(self):
        self.manager.delete_student(self.student1.name)
        self.assertEqual(len(self.manager.students), 1)
        self.manager.delete_student(self.student2.name)
        self.assertEqual(len(self.manager.students), 0)

    def test_save_students_to_json(self):
        self.manager.save_students_to_json('data/students.json')
        with open('data/students.json', 'r') as f:
            data = f.read()
            self.assertIn("Alice", data)
            self.assertIn("Bob", data)

    def test_load_students_from_json(self):
        self.manager.save_students_to_json('data/students.json')
        new_manager = StudentManager()
        new_manager.load_students_from_json('data/students.json')
        self.assertEqual(len(new_manager.students), 2)

if __name__ == '__main__':
    unittest.main()