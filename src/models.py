from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.STUDENT)
    name = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    enrollment_no = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer)
    contact_info = Column(String)

    user = relationship("User", back_populates="student_profile")
    attendance = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    marks = relationship("Marks", back_populates="student", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="student", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))

    teacher = relationship("User")
    attendance = relationship("Attendance", back_populates="course")
    marks = relationship("Marks", back_populates="course")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    date = Column(Date, default=func.current_date())
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    student = relationship("StudentProfile", back_populates="attendance")
    course = relationship("Course", back_populates="attendance")

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    exam_name = Column(String)
    score = Column(Float)
    total = Column(Float)

    student = relationship("StudentProfile", back_populates="marks")
    course = relationship("Course", back_populates="marks")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    file_name = Column(String)
    file_path = Column(String)
    document_type = Column(String) # e.g. Resume, Health Record

    student = relationship("StudentProfile", back_populates="documents")
