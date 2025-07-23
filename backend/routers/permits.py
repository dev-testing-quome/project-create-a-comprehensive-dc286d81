from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import PermitApplicationCreate, PermitApplication
from services import permits_service

router = APIRouter(prefix="/api/permits", tags=["Permits"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PermitApplication, status_code=status.HTTP_201_CREATED)
def create_permit_application(permit: PermitApplicationCreate, db: Session = Depends(get_db)):
    return permits_service.create_permit_application(db, permit)

@router.get("/{permit_id}", response_model=PermitApplication)
def get_permit_application(permit_id: int, db: Session = Depends(get_db)):
    permit = permits_service.get_permit_application(db, permit_id)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit application not found")
    return permit
