from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User, RoleEnum, StudentProfile, Course, Attendance, AttendanceStatus, Marks
from .auth import get_password_hash
from datetime import date, timedelta
import random

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin = User(
        email="admin@school.com", 
        password_hash=get_password_hash("admin123"), 
        name="System Admin", 
        role=RoleEnum.ADMIN
    )
    db.add(admin)
    
    teacher1 = User(email="smith@school.com", password_hash=get_password_hash("teacher123"), name="Mr. Smith", role=RoleEnum.TEACHER)
    teacher2 = User(email="doe@school.com", password_hash=get_password_hash("teacher123"), name="Mrs. Doe", role=RoleEnum.TEACHER)
    db.add(teacher1)
    db.add(teacher2)
    db.commit()
    
    math = Course(name="Advanced Mathematics", code="MATH301", teacher_id=teacher1.id)
    science = Course(name="Physics 101", code="PHY101", teacher_id=teacher2.id)
    cs = Course(name="Computer Science", code="CS101", teacher_id=teacher1.id)
    db.add(math)
    db.add(science)
    db.add(cs)
    db.commit()
    
    student_users = []
    for i in range(1, 16):
        su = User(email=f"student{i}@school.com", password_hash=get_password_hash("student123"), name=f"Alex Junior {i}", role=RoleEnum.STUDENT)
        db.add(su)
        student_users.append(su)
    db.commit()
    
    profiles = []
    for i, su in enumerate(student_users):
        sp = StudentProfile(user_id=su.id, enrollment_no=f"EN{2026000+i}", age=19+random.randint(0,2), contact_info=f"555-010{i}")
        db.add(sp)
        profiles.append(sp)
    db.commit()
    
    courses = [math, science, cs]
    for sp in profiles:
        for c in courses:
            for d in range(10):
                status = random.choices(
                    [AttendanceStatus.PRESENT, AttendanceStatus.ABSENT, AttendanceStatus.LATE], 
                    weights=[80, 15, 5]
                )[0]
                att = Attendance(student_id=sp.id, course_id=c.id, date=date.today() - timedelta(days=d), status=status)
                db.add(att)
            
            score = random.uniform(40, 95)
            mark = Marks(student_id=sp.id, course_id=c.id, exam_name="Midterms", score=score, total=100.0)
            db.add(mark)
            
    db.commit()
    db.close()
    print("Database seeded successfully! Admin: admin@school.com / admin123")

if __name__ == "__main__":
    seed_db()
