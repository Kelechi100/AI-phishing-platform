
# Import FastAPI framework
from fastapi import FastAPI, Depends

# Import session type for typing
from sqlalchemy.orm import Session

# Import database engine and dependency
from .database import engine, get_db

# Import database models
from .models import Base, Email

# Import request and response schemas
from .schemas import EmailCreate, EmailResponse

# Import phishing detection logic
from .services.detection import calculate_risk_score

# Create FastAPI app instance
app = FastAPI()

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)


def classify_risk(score: int) -> str:
    if score < 30:
        return "LOW"
    elif score < 60:
        return "MEDIUM"
    else:
        return "HIGH"
# Root endpoint to verify API is running
@app.get("/")
def root():
    return {"message": "AI Phishing Platform Running"}


# Endpoint to create a new email record
@app.post("/emails/", response_model=EmailResponse)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):

    # Calculating the  phishing risk score using service layer
    score, reasons = calculate_risk_score(
        sender=email.sender,
        subject=email.subject,
        body=email.body
    )
    risk_level = classify_risk(score)
    # Created SQLAlchemy model instance
    db_email = Email(
        sender=email.sender,
        subject=email.subject,
        body=email.body,
        risk_score=score
    )

    # Stage insert into database
    db.add(db_email)

    # Commit transaction (save permanently)
    db.commit()

    # Refresh instance to get generated fields like ID
    db.refresh(db_email)

    # Return saved email (converted via response schema)
    return {
        "id": db_email.id,
        "sender": db_email.sender,
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }