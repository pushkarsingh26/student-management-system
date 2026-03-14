
# Student Management System

An all-in-one Student Management System for managing student records, built with Python. It supports both a terminal-based CLI and a modern web interface (Flask + HTML/JS).

## What does this project help with?

- Effortlessly add, delete, search, and view students
- Calculate average marks for each student
- Use either a terminal or a web browser
- Data is saved in a JSON file for persistence

---

## Project Structure

```
student-management-system/
├── src/
│   ├── main.py         # Terminal CLI (text-based)
│   ├── app.py          # Flask web server (REST API)
│   ├── student.py      # Student class
│   ├── manager.py      # StudentManager (core logic)
│   ├── search.py       # Search helpers
│   └── utils.py        # JSON utilities
├── index.html          # Web frontend (fetches from Flask API)
├── data/
│   └── students.json   # Student data (auto-saved)
├── tests/
│   ├── test_student.py
│   ├── test_manager.py
│   └── test_search.py
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## How to Run

### 1. Clone and Install

```sh
git clone <repository-url>
cd student-management-system
python -m venv .venv
.venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```

### 2. Run in Terminal (CLI)

```sh
python src/main.py
```
Follow the on-screen prompts to add, delete, search, and view students.

### 3. Run as a Web App

```sh
python src/app.py
```
Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Features

- Add new students (name, age, marks, enrollment number)
- Delete students by enrollment number
- Calculate and view average marks
- Search by name or enrollment number
- View all students in a table (web) or list (CLI)
- Data is always saved to `data/students.json`

---


## License

MIT