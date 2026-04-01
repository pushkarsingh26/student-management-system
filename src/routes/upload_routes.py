from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os
from ..database import get_db
from ..models import User, StudentProfile, RoleEnum, Document
from ..auth import get_current_user, require_role

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/profile_pic")
def upload_profile_pic(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    file_extension = file.filename.split(".")[-1]
    file_path = f"{UPLOAD_DIR}/user_{current_user.id}_pic.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    current_user.profile_pic = f"/api/upload/static/{os.path.basename(file_path)}"
    db.commit()
    
    return {"message": "Profile picture updated", "url": current_user.profile_pic}

@router.post("/document/{student_id}")
def upload_document(
    student_id: int,
    doc_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.TEACHER, RoleEnum.STUDENT]))
):
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if current_user.role == RoleEnum.STUDENT and profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    file_path = f"{UPLOAD_DIR}/student_{student_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_doc = Document(
        student_id=student_id,
        file_name=file.filename,
        file_path=f"/api/upload/static/{os.path.basename(file_path)}",
        document_type=doc_type
    )
    db.add(new_doc)
    db.commit()
    
    return {"message": "Document uploaded successfully", "url": new_doc.file_path}

@router.get("/static/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
