from sqlalchemy import Column,Integer,String,Text
from .database import Base

class EmailAnalysis(Base):
    __tablename__ = "email_analysis"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,nullable=False)
    risk_score = Column(Integer,nullable=False)
    risk_level = Column(String,nullable=False)
    reasons = Column(Text)