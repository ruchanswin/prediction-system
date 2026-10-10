# backend/model/delay_prediction_db.py
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel's function filesystem is read-only; /tmp is writable but ephemeral.
DEFAULT_DATABASE_URL = (
    "sqlite:////tmp/delay_prediction.db"
    if os.getenv("VERCEL") == "1"
    else "sqlite:///./delay_prediction.db"
)
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Create the database engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the DelayPrediction model
class DelayPrediction(Base):
    __tablename__ = "delay_prediction"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, nullable=False) 
    day = Column(Integer, nullable=False)  
    daysofweek = Column(Integer, nullable=False)  
    originAirport = Column(String, nullable=False) 
    destinationAirport = Column(String, nullable=False)  
    scheduledDeparture = Column(Integer, nullable=False)  
    scheduledArrival = Column(Integer, nullable=False)  
    departureDelay = Column(Integer, nullable=False)  
    airTime = Column(Float, nullable=False)  
    distance = Column(Integer, nullable=False)  
    predicted_delay = Column(Float, nullable=False)  


# Create the table
Base.metadata.create_all(bind=engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
