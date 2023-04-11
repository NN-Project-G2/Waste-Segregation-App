from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database_manager import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=True)
    secret_question_answer = Column(String(1024), nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    

class UserPrediction(Base):
    __tablename__ = "user_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    image_s3_path = Column(String(1024), nullable=True)
    predicted_label = Column(String(255), nullable=True)
    actual_label = Column(String(255), nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
