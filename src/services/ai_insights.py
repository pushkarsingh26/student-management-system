from sqlalchemy.orm import Session
from ..models import Attendance, AttendanceStatus, Marks
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..auth import require_role
from ..models import RoleEnum

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.get("/insights/{student_id}")
def generate_insights(student_id: int, db: Session = Depends(get_db), current_user=Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    total_att = db.query(Attendance).filter(Attendance.student_id == student_id).count()
    present_att = db.query(Attendance).filter(Attendance.student_id == student_id, Attendance.status == AttendanceStatus.PRESENT).count()
    
    attendance_rate = (present_att / total_att * 100) if total_att > 0 else 100
    
    marks_records = db.query(Marks).filter(Marks.student_id == student_id).all()
    avg_score = 0
    if marks_records:
        total_p = sum([(m.score / m.total) * 100 for m in marks_records if m.total > 0])
        avg_score = total_p / len(marks_records)
        
    prediction = "Stable"
    risk_level = "Low"
    advice = "Keep up the good work."
    
    if attendance_rate < 75:
        prediction = "Likely to drop in performance"
        risk_level = "High"
        advice = "Warning: Attendance is below 75%. Student is at risk of falling behind."
        
    if avg_score < 50:
        if attendance_rate < 75:
            prediction = "High risk of failure"
            advice = "Critical Intervention Required. Both attendance and marks are critical."
        else:
            prediction = "Struggling with material"
            risk_level = "Medium"
            advice = "Good attendance, but low marks. Suggest tutoring."
            
    return {
        "attendance_rate": round(attendance_rate, 2),
        "average_score": round(avg_score, 2),
        "prediction": prediction,
        "risk_level": risk_level,
        "advice": advice
    }
