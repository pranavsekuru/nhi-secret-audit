from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


class NHIRequest(BaseModel):
    name: str
    type: str
    status: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "NHI Secret Audit Service is running"
    }


# CREATE NHI
@app.post("/nhi")
def create_nhi(
    nhi: NHIRequest,
    db: Session = Depends(get_db)
):
    new_nhi = models.NHI(
        name=nhi.name,
        type=nhi.type,
        status=nhi.status
    )

    db.add(new_nhi)
    db.commit()
    db.refresh(new_nhi)

    return {
        "success": True,
        "message": "NHI registered successfully",
        "data": {
            "id": new_nhi.id,
            "name": new_nhi.name,
            "type": new_nhi.type,
            "status": new_nhi.status
        }
    }


# GET ALL NHIs
@app.get("/nhi")
def get_nhis(db: Session = Depends(get_db)):
    nhis = db.query(models.NHI).all()

    return {
        "success": True,
        "data": [
            {
                "id": nhi.id,
                "name": nhi.name,
                "type": nhi.type,
                "status": nhi.status
            }
            for nhi in nhis
        ]
    }