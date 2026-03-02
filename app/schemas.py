from pydantic import BaseModel

class EmailCreate(BaseModel):
    sender:  str
    subject: str
    body: str 

class EmailResponse(BaseModel):
    id: int
    sender: str
    subject:str
    body: str
    risk_score: int

    class Config:
        from_attributes = True