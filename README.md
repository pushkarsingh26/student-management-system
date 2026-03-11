# Student Management System

This project is a simple Student Management System that allows users to manage student records efficiently. It provides functionalities to add, delete, and search for students, as well as calculate their average marks. The data is stored in a JSON format for easy access and manipulation.

## Features

- Add new students with their details (name, age, marks).
- Delete existing students from the system.
- Calculate the average marks of a student.
- Search for students by name or ID.
- Save and load student data in JSON format.

## Project Structure

```
student-management-system
├── src
│   ├── main.py          # Entry point of the application
│   ├── student.py       # Student class definition
│   ├── manager.py       # StudentManager class for managing students
│   ├── search.py        # Function to search for students
│   └── utils.py         # Utility functions for JSON handling
├── data
│   └── students.json    # JSON file to store student data
├── tests
│   ├── test_student.py   # Unit tests for the Student class
│   ├── test_manager.py   # Unit tests for the StudentManager class
│   └── test_search.py    # Unit tests for the search function
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd student-management-system
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Student Management System, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to manage student records.