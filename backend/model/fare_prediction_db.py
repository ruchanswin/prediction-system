# backend/model/fare_prediction_db.py
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel's function filesystem is read-only; /tmp is writable but ephemeral.
DEFAULT_DATABASE_URL = (
    "sqlite:////tmp/fare_prediction.db"
    if os.getenv("VERCEL") == "1"
    else "sqlite:///./fare_prediction.db"
)
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Create the database engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the FarePrediction model
class FarePrediction(Base):
    __tablename__ = "fare_prediction"

    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String, nullable=False)
    source_city = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)
    stops = Column(String, nullable=False)
    flight_class = Column(String, nullable=False)
    duration = Column(Float, nullable=False) 
    days_left = Column(Integer, nullable=False)
    predicted_fare = Column(Float, nullable=False)

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
