# main.py

from manager import StudentManager

def main():
    student_manager = StudentManager()
    student_manager.load_students_from_json()

    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Calculate Average Marks")
        print("4. Search Student")
        print("5. Show All Students")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            enrollment_no = input("Enter enrollment number: ")
            name = input("Enter student's name: ")
            age = int(input("Enter student's age: "))
            num_subjects = int(input("How many subjects? "))
            marks = {}
            for i in range(num_subjects):
                subject = input(f"  Enter subject {i + 1} name: ").strip()
                mark = float(input(f"  Enter marks for {subject}: "))
                marks[subject] = mark
            student_manager.add_student(name, age, marks, enrollment_no)
        
        elif choice == '2':
            enrollment_no = input("Enter enrollment number to delete: ")
            student_manager.delete_student(enrollment_no)
        
        elif choice == '3':
            enrollment_no = input("Enter enrollment number to calculate average marks: ")
            average = student_manager.get_average_marks(enrollment_no)
            if average is not None:
                print(f"Average marks for Enrollment No {enrollment_no}: {average:.2f}")
        
        elif choice == '4':
            search_term = input("Enter name or enrollment number to search: ")
            results = student_manager.search_student(search_term)
            if not results:
                print("No matching students found.")
            for student in results:
                print(student)
        
        elif choice == '5':
            students = student_manager.students
            if not students:
                print("No students found.")
            else:
                print(f"\n{'Enrollment No':<16} {'Name':<20} {'Age':<5} {'Avg Marks'}")
                print("-" * 55)
                for s in students:
                    print(f"{s.enrollment_no:<16} {s.name:<20} {s.age:<5} {s.get_average_marks():.2f}")

        elif choice == '6':
            student_manager.save_students_to_json()
            print("Exiting the system. Data saved.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()