from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routes import auth_routes, student_routes, attendance_routes, marks_routes, dashboard_routes, upload_routes
from .services import ai_insights, export_service
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/api/upload/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(attendance_routes.router)
app.include_router(marks_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(upload_routes.router)
app.include_router(ai_insights.router)
app.include_router(export_service.router)

os.makedirs("public", exist_ok=True)
app.mount("/", StaticFiles(directory="public", html=True), name="public")