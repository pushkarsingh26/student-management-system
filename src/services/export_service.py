from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
import pandas as pd
import io
from ..database import get_db
from ..models import StudentProfile, User
from ..auth import require_role
from ..models import RoleEnum

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/students/csv")
def export_students_csv(db: Session = Depends(get_db), current_user=Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER]))):
    records = db.query(StudentProfile, User).join(User).all()
    data = []
    for profile, user in records:
        data.append({
            "Enrollment No": profile.enrollment_no,
            "Name": user.name,
            "Email": user.email,
            "Age": profile.age,
            "Contact info": profile.contact_info
        })
        
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    response = Response(content=stream.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=students.csv"
    return response
