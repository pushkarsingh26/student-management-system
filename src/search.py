def search_student(students, search_term):
    matching_students = []
    for student in students:
        if search_term.lower() in student['name'].lower() or search_term == student['id']:
            matching_students.append(student)
    return matching_students