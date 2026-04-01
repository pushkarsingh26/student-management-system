from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, StudentProfile, RoleEnum, Marks, Course
from ..auth import get_current_user, require_role
from pydantic import BaseModel

router = APIRouter(prefix="/api/marks", tags=["marks"])

class MarkEntry(BaseModel):
    student_id: int
    course_id: int
    exam_name: str
    score: float
    total: float

@router.post("/")
def add_marks(data: MarkEntry, db: Session = Depends(get_db), current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    existing = db.query(Marks).filter(
        Marks.student_id == data.student_id,
        Marks.course_id == data.course_id,
        Marks.exam_name == data.exam_name
    ).first()
    
    if existing:
        existing.score = data.score
        existing.total = data.total
    else:
        new_mark = Marks(**data.dict())
        db.add(new_mark)
        
    db.commit()
    return {"message": "Marks recorded successfully"}

@router.get("/student/{student_id}")
def get_student_marks(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if current_user.role == RoleEnum.STUDENT and profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    records = db.query(Marks, Course).join(Course).filter(Marks.student_id == student_id).all()
    
    return [
        {
            "id": mark.id,
            "course": course.name,
            "exam_name": mark.exam_name,
            "score": mark.score,
            "total": mark.total,
            "percentage": round((mark.score / mark.total) * 100, 2) if mark.total > 0 else 0
        } for mark, course in records
    ]
