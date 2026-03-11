import unittest
from src.student import Student
from src.manager import StudentManager
from src.search import search_student

class TestSearchStudent(unittest.TestCase):

    def setUp(self):
        self.manager = StudentManager()
        self.manager.add_student(Student("Alice", 20, [85, 90, 78]))
        self.manager.add_student(Student("Bob", 22, [88, 76, 95]))
        self.manager.add_student(Student("Charlie", 21, [70, 80, 90]))

    def test_search_by_name(self):
        result = search_student(self.manager.students, "Alice")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Alice")

    def test_search_by_partial_name(self):
        result = search_student(self.manager.students, "Al")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Alice")

    def test_search_non_existent_student(self):
        result = search_student(self.manager.students, "David")
        self.assertEqual(len(result), 0)

    def test_search_by_id(self):
        # Assuming we have an ID attribute in the Student class
        self.manager.students[0].id = 1
        self.manager.students[1].id = 2
        self.manager.students[2].id = 3
        
        result = search_student(self.manager.students, 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)

if __name__ == '__main__':
    unittest.main()