from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..models import User, StudentProfile, RoleEnum, Attendance, AttendanceStatus, Course
from ..auth import get_current_user, require_role
from pydantic import BaseModel

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

class AttendanceMark(BaseModel):
    student_id: int
    course_id: int
    status: AttendanceStatus
    date_marked: date

@router.post("/")
def mark_attendance(data: AttendanceMark, db: Session = Depends(get_db), current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    existing = db.query(Attendance).filter(
        Attendance.student_id == data.student_id,
        Attendance.course_id == data.course_id,
        Attendance.date == data.date_marked
    ).first()
    
    if existing:
        existing.status = data.status
    else:
        new_att = Attendance(student_id=data.student_id, course_id=data.course_id, date=data.date_marked, status=data.status)
        db.add(new_att)
    
    db.commit()
    return {"message": "Attendance marked successfully"}

@router.get("/student/{student_id}")
def get_student_attendance(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if current_user.role == RoleEnum.STUDENT and profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    records = db.query(Attendance, Course).join(Course).filter(Attendance.student_id == student_id).order_by(Attendance.date.desc()).all()
    
    return [
        {
            "id": att.id,
            "course_id": course.id,
            "course": course.name,
            "date": att.date,
            "status": att.status.value
        } for att, course in records
    ]
