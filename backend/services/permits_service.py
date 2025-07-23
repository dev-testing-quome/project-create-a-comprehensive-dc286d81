from sqlalchemy.orm import Session
from schemas import PermitApplicationCreate, PermitApplication
from models import PermitApplication as PermitApplicationModel

def create_permit_application(db: Session, permit: PermitApplicationCreate):
    db_permit = PermitApplicationModel(permit_type=permit.permit_type, status="pending")
    db.add(db_permit)
    db.commit()
    db.refresh(db_permit)
    return PermitApplication.from_orm(db_permit)

def get_permit_application(db: Session, permit_id: int):
    return db.query(PermitApplicationModel).filter(PermitApplicationModel.id == permit_id).first()
