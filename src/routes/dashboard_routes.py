from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, StudentProfile, RoleEnum, Attendance, AttendanceStatus, Course
from ..auth import require_role

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    total_students = db.query(StudentProfile).count()
    total_teachers = db.query(User).filter(User.role == RoleEnum.TEACHER).count()
    total_courses = db.query(Course).count()
    
    total_attendance = db.query(Attendance).count()
    present_count = db.query(Attendance).filter(Attendance.status == AttendanceStatus.PRESENT).count()
    
    attendance_percentage = 0
    if total_attendance > 0:
        attendance_percentage = round((present_count / total_attendance) * 100, 2)
        
    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "attendance_percentage": attendance_percentage
    }
