

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, Email
from .schemas import EmailCreate



app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI Phishing Platform Running"}


@app.post("/emails/", response_model=EmailResponse)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    db_email = Email(
        sender=email.sender,
        subject=email.subject,
        body=email.body,
        risk_score=0
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)

    return db_email