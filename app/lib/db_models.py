from datetime import datetime

from sqlalchemy import Column, Text, Integer, DateTime, String, Float, ForeignKey

from app.database import Base


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    timestamp_utc = Column(DateTime, default=datetime.utcnow())
    sample_id = Column(Integer)
    text = Column(Text)
    label = Column(String(40))


class PredictionDetails(Base):
    __tablename__ = "prediction_details"

    id = Column(Integer, primary_key=True)
    probability = Column(Float)
    label = Column(String(40))

    timestamp_utc = Column(DateTime, ForeignKey("predictions.timestamp_utc"))
    sample_id = Column(Integer, ForeignKey("predictions.sample_id"))
