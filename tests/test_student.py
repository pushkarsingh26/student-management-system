import unittest
from src.student import Student

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(name="John Doe", age=20, marks=[80, 90, 85])

    def test_get_average_marks(self):
        self.assertEqual(self.student.get_average_marks(), 85.0)

    def test_get_average_marks_empty(self):
        empty_student = Student(name="Jane Doe", age=22, marks=[])
        self.assertEqual(empty_student.get_average_marks(), 0.0)

if __name__ == '__main__':
    unittest.main()