from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import User, StudentProfile, RoleEnum
from ..auth import get_current_user, require_role
from pydantic import BaseModel
from sqlalchemy import or_

router = APIRouter(prefix="/api/students", tags=["students"])

class StudentCreate(BaseModel):
    user_id: int
    enrollment_no: str
    age: int
    contact_info: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    user_id: int
    enrollment_no: str
    age: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    user = db.query(User).filter(User.id == student.user_id, User.role == RoleEnum.STUDENT).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student User not found")
        
    existing = db.query(StudentProfile).filter(StudentProfile.enrollment_no == student.enrollment_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Enrollment number already exists")

    new_profile = StudentProfile(
        user_id=student.user_id, 
        enrollment_no=student.enrollment_no, 
        age=student.age,
        contact_info=student.contact_info
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return {
        "id": new_profile.id,
        "user_id": new_profile.user_id,
        "enrollment_no": new_profile.enrollment_no,
        "age": new_profile.age,
        "name": user.name,
        "email": user.email
    }

@router.get("/")
def get_students(
    skip: int = 0, limit: int = 10, search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))
):
    query = db.query(StudentProfile, User).join(User)
    
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                StudentProfile.enrollment_no.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    results = query.offset(skip).limit(limit).all()
    
    students = []
    for profile, user in results:
        students.append({
            "id": profile.id,
            "user_id": user.id,
            "enrollment_no": profile.enrollment_no,
            "age": profile.age,
            "contact_info": profile.contact_info,
            "name": user.name,
            "email": user.email,
            "profile_pic": user.profile_pic
        })
        
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": students
    }

@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if current_user.role == RoleEnum.STUDENT and profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this profile")
        
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "enrollment_no": profile.enrollment_no,
        "age": profile.age,
        "contact_info": profile.contact_info,
        "name": profile.user.name,
        "email": profile.user.email,
        "profile_pic": profile.user.profile_pic
    }

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role([RoleEnum.ADMIN]))):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
        
    user = profile.user
    db.delete(profile)
    db.delete(user) 
    db.commit()
    
    return {"message": "Student successfully deleted"}
