
# Student Management System

Python-based student records with both a terminal CLI and a Flask-powered web UI. Data persists to JSON; averages and charts use numpy/pandas/matplotlib.

## What this project helps with
- Add, delete, search, and list students (CLI + web)
- Compute averages (numpy) and serve chart visuals (matplotlib)
- Persist data to JSON and expose it via a REST API

## Project Structure
```
student-management-system/
├── src/
│   ├── main.py         # Terminal CLI
│   ├── app.py          # Flask API + charts
│   ├── student.py      # Student model (numpy averages)
│   ├── manager.py      # Core logic (pandas dataframe helper)
│   ├── search.py       # Search helpers
│   └── utils.py        # JSON utilities
├── index.html          # Web frontend (fetch + charts modal)
├── data/
│   └── students.json   # Stored student data
├── tests/              # Pytest suite
├── requirements.txt    # Dependencies
└── README.md
```

## Prerequisites
- Python 3.10+ (venv recommended)
- PowerShell on Windows (commands below assume PowerShell)

## Setup (PowerShell)
```powershell
git clone <repository-url>
cd student-management-system
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Terminal CLI
```powershell
.venv\Scripts\Activate.ps1
python src/main.py
```
Use the menu to add/delete/search/list students; data saves to data/students.json.

## Running the Web App
```powershell
.venv\Scripts\Activate.ps1
python src/app.py
```
Then open http://127.0.0.1:5000

Web features:
- Add/Delete/Search/List students (REST calls to Flask)
- “Report” button per student opens a modal with bar/pie charts (matplotlib)
- All-students bar/pie endpoints: /api/charts/average/bar and /api/charts/average/pie

## Key Endpoints
- GET /api/students — list all
- POST /api/students — add
- DELETE /api/students/<enrollment_no> — delete
- GET /api/students/<enrollment_no>/average — average marks
- GET /api/students/search?q=term — search
- GET /api/charts/student/<enrollment_no>/bar — per-student bar chart
- GET /api/charts/student/<enrollment_no>/pie — per-student pie chart
- GET /api/charts/average/bar — all-students bar chart
- GET /api/charts/average/pie — all-students pie chart

## Tests
```powershell
.venv\Scripts\Activate.ps1
pytest
```

## License
MIT