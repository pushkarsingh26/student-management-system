# Next-Gen Student Management System

A production-ready, highly robust Student Management System built using a **FastAPI** backend and a stunning, responsive **Vanilla HTML/JS/CSS** glassmorphism frontend. This project is designed as an "interview-level" showcase, ditching basic JSON stores in favor of a relational database, strict JSON Web Tokens (JWT) based authentication, Role-Based Access Control (RBAC), and Artificial Intelligence heuristics.

## ✨ Key Features
- **FastAPI Backend Architecture**: Completely async-ready REST API built with industry-standard Python frameworks.
- **Relational Database**: Advanced SQLAlchemy models with 1-to-many relationships tracking Students, Courses, Attendance, Marks, and Users. Data is persisted to SQLite.
- **Secure Authentication**: End-to-end `bcrypt` password hashing and stateless JWT-based login mechanism ensuring robust session security.
- **Role-Based Access Control (RBAC)**: Distinct permissions separating Admin, Teacher, and Student routes natively at the dependency level.
- **Premium Glassmorphism UI**: A gorgeous, mobile-responsive "App Shell" dashboard integrating custom wallpapers, background blur effects, and smooth screen transitions without the bloat of React/Angular.
- **AI Smart Insights Engine**: A heuristic-based data integration module that evaluates historical attendance and grade trajectories to predict "At-Risk" students dynamically.
- **Data Export**: Built-in Pandas-powered CSV exports.
- **Data Visualization**: Smooth integrations with `Chart.js` for dynamic administrative dashboards.

## 🛠️ Project Structure
```text
student-management-system/
├── public/                 # Vanilla JS / CSS Frontend Single Page Application
│   ├── css/
│   │   ├── theme.css       # Core variables & background rendering
│   │   ├── layout.css      # App Shell and global flex configurations
│   │   └── components.css  # Granular UI elements (glass cards, buttons)
│   ├── js/
│   │   ├── api.js          # Fetch wrapper intercepting JWT tokens natively
│   │   ├── app.js          # SPA Controller & Route management
│   │   ├── dashboard.js    # Chart logic
│   │   └── students.js     # Data Table logic
│   └── index.html          # Dynamic Template Shell
├── src/                    # FastAPI Backend
│   ├── routes/             # Segmented API logic modules
│   ├── services/           # External microservice layers (AI, Exports)
│   ├── auth.py             # JWT and Passlib handler
│   ├── database.py         # SQLAlchemy engine connection
│   ├── main.py             # Master FastAPI instance & CORS
│   └── models.py           # Pydantic and SQLAlchemy Relational Schemas
├── .venv/                  # Virtual Environment
├── requirements.txt        # Python Packages
└── seed.py                 # Initial testing data seeder
```

## 🚀 Setup Instructions

This project relies on Python 3.10+ and standard virtual environments. Commands assume a PowerShell terminal on Windows.

1. **Clone the Repository**
2. **Setup the Virtual Environment & Dependencies**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Migrate and Seed the Database**
   To experience the system instantly with pre-populated dummy data and admin accounts, run the built-in data seeder module:
   ```powershell
   .venv\Scripts\python -m src.seed
   ```

## 🖥️ Running the Application

1. **Boot the API & Web Server**
   Start the FastAPI instance using `uvicorn`. The API dynamically mounts and serves the `public/` directory interface alongside the endpoints.
   ```powershell
   .venv\Scripts\uvicorn src.main:app --port 8000
   ```
2. **Access the App**
   Open your browser and navigate to: `http://127.0.0.1:8000`

### Example Demo Credentials
The `seed.py` command automatically generates a test Administrator account for you:
- **Email**: `admin@school.com`
- **Password**: `admin123`

## 🎨 Modifying Background Graphics
The user interface features a highly responsive UI that adapts its style between Desktop and Mobile automatically. To personalize it:
1. Drag and drop your desired desktop image into `public/img/bg-laptop.png`
2. Drag and drop your desired mobile image into `public/img/bg-mobile.png` 

The CSS `backdrop-filter` rules dynamically apply a frosted glass overlay rendering on top of these images automatically.

## 📄 License
MIT